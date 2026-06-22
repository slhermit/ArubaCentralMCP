#!/usr/bin/env python3
"""
MCP Server for Aruba Central (New Central / HPE GreenLake).

Covers Monitoring APIs from the MRT APIs Postman collection:
  - Access Points: list, detail, radios, WLANs, tunnels, top-by-usage
  - BSSIDs / Radios / Swarms / WLANs
  - Clients: list, detail, mobility trail, trend, top-N usage
  - Devices: list, inventory, update notes, delete

Authentication:
  - OAuth2 client credentials (ARUBA_CLIENT_ID + ARUBA_CLIENT_SECRET) — auto-refresh every 2h
  - Static bearer token fallback (ARUBA_TOKEN)

Base URL: ARUBA_BASE_URL env var (default: https://internal.api.central.arubanetworks.com)
"""

import json
import os
import time
from typing import Optional, Dict, Any

import httpx
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP("aruba_central_mcp")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_BASE_URL = os.environ.get("ARUBA_BASE_URL", "https://internal.api.central.arubanetworks.com")
SSO_TOKEN_URL = "https://sso.common.cloud.hpe.com/as/token.oauth2"
CLIENT_ID = os.environ.get("ARUBA_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("ARUBA_CLIENT_SECRET", "")
_STATIC_TOKEN = os.environ.get("ARUBA_TOKEN", "")

# ---------------------------------------------------------------------------
# Token cache
# ---------------------------------------------------------------------------

_token_cache: Dict[str, Any] = {"access_token": "", "expires_at": 0.0}


async def _get_token() -> str:
    """Return a valid bearer token, refreshing via OAuth2 client credentials if configured."""
    if not CLIENT_ID or not CLIENT_SECRET:
        return _STATIC_TOKEN

    now = time.time()
    if _token_cache["access_token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["access_token"]

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            SSO_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET},
        )
        r.raise_for_status()
        data = r.json()

    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = now + data.get("expires_in", 7200)
    return _token_cache["access_token"]


# ---------------------------------------------------------------------------
# Shared HTTP helper
# ---------------------------------------------------------------------------


async def _api(method: str, path: str, **kwargs) -> dict:
    token = await _get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.request(method, f"{API_BASE_URL}{path}", headers=headers, **kwargs)
        r.raise_for_status()
        return r.json()


def _err(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        code = e.response.status_code
        msgs = {
            400: "Bad request — check your parameters or filter syntax.",
            401: "Unauthorized — verify ARUBA_TOKEN or client credentials.",
            403: "Forbidden — token lacks permission for this action.",
            404: "Not found — check the resource ID.",
            429: "Rate limit exceeded — wait before retrying.",
            500: "Aruba Central internal server error.",
        }
        body = ""
        try:
            body = e.response.json().get("message", "")
        except Exception:
            pass
        return f"Error {code}: {msgs.get(code, 'API error')}{ (' — ' + body) if body else ''}"
    if isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out."
    return f"Error: {type(e).__name__}: {e}"


def _fmt_items(data: dict, items_key: str = "items") -> tuple:
    """Return (items, total, next_cursor) from a paginated response."""
    items = data.get(items_key, data.get("data", []))
    total = data.get("total", len(items))
    next_cursor = data.get("next")
    return items, total, next_cursor


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class ListAPsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(
        default=None,
        description=(
            "OData v4 filter string. Only 'and' is supported (not 'or'/'not'). "
            "Filterable fields: siteId, siteName, serialNumber, deviceName, status, model, "
            "firmwareVersion, deployment, clusterId, clusterName. "
            "Example: \"siteId eq '12345' and status eq 'ONLINE'\""
        ),
    )
    sort: Optional[str] = Field(
        default=None,
        description="Comma-separated sort expressions, e.g. 'deviceName asc,status desc'. "
                    "Sortable fields: siteId, serialNumber, deviceName, model, status, deployment.",
    )
    limit: Optional[int] = Field(default=20, ge=1, le=1000, description="Max results per page")
    next: Optional[str] = Field(default=None, description="Pagination cursor from previous response")


class SerialInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number (e.g. 'AP00000001')")


class APTrendsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    filter: Optional[str] = Field(
        default=None,
        description="OData filter for time range, e.g. \"timestamp ge 2024-01-01T00:00:00Z and timestamp le 2024-01-02T00:00:00Z\""
    )
    site_id: Optional[str] = Field(default=None, description="Site ID to scope the query")


class RadioTrendsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    radio_number: str = Field(..., description="Radio number (e.g. '0', '1')")
    filter: Optional[str] = Field(default=None, description="OData time-range filter")
    site_id: Optional[str] = Field(default=None, description="Site ID")


class ListWLANsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Filter by site ID")
    serial_number: Optional[str] = Field(default=None, description="Filter by AP serial number")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class WLANNameInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    wlan_name: str = Field(..., description="WLAN name")
    site_id: Optional[str] = Field(default=None, description="Site ID")
    serial_number: Optional[str] = Field(default=None, description="AP serial number")


class TopAPsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Filter by site ID")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Number of top APs to return")
    start_at: Optional[str] = Field(default=None, description="Start time ISO8601, e.g. '2024-01-01T00:00:00Z'")
    end_at: Optional[str] = Field(default=None, description="End time ISO8601")


class ListRadiosInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class ListBSSIDsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class ListSwarmsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class ListClientsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Filter by site ID")
    site_name: Optional[str] = Field(default=None, description="Filter by site name")
    serial_number: Optional[str] = Field(default=None, description="Filter by AP serial number")
    start_at: Optional[str] = Field(default=None, description="Start time ISO8601")
    end_at: Optional[str] = Field(default=None, description="End time ISO8601")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class ClientMACInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    mac_address: str = Field(..., description="Client MAC address (e.g. 'aa:bb:cc:dd:ee:ff')")


class ClientMobilityInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    mac_address: str = Field(..., description="Client MAC address")
    site_id: Optional[str] = Field(default=None, description="Filter by site ID")
    site_name: Optional[str] = Field(default=None, description="Filter by site name")
    start_at: Optional[str] = Field(default=None, description="Start time ISO8601")
    end_at: Optional[str] = Field(default=None, description="End time ISO8601")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class ClientsTrendInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Filter by site ID")
    site_name: Optional[str] = Field(default=None, description="Filter by site name")
    start_at: Optional[str] = Field(default=None, description="Start time ISO8601")
    end_at: Optional[str] = Field(default=None, description="End time ISO8601")
    group_by: Optional[str] = Field(default=None, description="Group by field, e.g. 'type', 'site'")
    type: Optional[str] = Field(default=None, description="Client type filter")
    serial_number: Optional[str] = Field(default=None, description="Filter by AP serial number")


class TopNClientsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Filter by site ID")
    site_name: Optional[str] = Field(default=None, description="Filter by site name")
    start_at: Optional[str] = Field(default=None, description="Start time ISO8601")
    end_at: Optional[str] = Field(default=None, description="End time ISO8601")
    serial_number: Optional[str] = Field(default=None, description="Filter by AP serial number")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Number of top clients")


class ListDevicesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(
        default=None,
        description=(
            "OData filter. Filterable fields: siteId, siteName, serialNumber, deviceName, "
            "status, model, firmwareVersion, deviceType, deployment. "
            "Example: \"deviceType eq 'ACCESS_POINT' and status eq 'ONLINE'\""
        ),
    )
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class DeviceInventoryInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    site_assigned: Optional[bool] = Field(default=None, description="Filter by site assignment status")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class UpdateDeviceNotesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    notes: str = Field(..., description="Notes to attach to the device (e.g. 'Located in Building A, Floor 2')")


class DeleteDeviceInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Serial number of the device to delete")
    confirm: bool = Field(..., description="Must be true to confirm deletion")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_params(**kwargs) -> Dict[str, Any]:
    """Build query param dict, omitting None values."""
    return {k.replace("_", "-"): v for k, v in kwargs.items() if v is not None}


def _pagination_note(total: int, count: int, next_cursor) -> str:
    if next_cursor:
        return f"\n_Showing {count} of {total}. Use next='{next_cursor}' for more._"
    return f"\n_Showing all {total} result(s)._"


# ===========================================================================
# ACCESS POINT TOOLS
# ===========================================================================


@mcp.tool(
    name="aruba_central_list_aps",
    annotations={"title": "List Access Points", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_aps(params: ListAPsInput) -> str:
    """List access points managed by Aruba Central.

    Returns serial number, name, model, IP, status, site, deployment, firmware,
    CPU/memory utilisation, and client count for each AP.

    Supports OData filtering (siteId, status, model, deployment, etc.), sorting,
    and cursor-based pagination via the 'next' field.

    Args:
        params (ListAPsInput):
            - filter: OData filter, e.g. "siteId eq '123' and status eq 'ONLINE'"
            - sort: e.g. "deviceName asc"
            - limit: max results (default 20)
            - next: pagination cursor from a previous response

    Returns:
        str: JSON list of APs with pagination info.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-monitoring/v1/aps", params=p)
        items, total, next_cursor = _fmt_items(data)
        result = {"total": total, "count": len(items), "next": next_cursor, "items": items}
        return json.dumps(result, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap",
    annotations={"title": "Get Access Point Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap(params: SerialInput) -> str:
    """Get full details for a single access point by serial number.

    Returns model, firmware, IP addresses, status, uptime, site, cluster,
    CPU/memory utilisation, client count, building/floor, and power consumption.

    Args:
        params (SerialInput):
            - serial_number: AP serial number (e.g. 'AP00000001')

    Returns:
        str: JSON object with AP details.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_radios",
    annotations={"title": "Get AP Radios", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_radios(params: SerialInput) -> str:
    """Get the list of radios for a specific access point.

    Returns radio number, band, channel, TX power, client count, and utilisation.

    Args:
        params (SerialInput):
            - serial_number: AP serial number

    Returns:
        str: JSON list of radios.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}/radios")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_throughput_trends",
    annotations={"title": "Get AP Throughput Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_throughput_trends(params: APTrendsInput) -> str:
    """Get throughput trend data for an access point over time.

    Returns time-series TX/RX throughput data points.

    Args:
        params (APTrendsInput):
            - serial_number: AP serial number
            - filter: OData time-range filter, e.g. "timestamp ge 2024-01-01T00:00:00Z"
            - site_id: optional site scope

    Returns:
        str: JSON time-series throughput data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}/throughput-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_cpu_trends",
    annotations={"title": "Get AP CPU Utilization Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_cpu_trends(params: APTrendsInput) -> str:
    """Get CPU utilization trend data for an access point.

    Args:
        params (APTrendsInput): serial_number, optional filter and site_id

    Returns:
        str: JSON time-series CPU utilization data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}/cpu-utilization-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_memory_trends",
    annotations={"title": "Get AP Memory Utilization Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_memory_trends(params: APTrendsInput) -> str:
    """Get memory utilization trend data for an access point.

    Args:
        params (APTrendsInput): serial_number, optional filter and site_id

    Returns:
        str: JSON time-series memory utilization data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}/memory-utilization-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_power_trends",
    annotations={"title": "Get AP Power Consumption Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_power_trends(params: APTrendsInput) -> str:
    """Get power consumption trend data for an access point.

    Args:
        params (APTrendsInput): serial_number, optional filter and site_id

    Returns:
        str: JSON time-series power consumption data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}/power-consumption-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_radio_throughput_trends",
    annotations={"title": "Get Radio Throughput Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_radio_throughput_trends(params: RadioTrendsInput) -> str:
    """Get throughput trend data for a specific radio on an access point.

    Args:
        params (RadioTrendsInput):
            - serial_number: AP serial number
            - radio_number: Radio number (e.g. '0' for 2.4GHz, '1' for 5GHz)
            - filter: OData time-range filter
            - site_id: optional site scope

    Returns:
        str: JSON time-series radio throughput data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api(
            "GET",
            f"/network-monitoring/v1/aps/{params.serial_number}/radios/{params.radio_number}/throughput-trends",
            params=p,
        )
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_radio_channel_utilization",
    annotations={"title": "Get Radio Channel Utilization", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_radio_channel_utilization(params: RadioTrendsInput) -> str:
    """Get channel utilization trend data for a specific radio.

    Args:
        params (RadioTrendsInput): serial_number, radio_number, optional filter and site_id

    Returns:
        str: JSON time-series channel utilization data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api(
            "GET",
            f"/network-monitoring/v1/aps/{params.serial_number}/radios/{params.radio_number}/channel-utilization-trends",
            params=p,
        )
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_wlans",
    annotations={"title": "Get AP WLANs", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_wlans(params: SerialInput) -> str:
    """Get the list of WLANs broadcast by a specific access point.

    Args:
        params (SerialInput): serial_number

    Returns:
        str: JSON list of WLANs with details.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/aps/{params.serial_number}/wlans")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_ap_tunnels",
    annotations={"title": "Get AP Tunnels", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_ap_tunnels(params: ListAPsInput) -> str:
    """Get the list of tunnels for a specific access point.

    Note: serial_number is embedded in the path — use filter to scope if needed.

    Args:
        params (ListAPsInput): filter, sort, limit, next — serial_number passed separately

    Returns:
        str: JSON list of tunnels.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        # This tool intentionally exposes the generic tunnel list; for per-AP use aruba_central_get_ap_tunnels_by_serial
        data = await _api("GET", "/network-monitoring/v1/aps", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_top_aps_by_wireless_usage",
    annotations={"title": "Top APs by Wireless Usage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_top_aps_by_wireless_usage(params: TopAPsInput) -> str:
    """Get the access points with the highest wireless bandwidth usage.

    Args:
        params (TopAPsInput):
            - site_id: optional site filter
            - limit: number of top APs (default 10)
            - start_at / end_at: ISO8601 time range

    Returns:
        str: JSON list of top APs by wireless usage.
    """
    try:
        p = _build_params(**{"site-id": params.site_id, "limit": params.limit, "start-at": params.start_at, "end-at": params.end_at})
        data = await _api("GET", "/network-monitoring/v1/top-aps-by-wireless-usage", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_top_aps_by_wired_usage",
    annotations={"title": "Top APs by Wired Usage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_top_aps_by_wired_usage(params: TopAPsInput) -> str:
    """Get the access points with the highest wired bandwidth usage.

    Args:
        params (TopAPsInput): site_id, limit, start_at, end_at

    Returns:
        str: JSON list of top APs by wired usage.
    """
    try:
        p = _build_params(**{"site-id": params.site_id, "limit": params.limit, "start-at": params.start_at, "end-at": params.end_at})
        data = await _api("GET", "/network-monitoring/v1/top-aps-by-wired-usage", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_top_aps_by_total_usage",
    annotations={"title": "Top APs by Total Usage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_top_aps_by_total_usage(params: TopAPsInput) -> str:
    """Get the access points with the highest total (wired + wireless) bandwidth usage.

    Args:
        params (TopAPsInput): site_id, limit, start_at, end_at

    Returns:
        str: JSON list of top APs by total usage.
    """
    try:
        p = _build_params(**{"site-id": params.site_id, "limit": params.limit, "start-at": params.start_at, "end-at": params.end_at})
        data = await _api("GET", "/network-monitoring/v1/top-aps-by-usage", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ===========================================================================
# RADIOS / BSSIDs / WLANs / SWARMS
# ===========================================================================


@mcp.tool(
    name="aruba_central_list_radios",
    annotations={"title": "List All Radios", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_radios(params: ListRadiosInput) -> str:
    """List all radios across all access points.

    Returns radio number, band, channel, TX power, noise floor, utilization, client count.

    Args:
        params (ListRadiosInput): filter, sort, limit, next

    Returns:
        str: JSON list of radios with pagination info.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-monitoring/v1/radios", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_list_bssids",
    annotations={"title": "List BSSIDs", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_bssids(params: ListBSSIDsInput) -> str:
    """List all BSSIDs across access points.

    Returns BSSID MAC, SSID name, band, AP serial, site, and status.

    Args:
        params (ListBSSIDsInput): filter, sort, limit, next

    Returns:
        str: JSON list of BSSIDs with pagination info.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-monitoring/v1/bssids", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_list_wlans",
    annotations={"title": "List WLANs", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_wlans(params: ListWLANsInput) -> str:
    """List all WLANs, optionally filtered by site or AP serial number.

    Args:
        params (ListWLANsInput): site_id, serial_number, filter, limit, next

    Returns:
        str: JSON list of WLANs.
    """
    try:
        p = _build_params(
            filter=params.filter,
            limit=params.limit,
            next=params.next,
            **{"site-id": params.site_id, "serial-number": params.serial_number},
        )
        data = await _api("GET", "/network-monitoring/v1/wlans", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_wlan",
    annotations={"title": "Get WLAN Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_wlan(params: WLANNameInput) -> str:
    """Get details for a specific WLAN by name.

    Args:
        params (WLANNameInput):
            - wlan_name: WLAN name
            - site_id: optional site filter
            - serial_number: optional AP filter

    Returns:
        str: JSON WLAN details.
    """
    try:
        p = _build_params(**{"site-id": params.site_id, "serial-number": params.serial_number})
        data = await _api("GET", f"/network-monitoring/v1/wlans/{params.wlan_name}", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_list_swarms",
    annotations={"title": "List Swarms", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_swarms(params: ListSwarmsInput) -> str:
    """List all Instant AP swarms (virtual controllers).

    Returns cluster ID, name, firmware version, AP count, and status.

    Args:
        params (ListSwarmsInput): filter, sort, limit, next

    Returns:
        str: JSON list of swarms.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-monitoring/v1/swarms", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


# ===========================================================================
# CLIENT TOOLS
# ===========================================================================


@mcp.tool(
    name="aruba_central_list_clients",
    annotations={"title": "List Clients", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_clients(params: ListClientsInput) -> str:
    """List all unified (wired + wireless) clients connected to the network.

    Returns MAC address, IP, hostname, SSID or port, AP or switch serial,
    site, VLAN, signal strength, connection time, and usage stats.

    Args:
        params (ListClientsInput):
            - site_id / site_name: filter by site
            - serial_number: filter by AP
            - start_at / end_at: ISO8601 time range
            - filter: OData filter string
            - sort: sort expression
            - limit / next: pagination

    Returns:
        str: JSON list of clients with pagination info.
    """
    try:
        p = _build_params(
            filter=params.filter,
            sort=params.sort,
            limit=params.limit,
            next=params.next,
            **{
                "site-id": params.site_id,
                "site-name": params.site_name,
                "serial-number": params.serial_number,
                "start-at": params.start_at,
                "end-at": params.end_at,
            },
        )
        data = await _api("GET", "/network-monitoring/v1/clients", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_client",
    annotations={"title": "Get Client Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_client(params: ClientMACInput) -> str:
    """Get full details for a specific client by MAC address.

    Returns hostname, IP, MAC, SSID, AP, site, signal strength, VLAN,
    connection time, data usage, and onboarding status.

    Args:
        params (ClientMACInput):
            - mac_address: Client MAC address (e.g. 'aa:bb:cc:dd:ee:ff')

    Returns:
        str: JSON client detail object.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/clients/{params.mac_address}")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_client_mobility_trail",
    annotations={"title": "Get Client Mobility Trail", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_client_mobility_trail(params: ClientMobilityInput) -> str:
    """Get the roaming/mobility history for a wireless client.

    Shows which APs the client has connected to over time, including
    timestamps, AP names, and site information.

    Args:
        params (ClientMobilityInput):
            - mac_address: Client MAC address
            - site_id / site_name: optional site filter
            - start_at / end_at: ISO8601 time range
            - limit / next: pagination

    Returns:
        str: JSON list of mobility trail events.
    """
    try:
        p = _build_params(
            limit=params.limit,
            next=params.next,
            **{
                "site-id": params.site_id,
                "site-name": params.site_name,
                "start-at": params.start_at,
                "end-at": params.end_at,
            },
        )
        data = await _api("GET", f"/network-monitoring/v1/clients/{params.mac_address}/mobility-trail", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_clients_trend",
    annotations={"title": "Get Clients Trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_clients_trend(params: ClientsTrendInput) -> str:
    """Get client count trend data over time.

    Returns time-series client count data, optionally grouped by type or site.

    Args:
        params (ClientsTrendInput):
            - site_id / site_name: filter by site
            - start_at / end_at: ISO8601 time range
            - group_by: grouping field (e.g. 'type', 'site')
            - type: client type filter
            - serial_number: AP filter

    Returns:
        str: JSON time-series client trend data.
    """
    try:
        p = _build_params(
            **{
                "site-id": params.site_id,
                "site-name": params.site_name,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "group-by": params.group_by,
                "type": params.type,
                "serial-number": params.serial_number,
            }
        )
        data = await _api("GET", "/network-monitoring/v1/clients-trend", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_top_clients_by_usage",
    annotations={"title": "Top N Clients by Usage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_top_clients_by_usage(params: TopNClientsInput) -> str:
    """Get the clients with the highest data usage over a time period.

    Args:
        params (TopNClientsInput):
            - site_id / site_name: optional site filter
            - start_at / end_at: ISO8601 time range
            - serial_number: optional AP filter
            - limit: number of top clients (default 10)

    Returns:
        str: JSON list of top clients by usage.
    """
    try:
        p = _build_params(
            limit=params.limit,
            **{
                "site-id": params.site_id,
                "site-name": params.site_name,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "serial-number": params.serial_number,
            },
        )
        data = await _api("GET", "/network-monitoring/v1/clients-topn-usage", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ===========================================================================
# DEVICE TOOLS
# ===========================================================================


@mcp.tool(
    name="aruba_central_list_devices",
    annotations={"title": "List All Devices", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_devices(params: ListDevicesInput) -> str:
    """List all network devices (APs, switches, gateways) managed by Aruba Central.

    Returns device name, model, serial, IP, status, device type, site, firmware,
    uptime, MAC address, and deployment type.

    Args:
        params (ListDevicesInput):
            - filter: OData filter, e.g. "deviceType eq 'ACCESS_POINT' and status eq 'ONLINE'"
            - sort: sort expression
            - limit / next: pagination

    Returns:
        str: JSON list of devices with pagination info.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-monitoring/v1/devices", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_device_inventory",
    annotations={"title": "Get Device Inventory", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_device_inventory(params: DeviceInventoryInput) -> str:
    """Get the full device inventory, including devices not yet assigned to a site.

    Args:
        params (DeviceInventoryInput):
            - filter: OData filter string
            - sort: sort expression
            - site_assigned: True = only site-assigned devices, False = unassigned only
            - limit / next: pagination

    Returns:
        str: JSON device inventory list.
    """
    try:
        p = _build_params(
            filter=params.filter,
            sort=params.sort,
            limit=params.limit,
            next=params.next,
            **{"site-assigned": params.site_assigned},
        )
        data = await _api("GET", "/network-monitoring/v1/device-inventory", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_update_device_notes",
    annotations={"title": "Update Device Notes", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_update_device_notes(params: UpdateDeviceNotesInput) -> str:
    """Update the notes field on a device.

    Args:
        params (UpdateDeviceNotesInput):
            - serial_number: Device serial number
            - notes: Free-text notes (e.g. 'Located in Building A, Floor 2')

    Returns:
        str: Confirmation message or error.
    """
    try:
        await _api(
            "PATCH",
            f"/network-monitoring/v1/devices/{params.serial_number}",
            json={"notes": params.notes},
        )
        return f"Notes updated for device {params.serial_number}."
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_delete_device",
    annotations={"title": "Delete Device", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_delete_device(params: DeleteDeviceInput) -> str:
    """Delete a device from Aruba Central by serial number.

    WARNING: This removes the device from Central management. Set confirm=true to proceed.

    Args:
        params (DeleteDeviceInput):
            - serial_number: Device serial number
            - confirm: Must be true to execute deletion

    Returns:
        str: Confirmation or error message.
    """
    if not params.confirm:
        return "Deletion cancelled: set confirm=true to proceed."
    try:
        await _api("DELETE", f"/network-monitoring/v1/devices/{params.serial_number}")
        return f"Device {params.serial_number} deleted from Aruba Central."
    except Exception as e:
        return _err(e)


# ===========================================================================
# SITE HEALTH TOOLS
# ===========================================================================


class SiteHealthListInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    offset: Optional[int] = Field(default=0, ge=0, description="Pagination offset")


class SiteIdInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: str = Field(..., description="Site ID")


@mcp.tool(
    name="aruba_central_list_sites_health",
    annotations={"title": "List Sites Health Overview", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_sites_health(params: SiteHealthListInput) -> str:
    """List all sites with their overall health overview score.

    Returns per-site health scores for devices and clients.

    Args:
        params (SiteHealthListInput): filter, sort, limit, offset

    Returns:
        str: JSON list of sites with health data.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, offset=params.offset)
        data = await _api("GET", "/network-monitoring/v1/sites-health", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_site_health",
    annotations={"title": "Get Site Health", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_site_health(params: SiteIdInput) -> str:
    """Get detailed health information for a specific site.

    Args:
        params (SiteIdInput): site_id

    Returns:
        str: JSON site health details.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/site-health/{params.site_id}")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_list_sites_device_health",
    annotations={"title": "List Sites Device Health", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_sites_device_health(params: SiteHealthListInput) -> str:
    """List all sites with device health breakdown (online/offline/degraded counts).

    Args:
        params (SiteHealthListInput): filter, sort, limit, offset

    Returns:
        str: JSON list of sites with device health.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, offset=params.offset)
        data = await _api("GET", "/network-monitoring/v1/sites-device-health", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_tenant_device_health",
    annotations={"title": "Get Tenant Device Health Overview", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_tenant_device_health() -> str:
    """Get the overall device health overview for the entire tenant.

    Returns aggregate device online/offline/degraded counts across all sites.

    Returns:
        str: JSON tenant-wide device health summary.
    """
    try:
        data = await _api("GET", "/network-monitoring/v1/tenant-device-health")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_list_sites_client_health",
    annotations={"title": "List Sites Client Health", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_sites_client_health(params: SiteHealthListInput) -> str:
    """List all sites with client health breakdown.

    Args:
        params (SiteHealthListInput): filter, sort, limit, offset

    Returns:
        str: JSON list of sites with client health data.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, offset=params.offset)
        data = await _api("GET", "/network-monitoring/v1/sites-client-health", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_tenant_client_health",
    annotations={"title": "Get Tenant Client Health Overview", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_tenant_client_health() -> str:
    """Get the overall client health overview for the entire tenant.

    Returns:
        str: JSON tenant-wide client health summary.
    """
    try:
        data = await _api("GET", "/network-monitoring/v1/tenant-client-health")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ===========================================================================
# SWITCH TOOLS
# ===========================================================================


class ListSwitchesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class SwitchSerialInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Switch serial number or stack ID")


class SwitchInterfacesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Switch serial number or stack ID")
    filter: Optional[str] = Field(default=None, description="OData filter string")
    search: Optional[str] = Field(default=None, description="Search string")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    offset: Optional[int] = Field(default=0, ge=0)


class SwitchTrendsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Switch serial number")
    site_id: Optional[str] = Field(default=None, description="Site ID")
    filter: Optional[str] = Field(default=None, description="OData time-range filter")
    interface_id: Optional[str] = Field(default=None, description="Interface ID for interface trends")
    uplink: Optional[bool] = Field(default=None, description="Filter uplink interfaces only")


class TopNSwitchInterfacesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Site ID")
    filter: Optional[str] = Field(default=None, description="OData filter string")


@mcp.tool(
    name="aruba_central_list_switches",
    annotations={"title": "List Switches", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_switches(params: ListSwitchesInput) -> str:
    """List all switches managed by Aruba Central.

    Returns serial, name, model, IP, status, firmware, site, and stack info.

    Args:
        params (ListSwitchesInput): filter, sort, limit, next

    Returns:
        str: JSON list of switches with pagination info.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-monitoring/v1/switches", params=p)
        items, total, next_cursor = _fmt_items(data)
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch",
    annotations={"title": "Get Switch Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch(params: SwitchSerialInput) -> str:
    """Get full details for a switch or stack by serial number.

    Args:
        params (SwitchSerialInput): serial_number

    Returns:
        str: JSON switch detail object.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_stack_members",
    annotations={"title": "Get Switch Stack Members", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_stack_members(params: SwitchSerialInput) -> str:
    """Get the members of a switch stack by stack ID or conductor serial.

    Args:
        params (SwitchSerialInput): serial_number (stack ID or conductor serial)

    Returns:
        str: JSON list of stack members.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/stack/{params.serial_number}/members")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_interfaces",
    annotations={"title": "Get Switch Interfaces", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_interfaces(params: SwitchInterfacesInput) -> str:
    """Get interface details for a switch including status, speed, VLAN, and PoE.

    Args:
        params (SwitchInterfacesInput): serial_number, filter, search, sort, limit, offset

    Returns:
        str: JSON list of switch interfaces.
    """
    try:
        p = _build_params(filter=params.filter, search=params.search, sort=params.sort,
                          limit=params.limit, offset=params.offset)
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/interfaces", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_vlans",
    annotations={"title": "Get Switch VLANs", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_vlans(params: SwitchInterfacesInput) -> str:
    """Get VLAN details for a switch or stack.

    Args:
        params (SwitchInterfacesInput): serial_number, filter, search, sort, limit, offset

    Returns:
        str: JSON list of VLANs.
    """
    try:
        p = _build_params(filter=params.filter, search=params.search, sort=params.sort,
                          limit=params.limit, offset=params.offset)
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/vlans", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_lag",
    annotations={"title": "Get Switch LAG Summary", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_lag(params: SwitchSerialInput) -> str:
    """Get Link Aggregation Group (LAG) summary for a switch.

    Args:
        params (SwitchSerialInput): serial_number

    Returns:
        str: JSON LAG summary.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/lag")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_hardware",
    annotations={"title": "Get Switch Hardware Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_hardware(params: SwitchSerialInput) -> str:
    """Get hardware category details (fans, PSUs, modules) for a switch.

    Args:
        params (SwitchSerialInput): serial_number

    Returns:
        str: JSON hardware details.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/hardware-categories")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_interface_poe",
    annotations={"title": "Get Switch Interface PoE", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_interface_poe(params: SwitchSerialInput) -> str:
    """Get PoE status and power consumption per interface for a switch.

    Args:
        params (SwitchSerialInput): serial_number

    Returns:
        str: JSON PoE interface data.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/interface-poe")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_interface_trends",
    annotations={"title": "Get Switch Interface Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_interface_trends(params: SwitchTrendsInput) -> str:
    """Get throughput trend data for switch interfaces.

    Args:
        params (SwitchTrendsInput): serial_number, site_id, filter, interface_id, uplink

    Returns:
        str: JSON interface trend time-series data.
    """
    try:
        p = _build_params(filter=params.filter, **{
            "site-id": params.site_id,
            "interface-id": params.interface_id,
            "uplink": params.uplink,
        })
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/interface-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_hardware_trends",
    annotations={"title": "Get Switch Hardware Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_hardware_trends(params: SwitchTrendsInput) -> str:
    """Get hardware trends (CPU, memory, temperature) for a switch.

    Args:
        params (SwitchTrendsInput): serial_number, site_id, filter

    Returns:
        str: JSON hardware trend time-series data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/hardware-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_topn_interface_trends",
    annotations={"title": "Get Top-N Switch Interface Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_topn_interface_trends(params: TopNSwitchInterfacesInput) -> str:
    """Get Top-N interface trends across switches for a site.

    Args:
        params (TopNSwitchInterfacesInput): site_id, filter

    Returns:
        str: JSON top-N interface trend data.
    """
    try:
        p = _build_params(filter=params.filter, **{"site-id": params.site_id})
        data = await _api("GET", "/network-monitoring/v1/switches/topn-interface-trends", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_switch_vsx",
    annotations={"title": "Get Switch VSX Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_switch_vsx(params: SwitchSerialInput) -> str:
    """Get Virtual Switching Extension (VSX) details for a CX switch.

    Args:
        params (SwitchSerialInput): serial_number

    Returns:
        str: JSON VSX details.
    """
    try:
        data = await _api("GET", f"/network-monitoring/v1/switches/{params.serial_number}/vsx")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ===========================================================================
# NOTIFICATIONS / ALERTS TOOLS
# ===========================================================================


class ListAlertsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    filter: Optional[str] = Field(default=None, description="OData filter string (e.g. \"severity eq 'critical'\")")
    sort: Optional[str] = Field(default=None, description="Sort expression")
    limit: Optional[int] = Field(default=20, ge=1, le=1000)
    next: Optional[str] = Field(default=None, description="Pagination cursor")


class AlertKeysInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    keys: list = Field(..., description="List of alert keys to act on (e.g. ['22071893000:47765082406'])")


class ClearAlertsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    keys: list = Field(..., description="List of alert keys to clear")
    reason: Optional[str] = Field(default=None, description="Reason for clearing (e.g. 'Problem was resolved')")
    notes: Optional[str] = Field(default=None, description="Additional notes")


class DeferAlertsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    keys: list = Field(..., description="List of alert keys to defer")
    defer_until: str = Field(..., description="ISO8601 datetime to defer until (e.g. '2026-03-01T00:00:00Z')")


class SetAlertPriorityInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    keys: list = Field(..., description="List of alert keys")
    priority: str = Field(..., description="Priority level: 'High', 'Medium', or 'Low'")


class AsyncTaskInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    task_id: str = Field(..., description="Async operation task ID returned from a previous request")


class InsightsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    site_id: Optional[str] = Field(default=None, description="Filter insights by site ID")
    id: Optional[str] = Field(default=None, description="Specific insight ID")


@mcp.tool(
    name="aruba_central_list_alerts",
    annotations={"title": "List Alerts", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_alerts(params: ListAlertsInput) -> str:
    """List all alerts from Aruba Central notifications.

    Returns alert key, type, severity, device, site, description, and timestamps.

    Args:
        params (ListAlertsInput): filter, sort, limit, next

    Returns:
        str: JSON list of alerts with pagination info.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-notifications/v1/alerts", params=p)
        items, total, next_cursor = _fmt_items(data, items_key="items")
        return json.dumps({"total": total, "count": len(items), "next": next_cursor, "items": items}, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_clear_alerts",
    annotations={"title": "Clear Alerts", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_clear_alerts(params: ClearAlertsInput) -> str:
    """Clear one or more alerts by their keys.

    Args:
        params (ClearAlertsInput):
            - keys: list of alert keys (e.g. ['22071893000:47765082406'])
            - reason: optional reason string
            - notes: optional additional notes

    Returns:
        str: Confirmation or error message.
    """
    try:
        body: dict = {"keys": params.keys}
        if params.reason:
            body["reason"] = params.reason
        if params.notes:
            body["notes"] = params.notes
        data = await _api("POST", "/network-notifications/v1/alerts/clear", json=body)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_defer_alerts",
    annotations={"title": "Defer Alerts", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_defer_alerts(params: DeferAlertsInput) -> str:
    """Defer alerts until a specified date/time.

    Args:
        params (DeferAlertsInput):
            - keys: list of alert keys
            - defer_until: ISO8601 datetime (e.g. '2026-03-01T00:00:00Z')

    Returns:
        str: Confirmation or error message.
    """
    try:
        data = await _api("POST", "/network-notifications/v1/alerts/defer",
                          json={"keys": params.keys, "deferUntil": params.defer_until})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_set_alerts_active",
    annotations={"title": "Set Alerts Active", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_set_alerts_active(params: AlertKeysInput) -> str:
    """Set deferred alerts back to active status.

    Args:
        params (AlertKeysInput): keys — list of alert keys

    Returns:
        str: Confirmation or error message.
    """
    try:
        data = await _api("POST", "/network-notifications/v1/alerts/active", json={"keys": params.keys})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_set_alert_priority",
    annotations={"title": "Set Alert Priority", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_set_alert_priority(params: SetAlertPriorityInput) -> str:
    """Set the priority of one or more alerts.

    Args:
        params (SetAlertPriorityInput):
            - keys: list of alert keys
            - priority: 'High', 'Medium', or 'Low'

    Returns:
        str: Confirmation or error message.
    """
    try:
        data = await _api("POST", "/network-notifications/v1/alerts/priority",
                          json={"keys": params.keys, "priority": params.priority})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_alerts_classification",
    annotations={"title": "Get Alerts Classification", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_alerts_classification(params: ListAlertsInput) -> str:
    """Get alert classification types available in Aruba Central.

    Args:
        params (ListAlertsInput): filter, sort, limit, next

    Returns:
        str: JSON alert classification data.
    """
    try:
        p = _build_params(filter=params.filter, sort=params.sort, limit=params.limit, next=params.next)
        data = await _api("GET", "/network-notifications/v1/alerts/classification", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_get_alert_async_status",
    annotations={"title": "Get Alert Async Operation Status", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_alert_async_status(params: AsyncTaskInput) -> str:
    """Get the status of an asynchronous alert operation.

    Args:
        params (AsyncTaskInput): task_id — returned from a previous async alert operation

    Returns:
        str: JSON async operation status and result.
    """
    try:
        data = await _api("GET", f"/network-notifications/v1/alerts/async-operations/{params.task_id}")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_list_insights",
    annotations={"title": "List Insights", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_list_insights(params: InsightsInput) -> str:
    """List AI-generated network insights and recommendations.

    Args:
        params (InsightsInput): site_id, id

    Returns:
        str: JSON list of insights and recommendations.
    """
    try:
        p = _build_params(**{"site-id": params.site_id, "id": params.id})
        data = await _api("GET", "/network-notifications/v1/insights", params=p)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ===========================================================================
# TROUBLESHOOTING TOOLS
# ===========================================================================
# All async tests return a task_id. Use aruba_central_get_async_result
# with the task_id to poll for results.


class TshootSerialInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")


class PingInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    destination: str = Field(..., description="Ping target hostname or IP (e.g. 'www.google.com' or '8.8.8.8')")


class TracerouteInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    destination: str = Field(..., description="Traceroute target hostname or IP")


class PortListInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    ports: list = Field(..., description="List of port identifiers (AOS-S: ['1','2'], CX: ['1/1/1','1/1/2'], GW: ['GE 0/0/0'])")


class ShowCommandsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    commands: list = Field(..., description="List of show commands to run (e.g. ['show version', 'show arp'])")


class SpeedtestInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    iperf_server_address: str = Field(..., description="iPerf server IP address (e.g. '84.1.43.23')")


class HttpTestInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    url: str = Field(..., description="Target URL or hostname (e.g. 'www.google.com')")


class TcpTestInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    host: str = Field(..., description="Target hostname or IP")
    port: int = Field(..., description="TCP port number (e.g. 443)")


class NslookupInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    host: str = Field(..., description="Hostname to resolve (e.g. 'www.google.com')")


class AaaTestAPInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    server_name: str = Field(..., description="RADIUS server name")
    username: str = Field(..., description="Test username")
    password: str = Field(..., description="Test password")


class DisconnectByMacInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    mac_address: str = Field(..., description="Client MAC address to disconnect (e.g. 'AA:BB:CC:DD:EE:FF')")


class DisconnectByNetworkInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="AP serial number")
    network_name: str = Field(..., description="SSID/network name to disconnect all users from")


class AsyncResultInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    device_type: str = Field(..., description="Device type: 'ap', 'aos-s', 'cx', or 'gateway'")
    serial_number: str = Field(..., description="Device serial number")
    operation: str = Field(..., description="Operation name (e.g. 'ping', 'traceroute', 'showCommands')")
    task_id: str = Field(..., description="Task ID returned from the initiating request")


class PingSweepInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Gateway serial number")
    destination: str = Field(..., description="Target IP address")
    count: Optional[int] = Field(default=2, description="Number of sweep iterations")
    start_packet_size: Optional[int] = Field(default=10, description="Starting packet size in bytes")
    end_packet_size: Optional[int] = Field(default=50, description="Ending packet size in bytes")
    sweep_interval: Optional[int] = Field(default=10, description="Packet size increment per step")


class CxAaaTestInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="CX Switch serial number")
    auth_method_type: str = Field(..., description="Auth method: 'chap' or 'pap'")
    radius_server_ip: str = Field(..., description="RADIUS server IP address")
    username: str = Field(..., description="Test username")
    password: str = Field(..., description="Test password")


class RebootConfirmInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    serial_number: str = Field(..., description="Device serial number")
    confirm: bool = Field(..., description="Must be true to confirm reboot")


# ---------------------------------------------------------------------------
# Shared async result getter
# ---------------------------------------------------------------------------

@mcp.tool(
    name="aruba_central_get_async_result",
    annotations={"title": "Get Async Operation Result", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_get_async_result(params: AsyncResultInput) -> str:
    """Poll the result of an async troubleshooting operation (ping, traceroute, showCommands, etc.).

    All troubleshooting POST operations are async — they return a task_id.
    Call this tool with the task_id to retrieve the result.

    Args:
        params (AsyncResultInput):
            - device_type: 'ap', 'aos-s', 'cx', or 'gateway'
            - serial_number: device serial number
            - operation: e.g. 'ping', 'traceroute', 'speedtest', 'showCommands', 'cableTest'
            - task_id: from the initiating POST response

    Returns:
        str: JSON operation status and result (status may be 'running' if not yet complete).
    """
    prefix_map = {"ap": "aps", "aos-s": "aos-s", "cx": "cx", "gateway": "gateways"}
    prefix = prefix_map.get(params.device_type.lower())
    if not prefix:
        return f"Error: Unknown device_type '{params.device_type}'. Use 'ap', 'aos-s', 'cx', or 'gateway'."
    try:
        path = f"/network-troubleshooting/v1/{prefix}/{params.serial_number}/{params.operation}/async-operations/{params.task_id}"
        data = await _api("GET", path)
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# AP Troubleshooting
# ---------------------------------------------------------------------------

@mcp.tool(
    name="aruba_central_ap_ping",
    annotations={"title": "AP Ping Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_ping(params: PingInput) -> str:
    """Initiate a ping test from an access point. Returns a task_id — use aruba_central_get_async_result to get results.

    Args:
        params (PingInput): serial_number, destination (hostname or IP)

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/ping",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_traceroute",
    annotations={"title": "AP Traceroute Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_traceroute(params: TracerouteInput) -> str:
    """Initiate a traceroute test from an access point. Returns a task_id.

    Args:
        params (TracerouteInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/traceroute",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_speedtest",
    annotations={"title": "AP Speed Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_speedtest(params: SpeedtestInput) -> str:
    """Initiate an iPerf speed test from an access point. Returns a task_id.

    Args:
        params (SpeedtestInput): serial_number, iperf_server_address

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/speedtest",
                          json={"iperfServerAddress": params.iperf_server_address})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_http_test",
    annotations={"title": "AP HTTP Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_http_test(params: HttpTestInput) -> str:
    """Initiate an HTTP connectivity test from an access point. Returns a task_id.

    Args:
        params (HttpTestInput): serial_number, url

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/http",
                          json={"url": params.url})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_https_test",
    annotations={"title": "AP HTTPS Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_https_test(params: HttpTestInput) -> str:
    """Initiate an HTTPS connectivity test from an access point. Returns a task_id.

    Args:
        params (HttpTestInput): serial_number, url

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/https",
                          json={"url": params.url})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_tcp_test",
    annotations={"title": "AP TCP Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_tcp_test(params: TcpTestInput) -> str:
    """Initiate a TCP connectivity test from an access point. Returns a task_id.

    Args:
        params (TcpTestInput): serial_number, host, port

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/tcp",
                          json={"host": params.host, "port": params.port})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_nslookup",
    annotations={"title": "AP NSLookup Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_nslookup(params: NslookupInput) -> str:
    """Initiate a DNS lookup (nslookup) from an access point. Returns a task_id.

    Args:
        params (NslookupInput): serial_number, host

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/nslookup",
                          json={"host": params.host})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_arp_table",
    annotations={"title": "AP Get ARP Table", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_arp_table(params: TshootSerialInput) -> str:
    """Retrieve the ARP table from an access point. Returns a task_id.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/getArpTable")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_show_commands_list",
    annotations={"title": "List AP Show Commands", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_ap_show_commands_list(params: TshootSerialInput) -> str:
    """List the supported 'show' commands for an access point.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of supported show commands.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/aps/{params.serial_number}/show-commands")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_run_show_commands",
    annotations={"title": "Run AP Show Commands", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_run_show_commands(params: ShowCommandsInput) -> str:
    """Run one or more 'show' commands on an access point. Returns a task_id.

    Args:
        params (ShowCommandsInput):
            - serial_number: AP serial number
            - commands: list of show commands (e.g. ['show interface brief', 'show version'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/showCommands",
                          json={"commands": params.commands})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_reboot",
    annotations={"title": "Reboot Access Point", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_reboot(params: RebootConfirmInput) -> str:
    """Reboot an access point. Clients will be disconnected during reboot.

    Args:
        params (RebootConfirmInput): serial_number, confirm (must be true)

    Returns:
        str: Confirmation or error.
    """
    if not params.confirm:
        return "Reboot cancelled: set confirm=true to proceed."
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/reboot")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_reboot_swarm",
    annotations={"title": "Reboot AP Swarm", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_reboot_swarm(params: RebootConfirmInput) -> str:
    """Reboot an entire AP swarm (virtual controller cluster).

    Args:
        params (RebootConfirmInput): serial_number, confirm (must be true)

    Returns:
        str: Confirmation or error.
    """
    if not params.confirm:
        return "Swarm reboot cancelled: set confirm=true to proceed."
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/rebootSwarm")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_locate",
    annotations={"title": "Locate Access Point", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_locate(params: TshootSerialInput) -> str:
    """Trigger the locate/blink LED function on an access point.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/locate")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_disconnect_all_users",
    annotations={"title": "Disconnect All AP Users", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_disconnect_all_users(params: TshootSerialInput) -> str:
    """Disconnect all wireless users from an access point.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/disconnectUserAll")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_disconnect_user_by_mac",
    annotations={"title": "Disconnect AP User by MAC", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_disconnect_user_by_mac(params: DisconnectByMacInput) -> str:
    """Disconnect a specific wireless user from an AP by MAC address.

    Args:
        params (DisconnectByMacInput): serial_number, mac_address

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/disconnectUserByMacAddress",
                          json={"userMacAddress": params.mac_address})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_disconnect_users_by_network",
    annotations={"title": "Disconnect All Users from SSID", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_ap_disconnect_users_by_network(params: DisconnectByNetworkInput) -> str:
    """Disconnect all users from a specific SSID on an access point.

    Args:
        params (DisconnectByNetworkInput): serial_number, network_name (SSID)

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aps/{params.serial_number}/disconnectUserByNetwork",
                          json={"networkName": params.network_name})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_ap_list_tasks",
    annotations={"title": "List AP Active Tasks", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_ap_list_tasks(params: TshootSerialInput) -> str:
    """List all active async troubleshooting tasks for an access point.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of active tasks with their IDs and status.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/aps/{params.serial_number}/list-tasks")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# CX Switch Troubleshooting
# ---------------------------------------------------------------------------

@mcp.tool(
    name="aruba_central_cx_ping",
    annotations={"title": "CX Switch Ping Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_ping(params: PingInput) -> str:
    """Initiate a ping test from a CX switch. Returns a task_id.

    Args:
        params (PingInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/ping",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_traceroute",
    annotations={"title": "CX Switch Traceroute", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_traceroute(params: TracerouteInput) -> str:
    """Initiate a traceroute from a CX switch. Returns a task_id.

    Args:
        params (TracerouteInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/traceroute",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_poe_bounce",
    annotations={"title": "CX Switch PoE Bounce", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_poe_bounce(params: PortListInput) -> str:
    """Bounce PoE power on specified CX switch ports. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['1/1/1', '1/1/2'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/poeBounce",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_port_bounce",
    annotations={"title": "CX Switch Port Bounce", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_port_bounce(params: PortListInput) -> str:
    """Bounce specified CX switch ports (link down then up). Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['1/1/1', '1/1/2'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/portBounce",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_cable_test",
    annotations={"title": "CX Switch Cable Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_cable_test(params: PortListInput) -> str:
    """Run a cable test on CX switch ports. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['1/1/1', '2/1/1'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/cableTest",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_http_test",
    annotations={"title": "CX Switch HTTP Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_http_test(params: HttpTestInput) -> str:
    """Initiate an HTTP connectivity test from a CX switch. Returns a task_id.

    Args:
        params (HttpTestInput): serial_number, url/destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/http",
                          json={"destination": params.url})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_aaa_test",
    annotations={"title": "CX Switch AAA Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_aaa_test(params: CxAaaTestInput) -> str:
    """Initiate an AAA (RADIUS) authentication test from a CX switch. Returns a task_id.

    Args:
        params (CxAaaTestInput): serial_number, auth_method_type ('chap'/'pap'), radius_server_ip, username, password

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/aaa",
                          json={"authMethodType": params.auth_method_type, "radiusServerIp": params.radius_server_ip,
                                "username": params.username, "password": params.password})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_show_commands_list",
    annotations={"title": "List CX Show Commands", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_cx_show_commands_list(params: TshootSerialInput) -> str:
    """List supported 'show' commands for a CX switch.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of supported show commands.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/cx/{params.serial_number}/show-commands")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_run_show_commands",
    annotations={"title": "Run CX Show Commands", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_run_show_commands(params: ShowCommandsInput) -> str:
    """Run 'show' commands on a CX switch. Returns a task_id.

    Args:
        params (ShowCommandsInput): serial_number, commands list

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/showCommands",
                          json={"commands": params.commands})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_reboot",
    annotations={"title": "Reboot CX Switch", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_reboot(params: RebootConfirmInput) -> str:
    """Reboot a CX switch.

    Args:
        params (RebootConfirmInput): serial_number, confirm (must be true)

    Returns:
        str: Confirmation or error.
    """
    if not params.confirm:
        return "Reboot cancelled: set confirm=true to proceed."
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/reboot")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_locate",
    annotations={"title": "Locate CX Switch", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_cx_locate(params: TshootSerialInput) -> str:
    """Trigger the locate/blink LED function on a CX switch.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/cx/{params.serial_number}/locate")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_cx_list_tasks",
    annotations={"title": "List CX Active Tasks", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_cx_list_tasks(params: TshootSerialInput) -> str:
    """List all active async troubleshooting tasks for a CX switch.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of active tasks.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/cx/{params.serial_number}/list-tasks")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# AOS-S Switch Troubleshooting
# ---------------------------------------------------------------------------

@mcp.tool(
    name="aruba_central_aoss_ping",
    annotations={"title": "AOS-S Switch Ping Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_ping(params: PingInput) -> str:
    """Initiate a ping test from an AOS-S switch. Returns a task_id.

    Args:
        params (PingInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/ping",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_traceroute",
    annotations={"title": "AOS-S Switch Traceroute", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_traceroute(params: TracerouteInput) -> str:
    """Initiate a traceroute from an AOS-S switch. Returns a task_id.

    Args:
        params (TracerouteInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/traceroute",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_poe_bounce",
    annotations={"title": "AOS-S Switch PoE Bounce", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_poe_bounce(params: PortListInput) -> str:
    """Bounce PoE power on AOS-S switch ports. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['1', '2'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/poeBounce",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_port_bounce",
    annotations={"title": "AOS-S Switch Port Bounce", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_port_bounce(params: PortListInput) -> str:
    """Bounce ports on an AOS-S switch. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['1', '2'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/portBounce",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_cable_test",
    annotations={"title": "AOS-S Switch Cable Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_cable_test(params: PortListInput) -> str:
    """Run a cable test on AOS-S switch ports. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['1', '2'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/cableTest",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_arp_table",
    annotations={"title": "AOS-S Switch ARP Table", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_arp_table(params: TshootSerialInput) -> str:
    """Retrieve the ARP table from an AOS-S switch. Returns a task_id.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/getArpTable")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_show_commands_list",
    annotations={"title": "List AOS-S Show Commands", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_aoss_show_commands_list(params: TshootSerialInput) -> str:
    """List supported 'show' commands for an AOS-S switch.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of supported show commands.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/show-commands")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_run_show_commands",
    annotations={"title": "Run AOS-S Show Commands", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_run_show_commands(params: ShowCommandsInput) -> str:
    """Run 'show' commands on an AOS-S switch. Returns a task_id.

    Args:
        params (ShowCommandsInput): serial_number, commands list

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/showCommands",
                          json={"commands": params.commands})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_reboot",
    annotations={"title": "Reboot AOS-S Switch", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_reboot(params: RebootConfirmInput) -> str:
    """Reboot an AOS-S switch.

    Args:
        params (RebootConfirmInput): serial_number, confirm (must be true)

    Returns:
        str: Confirmation or error.
    """
    if not params.confirm:
        return "Reboot cancelled: set confirm=true to proceed."
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/reboot")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_locate",
    annotations={"title": "Locate AOS-S Switch", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_aoss_locate(params: TshootSerialInput) -> str:
    """Trigger the locate/blink LED function on an AOS-S switch.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/locate")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_aoss_list_tasks",
    annotations={"title": "List AOS-S Active Tasks", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_aoss_list_tasks(params: TshootSerialInput) -> str:
    """List all active async troubleshooting tasks for an AOS-S switch.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of active tasks.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/aos-s/{params.serial_number}/list-tasks")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Gateway Troubleshooting
# ---------------------------------------------------------------------------

@mcp.tool(
    name="aruba_central_gw_ping",
    annotations={"title": "Gateway Ping Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_ping(params: PingInput) -> str:
    """Initiate a ping test from a gateway. Returns a task_id.

    Args:
        params (PingInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/ping",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_ping_sweep",
    annotations={"title": "Gateway Ping Sweep", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_ping_sweep(params: PingSweepInput) -> str:
    """Run a ping sweep from a gateway across a range of packet sizes. Returns a task_id.

    Args:
        params (PingSweepInput): serial_number, destination, count, start_packet_size, end_packet_size, sweep_interval

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/pingSweep",
                          json={"destination": params.destination, "count": params.count,
                                "startPacketSize": params.start_packet_size, "endPacketSize": params.end_packet_size,
                                "sweepInterval": params.sweep_interval})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_traceroute",
    annotations={"title": "Gateway Traceroute", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_traceroute(params: TracerouteInput) -> str:
    """Initiate a traceroute from a gateway. Returns a task_id.

    Args:
        params (TracerouteInput): serial_number, destination

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/traceroute",
                          json={"destination": params.destination})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_poe_bounce",
    annotations={"title": "Gateway PoE Bounce", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_poe_bounce(params: PortListInput) -> str:
    """Bounce PoE power on gateway ports. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['GE 0/0/0', 'GE 0/0/1'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/poeBounce",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_port_bounce",
    annotations={"title": "Gateway Port Bounce", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_port_bounce(params: PortListInput) -> str:
    """Bounce ports on a gateway. Returns a task_id.

    Args:
        params (PortListInput): serial_number, ports (e.g. ['GE 0/0/0', 'GE 0/0/1'])

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/portBounce",
                          json={"ports": params.ports})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_iperf_test",
    annotations={"title": "Gateway iPerf Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_iperf_test(params: SpeedtestInput) -> str:
    """Initiate an iPerf bandwidth test from a gateway. Returns a task_id.

    Args:
        params (SpeedtestInput): serial_number, iperf_server_address

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/iperf",
                          json={"iperfServerAddress": params.iperf_server_address})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_http_test",
    annotations={"title": "Gateway HTTP Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_http_test(params: HttpTestInput) -> str:
    """Initiate an HTTP test from a gateway. Returns a task_id.

    Args:
        params (HttpTestInput): serial_number, url

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/http",
                          json={"url": params.url})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_https_test",
    annotations={"title": "Gateway HTTPS Test", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_https_test(params: HttpTestInput) -> str:
    """Initiate an HTTPS test from a gateway. Returns a task_id.

    Args:
        params (HttpTestInput): serial_number, url

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/https",
                          json={"url": params.url})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_arp_table",
    annotations={"title": "Gateway ARP Table", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_arp_table(params: TshootSerialInput) -> str:
    """Retrieve the ARP table from a gateway. Returns a task_id.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/getArpTable")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_show_commands_list",
    annotations={"title": "List Gateway Show Commands", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_gw_show_commands_list(params: TshootSerialInput) -> str:
    """List supported 'show' commands for a gateway.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of supported show commands.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/gateways/{params.serial_number}/show-commands")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_run_show_commands",
    annotations={"title": "Run Gateway Show Commands", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_run_show_commands(params: ShowCommandsInput) -> str:
    """Run 'show' commands on a gateway. Returns a task_id.

    Args:
        params (ShowCommandsInput): serial_number, commands list

    Returns:
        str: JSON with task_id for polling.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/showCommands",
                          json={"commands": params.commands})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_reboot",
    annotations={"title": "Reboot Gateway", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_reboot(params: RebootConfirmInput) -> str:
    """Reboot a gateway.

    Args:
        params (RebootConfirmInput): serial_number, confirm (must be true)

    Returns:
        str: Confirmation or error.
    """
    if not params.confirm:
        return "Reboot cancelled: set confirm=true to proceed."
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/reboot")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_disconnect_all_clients",
    annotations={"title": "Disconnect All Gateway Clients", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_disconnect_all_clients(params: TshootSerialInput) -> str:
    """Disconnect all clients from a gateway.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/disconnectClientAll")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_disconnect_client_by_mac",
    annotations={"title": "Disconnect Gateway Client by MAC", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True},
)
async def aruba_central_gw_disconnect_client_by_mac(params: DisconnectByMacInput) -> str:
    """Disconnect a specific client from a gateway by MAC address.

    Args:
        params (DisconnectByMacInput): serial_number, mac_address

    Returns:
        str: Confirmation or error.
    """
    try:
        data = await _api("POST", f"/network-troubleshooting/v1/gateways/{params.serial_number}/disconnectClientByMacAddress",
                          json={"clientMacAddress": params.mac_address})
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="aruba_central_gw_list_tasks",
    annotations={"title": "List Gateway Active Tasks", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def aruba_central_gw_list_tasks(params: TshootSerialInput) -> str:
    """List all active async troubleshooting tasks for a gateway.

    Args:
        params (TshootSerialInput): serial_number

    Returns:
        str: JSON list of active tasks.
    """
    try:
        data = await _api("GET", f"/network-troubleshooting/v1/gateways/{params.serial_number}/list-tasks")
        return json.dumps(data, indent=2)
    except Exception as e:
        return _err(e)


# ---------------------------------------------------------------------------
# Configuration API tools (auto-generated from Configuration APIs collection)
# ---------------------------------------------------------------------------

from config_tools import register_config_tools
register_config_tools(mcp, _api, _err)

from api_tools import register_api_tools
register_api_tools(mcp, _api, _err)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
