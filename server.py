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


# ---------------------------------------------------------------------------
# Configuration & API tools (auto-generated)
# ---------------------------------------------------------------------------

from config_tools import register_config_tools
register_config_tools(mcp, _api, _err)

from api_tools import register_api_tools
register_api_tools(mcp, _api, _err)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    mcp.run()
