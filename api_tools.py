"""
Aruba Central API tools — auto-generated from OpenAPI specs (v26.04).
Covers: Monitoring, Troubleshooting, Services, Notifications, Reporting, MSP.
"""

import json
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP


def register_api_tools(mcp: FastMCP, api_fn, err_fn):
    """Register all non-config API tools from OpenAPI specs."""

    class _M_aruba_central_firewallsessionlogsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="The ID of the site from which to retrieve the firewall session logs. ")
        start_at: str = Field(..., description="The start time for the query in RFC 3339 format, must be less than end-at. ")
        end_at: str = Field(..., description="The end time for the query in RFC 3339 format, must be greater than start-at. ")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        limit: Optional[int] = Field(None, description="The maximum number of items to return. ")
        offset: Optional[int] = Field(None, description="The offset of the item at which to begin the response. ")

    @mcp.tool(name="aruba_central_firewallsessionlogsv1",
              annotations={"title": "Get blocked firewall session logs ", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_firewallsessionlogsv1(params: _M_aruba_central_firewallsessionlogsv1) -> str:
        """Get blocked firewall session logs .

        Spec: monitoring | GET /network-monitoring/v1/site-firewall-sessions
        Query params: site-id, start-at, end-at, filter, limit, offset
        """
        try:
            url = "/network-monitoring/v1/site-firewall-sessions"
            p = {k: v for k, v in {
                "site-id": params.site_id,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "filter": params.filter,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_clientfirewallsessionlogsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="The ID of the site from which to retrieve the firewall session logs. ")
        start_at: str = Field(..., description="The start time for the query in RFC 3339 format, must be less than end-at. ")
        end_at: str = Field(..., description="The end time for the query in RFC 3339 format, must be greater than start-at. ")
        client_mac: str = Field(..., description="The client MAC of the source device. ")
        filter: str = Field(..., description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        limit: Optional[int] = Field(None, description="The maximum number of items to return. ")
        offset: Optional[int] = Field(None, description="The offset of the item at which to begin the response. ")

    @mcp.tool(name="aruba_central_clientfirewallsessionlogsv1",
              annotations={"title": "Get client firewall session logs ", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_clientfirewallsessionlogsv1(params: _M_aruba_central_clientfirewallsessionlogsv1) -> str:
        """Get client firewall session logs .

        Spec: monitoring | GET /network-monitoring/v1/client-firewall-sessions
        Query params: site-id, start-at, end-at, client-mac, filter, limit, offset
        """
        try:
            url = "/network-monitoring/v1/client-firewall-sessions"
            p = {k: v for k, v in {
                "site-id": params.site_id,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "client-mac": params.client_mac,
                "filter": params.filter,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_clientsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="The ID of the site from which to retrieve the firewall session logs. ")
        start_at: str = Field(..., description="The start time for the query in RFC 3339 format, must be less than end-at. ")
        end_at: str = Field(..., description="The end time for the query in RFC 3339 format, must be greater than start-at. ")
        filter: str = Field(..., description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        limit: Optional[int] = Field(None, description="The maximum number of items to return. ")
        offset: Optional[int] = Field(None, description="The offset of the item at which to begin the response. ")

    @mcp.tool(name="aruba_central_clientsv1",
              annotations={"title": "Get clients list ", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_clientsv1(params: _M_aruba_central_clientsv1) -> str:
        """Get clients list .

        Spec: monitoring | GET /network-monitoring/v1/firewall-clients
        Query params: site-id, start-at, end-at, filter, limit, offset
        """
        try:
            url = "/network-monitoring/v1/firewall-clients"
            p = {k: v for k, v in {
                "site-id": params.site_id,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "filter": params.filter,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_applicationsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="The ID of the site from which applications will be retrieved. ")
        client_id: Optional[str] = Field(None, description="The client MAC of the source device. ")
        start_at: str = Field(..., description="The start time in RFC 3339 Format (must be within 7 days of end-at). ")
        end_at: str = Field(..., description="The end time in RFC 3339 Format (must be greater than start-at)")
        limit: int = Field(..., description="limit")
        offset: int = Field(..., description="The offset of the item at which to begin the response. ")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and', 'eq', and 'in' conjunction ('or' and 'not'")
        sort: Optional[str] = Field(None, description="Sort field followed by direction indicator (asc/desc). Supported fields: NAME, CATEGORY, EXPERIENCE, RISK, USAGE, STATE,")

    @mcp.tool(name="aruba_central_applicationsv1",
              annotations={"title": "Get applications accessed in a site ", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_applicationsv1(params: _M_aruba_central_applicationsv1) -> str:
        """Get applications accessed in a site .

        Spec: monitoring | GET /network-monitoring/v1/applications
        Query params: site-id, client-id, start-at, end-at, limit, offset, filter, sort
        """
        try:
            url = "/network-monitoring/v1/applications"
            p = {k: v for k, v in {
                "site-id": params.site_id,
                "client-id": params.client_id,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
                "filter": params.filter,
                "sort": params.sort,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getlinktopology(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")

    @mcp.tool(name="aruba_central_getlinktopology",
              annotations={"title": "Returns topology details for the given site.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getlinktopology(params: _M_aruba_central_getlinktopology) -> str:
        """Returns topology details for the given site..

        Spec: monitoring | GET /network-monitoring/v1/topology/{site-id}
        """
        try:
            url = f"/network-monitoring/v1/topology/{params.site_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getunmanageddevice(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        mac_address: str = Field(..., description="mac-address")
        site_id: str = Field(..., description="ID of the site for which unmanaged device details are requested.")

    @mcp.tool(name="aruba_central_getunmanageddevice",
              annotations={"title": "Returns details for an unmanaged device of a given site.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getunmanageddevice(params: _M_aruba_central_getunmanageddevice) -> str:
        """Returns details for an unmanaged device of a given site..

        Spec: monitoring | GET /network-monitoring/v1/unmanaged-device/{mac-address}
        Query params: site-id
        """
        try:
            url = f"/network-monitoring/v1/unmanaged-device/{params.mac_address}"
            p = {k: v for k, v in {
                "site-id": params.site_id,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getisolatednodes(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")

    @mcp.tool(name="aruba_central_getisolatednodes",
              annotations={"title": "Returns isolated devices for the given site.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getisolatednodes(params: _M_aruba_central_getisolatednodes) -> str:
        """Returns isolated devices for the given site..

        Spec: monitoring | GET /network-monitoring/v1/isolated-devices/{site-id}
        """
        try:
            url = f"/network-monitoring/v1/isolated-devices/{params.site_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getneighbours(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getneighbours",
              annotations={"title": "Returns details of neighbor devices for a given serial number.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getneighbours(params: _M_aruba_central_getneighbours) -> str:
        """Returns details of neighbor devices for a given serial number..

        Spec: monitoring | GET /network-monitoring/v1/neighbours/{serial-number}
        """
        try:
            url = f"/network-monitoring/v1/neighbours/{params.serial_number}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaprfchannelqualityperformancev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        radio_number: str = Field(..., description="radio-number")

    @mcp.tool(name="aruba_central_getaprfchannelqualityperformancev1",
              annotations={"title": "Get channel quality information for a radio", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaprfchannelqualityperformancev1(params: _M_aruba_central_getaprfchannelqualityperformancev1) -> str:
        """Get channel quality information for a radio.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/channel-quality-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/radios/{params.radio_number}/channel-quality-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaprfnoisefloorperformancev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        radio_number: str = Field(..., description="radio-number")

    @mcp.tool(name="aruba_central_getaprfnoisefloorperformancev1",
              annotations={"title": "Get noise floor information for a radio", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaprfnoisefloorperformancev1(params: _M_aruba_central_getaprfnoisefloorperformancev1) -> str:
        """Get noise floor information for a radio.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/noise-floor-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/radios/{params.radio_number}/noise-floor-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaprfframesperformancev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        radio_number: str = Field(..., description="radio-number")

    @mcp.tool(name="aruba_central_getaprfframesperformancev1",
              annotations={"title": "Get transmission information for a radio", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaprfframesperformancev1(params: _M_aruba_central_getaprfframesperformancev1) -> str:
        """Get transmission information for a radio.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/frames-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/radios/{params.radio_number}/frames-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointportlistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getaccesspointportlistv1",
              annotations={"title": "Get a list of Access Point ports", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointportlistv1(params: _M_aruba_central_getaccesspointportlistv1) -> str:
        """Get a list of Access Point ports.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/ports
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/ports"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointportthroughputv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_index: str = Field(..., description="port-index")

    @mcp.tool(name="aruba_central_getaccesspointportthroughputv1",
              annotations={"title": "Get Access Point Port throughput trend.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointportthroughputv1(params: _M_aruba_central_getaccesspointportthroughputv1) -> str:
        """Get Access Point Port throughput trend..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/ports/{params.port_index}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointportframesperformancev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_index: str = Field(..., description="port-index")

    @mcp.tool(name="aruba_central_getaccesspointportframesperformancev1",
              annotations={"title": "Get Access Point Port Frame Trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointportframesperformancev1(params: _M_aruba_central_getaccesspointportframesperformancev1) -> str:
        """Get Access Point Port Frame Trends.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/frames-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/ports/{params.port_index}/frames-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointportcrcperformancev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_index: str = Field(..., description="port-index")

    @mcp.tool(name="aruba_central_getaccesspointportcrcperformancev1",
              annotations={"title": "Get Access Point Port CRC Errors", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointportcrcperformancev1(params: _M_aruba_central_getaccesspointportcrcperformancev1) -> str:
        """Get Access Point Port CRC Errors.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/crc-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/ports/{params.port_index}/crc-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointportcollisionsperformancev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_index: str = Field(..., description="port-index")

    @mcp.tool(name="aruba_central_getaccesspointportcollisionsperformancev1",
              annotations={"title": "Get Access Point Port Collision Error", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointportcollisionsperformancev1(params: _M_aruba_central_getaccesspointportcollisionsperformancev1) -> str:
        """Get Access Point Port Collision Error.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/collisions-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/ports/{params.port_index}/collisions-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointtunnellistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        site_id: Optional[str] = Field(None, description="ID of the Site for which access point tunnel information is requested ")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Specifies the maximum number of tunnels returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  The minimum value: 1 ")

    @mcp.tool(name="aruba_central_getaccesspointtunnellistv1",
              annotations={"title": "Get a list of Access Point Tunnels", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointtunnellistv1(params: _M_aruba_central_getaccesspointtunnellistv1) -> str:
        """Get a list of Access Point Tunnels.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels
        Query params: site-id, filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels"
            p = {k: v for k, v in {
                "site-id": params.site_id,
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointtunneldetailv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_id: str = Field(..., description="tunnel-id")

    @mcp.tool(name="aruba_central_getaccesspointtunneldetailv1",
              annotations={"title": "Get an Access Point Tunnel details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointtunneldetailv1(params: _M_aruba_central_getaccesspointtunneldetailv1) -> str:
        """Get an Access Point Tunnel details.

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels/{params.tunnel_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointtunnelthroughputv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_id: str = Field(..., description="tunnel-id")

    @mcp.tool(name="aruba_central_getaccesspointtunnelthroughputv1",
              annotations={"title": "Get throughput trend of an Access Point Tunnel.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointtunnelthroughputv1(params: _M_aruba_central_getaccesspointtunnelthroughputv1) -> str:
        """Get throughput trend of an Access Point Tunnel..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels/{params.tunnel_id}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointprobelosstrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_id: str = Field(..., description="tunnel-id")

    @mcp.tool(name="aruba_central_getaccesspointprobelosstrendv1",
              annotations={"title": "Get packet loss trend of an Access Point Tunnel.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointprobelosstrendv1(params: _M_aruba_central_getaccesspointprobelosstrendv1) -> str:
        """Get packet loss trend of an Access Point Tunnel..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/packet-loss-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels/{params.tunnel_id}/packet-loss-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointprobemostrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_id: str = Field(..., description="tunnel-id")

    @mcp.tool(name="aruba_central_getaccesspointprobemostrendv1",
              annotations={"title": "Get MOS score trend of an Access Point Tunnel.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointprobemostrendv1(params: _M_aruba_central_getaccesspointprobemostrendv1) -> str:
        """Get MOS score trend of an Access Point Tunnel..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/mos-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels/{params.tunnel_id}/mos-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointprobejittertrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_id: str = Field(..., description="tunnel-id")

    @mcp.tool(name="aruba_central_getaccesspointprobejittertrendv1",
              annotations={"title": "Get jitter trend of an Access Point Tunnel.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointprobejittertrendv1(params: _M_aruba_central_getaccesspointprobejittertrendv1) -> str:
        """Get jitter trend of an Access Point Tunnel..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/jitter-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels/{params.tunnel_id}/jitter-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointprobelatencytrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_id: str = Field(..., description="tunnel-id")

    @mcp.tool(name="aruba_central_getaccesspointprobelatencytrendv1",
              annotations={"title": "Get latency trend of an Access Point Tunnel.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointprobelatencytrendv1(params: _M_aruba_central_getaccesspointprobelatencytrendv1) -> str:
        """Get latency trend of an Access Point Tunnel..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/latency-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/tunnels/{params.tunnel_id}/latency-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaccesspointwlanthroughputv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        wlan_name: str = Field(..., description="wlan-name")

    @mcp.tool(name="aruba_central_getaccesspointwlanthroughputv1",
              annotations={"title": "Get the throughput trend for a WLAN of an Access Point.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaccesspointwlanthroughputv1(params: _M_aruba_central_getaccesspointwlanthroughputv1) -> str:
        """Get the throughput trend for a WLAN of an Access Point..

        Spec: monitoring | GET /network-monitoring/v1/aps/{serial-number}/wlans/{wlan-name}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/aps/{params.serial_number}/wlans/{params.wlan_name}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getwlanthroughputtrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        wlan_name: str = Field(..., description="wlan-name")

    @mcp.tool(name="aruba_central_getwlanthroughputtrendv1",
              annotations={"title": "Get the throughput trend for a WLAN.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getwlanthroughputtrendv1(params: _M_aruba_central_getwlanthroughputtrendv1) -> str:
        """Get the throughput trend for a WLAN..

        Spec: monitoring | GET /network-monitoring/v1/wlans/{wlan-name}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/wlans/{params.wlan_name}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getswarmv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_id: str = Field(..., description="cluster-id")

    @mcp.tool(name="aruba_central_getswarmv1",
              annotations={"title": "Get a Swarm details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getswarmv1(params: _M_aruba_central_getswarmv1) -> str:
        """Get a Swarm details.

        Spec: monitoring | GET /network-monitoring/v1/swarms/{cluster-id}
        """
        try:
            url = f"/network-monitoring/v1/swarms/{params.cluster_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getsummaryv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        filter: str = Field(..., description="An OData 4.0 filter can be provided with `floorId` (`in` operator must be used ). ")

    @mcp.tool(name="aruba_central_getsummaryv1",
              annotations={"title": "Site devices summary", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getsummaryv1(params: _M_aruba_central_getsummaryv1) -> str:
        """Site devices summary.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps-summary/{site-id}
        Query params: filter
        """
        try:
            url = f"/network-monitoring/v1/sitemaps-summary/{params.site_id}"
            p = {k: v for k, v in {
                "filter": params.filter,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getplaceddevicesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        filter: str = Field(..., description="An OData 4.0 filter must be provided with at least `floorId` or `buildingId`. Other supported fields are ``types` (`in` ")
        limit: Optional[str] = Field(None, description="limit")
        next: Optional[str] = Field(None, description="next")

    @mcp.tool(name="aruba_central_getplaceddevicesv1",
              annotations={"title": "Retrieves placed devices over the FloorMap", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getplaceddevicesv1(params: _M_aruba_central_getplaceddevicesv1) -> str:
        """Retrieves placed devices over the FloorMap.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/network-devices-deployed
        Query params: filter, limit, next
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-deployed"
            p = {k: v for k, v in {
                "filter": params.filter,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_placedevicesonfloorv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_placedevicesonfloorv1",
              annotations={"title": "Place devices over the FloorMap", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_placedevicesonfloorv1(params: _M_aruba_central_placedevicesonfloorv1) -> str:
        """Place devices over the FloorMap.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-deployed
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-deployed"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_removedevicesonfloorv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_removedevicesonfloorv1",
              annotations={"title": "Remove devices from the FloorMap", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_removedevicesonfloorv1(params: _M_aruba_central_removedevicesonfloorv1) -> str:
        """Remove devices from the FloorMap.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-undeploy
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-undeploy"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getassociateddevicesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        filter: str = Field(..., description="An OData 4.0 filter must be provided with at least `floorId`. Other supported fields are  `types` (`in` operator must be")
        limit: Optional[str] = Field(None, description="limit")
        next: Optional[str] = Field(None, description="next")

    @mcp.tool(name="aruba_central_getassociateddevicesv1",
              annotations={"title": "Retrieves assigned devices", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getassociateddevicesv1(params: _M_aruba_central_getassociateddevicesv1) -> str:
        """Retrieves assigned devices.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/network-devices-assigned
        Query params: filter, limit, next
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-assigned"
            p = {k: v for k, v in {
                "filter": params.filter,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_changedeviceassignmentv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_changedeviceassignmentv1",
              annotations={"title": "Assign/Unassign devices to the FloorPlan", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_changedeviceassignmentv1(params: _M_aruba_central_changedeviceassignmentv1) -> str:
        """Assign/Unassign devices to the FloorPlan.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-assigned
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-assigned"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getplacedplanneddevicesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        filter: str = Field(..., description="OData 4.0 filter must be provided with at least `floorId`. ")
        limit: Optional[str] = Field(None, description="limit")
        next: Optional[str] = Field(None, description="next")

    @mcp.tool(name="aruba_central_getplacedplanneddevicesv1",
              annotations={"title": "Retrieves placed (planned) devices", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getplacedplanneddevicesv1(params: _M_aruba_central_getplacedplanneddevicesv1) -> str:
        """Retrieves placed (planned) devices.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/network-devices-planned
        Query params: filter, limit, next
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-planned"
            p = {k: v for k, v in {
                "filter": params.filter,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_placeplanneddevicesonfloorv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_placeplanneddevicesonfloorv1",
              annotations={"title": "Place planned devices", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_placeplanneddevicesonfloorv1(params: _M_aruba_central_placeplanneddevicesonfloorv1) -> str:
        """Place planned devices.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-planned
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-planned"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_removeplanneddevicesonfloorv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_removeplanneddevicesonfloorv1",
              annotations={"title": "Remove planned devices on the FloorMap", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_removeplanneddevicesonfloorv1(params: _M_aruba_central_removeplanneddevicesonfloorv1) -> str:
        """Remove planned devices on the FloorMap.

        Spec: monitoring | DELETE /network-monitoring/v1/sitemaps/{site-id}/network-devices-planned
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/network-devices-planned"
            p = {}
            data = await api_fn("DELETE", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcataloguev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_getcataloguev1",
              annotations={"title": "Retrieves  device specification for all models", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcataloguev1(params: _M_aruba_central_getcataloguev1) -> str:
        """Retrieves  device specification for all models.

        Spec: monitoring | GET /network-monitoring/v1/catalogue-aps
        """
        try:
            url = "/network-monitoring/v1/catalogue-aps"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getsites(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        filter: Optional[str] = Field(None, description="An OData 4.0 filter can be provided with `hasFloors` (use `eq` operator, e.g. `hasFloors eq true`). ")
        limit: Optional[str] = Field(None, description="limit")
        offset: Optional[str] = Field(None, description="offset")

    @mcp.tool(name="aruba_central_getsites",
              annotations={"title": "Retrieve sites with floor and without floor information", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getsites(params: _M_aruba_central_getsites) -> str:
        """Retrieve sites with floor and without floor information.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/sites
        Query params: filter, limit, offset
        """
        try:
            url = "/network-monitoring/v1/sitemaps/sites"
            p = {k: v for k, v in {
                "filter": params.filter,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_createfloorv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_createfloorv1",
              annotations={"title": "Create New Floor", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_createfloorv1(params: _M_aruba_central_createfloorv1) -> str:
        """Create New Floor.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/floors
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getfloormapv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")

    @mcp.tool(name="aruba_central_getfloormapv1",
              annotations={"title": "Retrieve FloorMap information", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getfloormapv1(params: _M_aruba_central_getfloormapv1) -> str:
        """Retrieve FloorMap information.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updatefloormapv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updatefloormapv1",
              annotations={"title": "Update FloorMap", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updatefloormapv1(params: _M_aruba_central_updatefloormapv1) -> str:
        """Update FloorMap.

        Spec: monitoring | PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_removefloorv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")

    @mcp.tool(name="aruba_central_removefloorv1",
              annotations={"title": "Remove floor from a building", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_removefloorv1(params: _M_aruba_central_removefloorv1) -> str:
        """Remove floor from a building.

        Spec: monitoring | DELETE /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_scalefloormapv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_scalefloormapv1",
              annotations={"title": "Scale FloorMap", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_scalefloormapv1(params: _M_aruba_central_scalefloormapv1) -> str:
        """Scale FloorMap.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/scale
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/scale"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getfloormapimagev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        raster: bool = Field(..., description="Determines the type of image to retrieve. true: Retrieves a raster image. false: Retrieves actual floormap image")

    @mcp.tool(name="aruba_central_getfloormapimagev1",
              annotations={"title": "Retrieve FloorMap Image", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getfloormapimagev1(params: _M_aruba_central_getfloormapimagev1) -> str:
        """Retrieve FloorMap Image.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/image
        Query params: raster
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/image"
            p = {k: v for k, v in {
                "raster": params.raster,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_replaceimagev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_replaceimagev1",
              annotations={"title": "Update Floor Image", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_replaceimagev1(params: _M_aruba_central_replaceimagev1) -> str:
        """Update Floor Image.

        Spec: monitoring | PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/image
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/image"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getbuildingsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")

    @mcp.tool(name="aruba_central_getbuildingsv1",
              annotations={"title": "Retrieve building information", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getbuildingsv1(params: _M_aruba_central_getbuildingsv1) -> str:
        """Retrieve building information.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/buildings
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/buildings"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updatebuildingv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        building_id: str = Field(..., description="building-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updatebuildingv1",
              annotations={"title": "Update Building", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updatebuildingv1(params: _M_aruba_central_updatebuildingv1) -> str:
        """Update Building.

        Spec: monitoring | PUT /network-monitoring/v1/sitemaps/{site-id}/buildings/{building-id}
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/buildings/{params.building_id}"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_removebuildingv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        building_id: str = Field(..., description="building-id")

    @mcp.tool(name="aruba_central_removebuildingv1",
              annotations={"title": "Remove Building", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_removebuildingv1(params: _M_aruba_central_removebuildingv1) -> str:
        """Remove Building.

        Spec: monitoring | DELETE /network-monitoring/v1/sitemaps/{site-id}/buildings/{building-id}
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/buildings/{params.building_id}"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_importfloorsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_importfloorsv1",
              annotations={"title": "Import FloorPlans using zip file", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_importfloorsv1(params: _M_aruba_central_importfloorsv1) -> str:
        """Import FloorPlans using zip file.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/import
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/import"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getimportstatusv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        id: str = Field(..., description="id")

    @mcp.tool(name="aruba_central_getimportstatusv1",
              annotations={"title": "Retrieve Import Status", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getimportstatusv1(params: _M_aruba_central_getimportstatusv1) -> str:
        """Retrieve Import Status.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/import/{id}
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/import/{params.id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getwalltypesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_getwalltypesv1",
              annotations={"title": "Retrieve Wall Types", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getwalltypesv1(params: _M_aruba_central_getwalltypesv1) -> str:
        """Retrieve Wall Types.

        Spec: monitoring | GET /network-monitoring/v1/wall-types
        """
        try:
            url = "/network-monitoring/v1/wall-types"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_createwalltypesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_createwalltypesv1",
              annotations={"title": "Create Wall Types", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_createwalltypesv1(params: _M_aruba_central_createwalltypesv1) -> str:
        """Create Wall Types.

        Spec: monitoring | POST /network-monitoring/v1/wall-types
        """
        try:
            url = "/network-monitoring/v1/wall-types"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updatewalltypesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updatewalltypesv1",
              annotations={"title": "Update Wall Types", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updatewalltypesv1(params: _M_aruba_central_updatewalltypesv1) -> str:
        """Update Wall Types.

        Spec: monitoring | PUT /network-monitoring/v1/wall-types
        """
        try:
            url = "/network-monitoring/v1/wall-types"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deletewalltypesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_deletewalltypesv1",
              annotations={"title": "Delete Wall Types.", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deletewalltypesv1(params: _M_aruba_central_deletewalltypesv1) -> str:
        """Delete Wall Types..

        Spec: monitoring | DELETE /network-monitoring/v1/wall-types
        """
        try:
            url = "/network-monitoring/v1/wall-types"
            p = {}
            data = await api_fn("DELETE", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getwallsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")

    @mcp.tool(name="aruba_central_getwallsv1",
              annotations={"title": "Retrieve Walls", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getwallsv1(params: _M_aruba_central_getwallsv1) -> str:
        """Retrieve Walls.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/walls"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_createwallsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_createwallsv1",
              annotations={"title": "Create Wall", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_createwallsv1(params: _M_aruba_central_createwallsv1) -> str:
        """Create Wall.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/walls"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updatewallsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updatewallsv1",
              annotations={"title": "Update Walls.", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updatewallsv1(params: _M_aruba_central_updatewallsv1) -> str:
        """Update Walls..

        Spec: monitoring | PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/walls"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deletewallsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_deletewallsv1",
              annotations={"title": "Delete Walls.", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deletewallsv1(params: _M_aruba_central_deletewallsv1) -> str:
        """Delete Walls..

        Spec: monitoring | DELETE /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/walls"
            p = {}
            data = await api_fn("DELETE", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getzonesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")

    @mcp.tool(name="aruba_central_getzonesv1",
              annotations={"title": "Retrieves Zones", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getzonesv1(params: _M_aruba_central_getzonesv1) -> str:
        """Retrieves Zones.

        Spec: monitoring | GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/zones"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_createzonesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_createzonesv1",
              annotations={"title": "Create zone", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_createzonesv1(params: _M_aruba_central_createzonesv1) -> str:
        """Create zone.

        Spec: monitoring | POST /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/zones"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updatezonesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updatezonesv1",
              annotations={"title": "Update zones", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updatezonesv1(params: _M_aruba_central_updatezonesv1) -> str:
        """Update zones.

        Spec: monitoring | PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/zones"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deletezonesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_deletezonesv1",
              annotations={"title": "Delete zones", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deletezonesv1(params: _M_aruba_central_deletezonesv1) -> str:
        """Delete zones.

        Spec: monitoring | DELETE /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
        """
        try:
            url = f"/network-monitoring/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/zones"
            p = {}
            data = await api_fn("DELETE", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclientonboardingscorev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: Optional[str] = Field(None, description="Start timestamp (ISO date format). Must be earlier than end-at. If start-at and end-at are not provided, the default tim")
        end_at: Optional[str] = Field(None, description="End timestamp (ISO date format). Must be later than start-at. If start-at and end-at are not provided, the default time ")
        site_id: Optional[str] = Field(None, description="Optional site identifier. If omitted, tenant-level score is returned.")
        stage: Optional[str] = Field(None, description="Optional onboarding stage. Supported values: `assoc`, `auth`, `dhcp`, `dns`. Omit to get all supported stages.")
        version: Optional[str] = Field(None, description="Optional onboarding events version. If not provided or non-numeric, the service uses a default version.")
        view_type: Optional[str] = Field(None, description="view-type supports DEFAULT, BY_CLIENT and BY_ATTEMPTS view. DEFAULT view gives consolidated metrics based on every singl [DEFAULT, BY_CLIENT, BY_ATTEM")

    @mcp.tool(name="aruba_central_getclientonboardingscorev1",
              annotations={"title": "Get onboarding score", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclientonboardingscorev1(params: _M_aruba_central_getclientonboardingscorev1) -> str:
        """Get onboarding score.

        Spec: monitoring | GET /network-monitoring/v1/client-onboarding-score
        Query params: start-at, end-at, site-id, stage, version, view-type
        """
        try:
            url = "/network-monitoring/v1/client-onboarding-score"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "site-id": params.site_id,
                "stage": params.stage,
                "version": params.version,
                "view-type": params.view_type,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclientonboardingstageexportv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: str = Field(..., description="Start timestamp (ISO date format). Must be earlier than end-at. If start-at and end-at are not provided, the default tim")
        end_at: str = Field(..., description="End timestamp (ISO date format). Must be later than start-at. If start-at and end-at are not provided, the default time ")
        site_id: Optional[str] = Field(None, description="Optional site identifier. If omitted, tenant-level aggregation is returned.")
        stage: Optional[str] = Field(None, description="Optional onboarding stage selector. Omit to get all supported stages. [assoc, auth, dhcp, dns]")
        version: Optional[str] = Field(None, description="Optional onboarding events version. If missing or non-numeric, default version is used.")
        view_type: Optional[str] = Field(None, description="view-type supports DEFAULT, BY_CLIENT and BY_ATTEMPTS view. DEFAULT view gives consolidated metrics based on every singl [DEFAULT, BY_CLIENT, BY_ATTEM")

    @mcp.tool(name="aruba_central_getclientonboardingstageexportv1",
              annotations={"title": "Get onboarding stage export data", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclientonboardingstageexportv1(params: _M_aruba_central_getclientonboardingstageexportv1) -> str:
        """Get onboarding stage export data.

        Spec: monitoring | GET /network-monitoring/v1/client-onboarding-stage/export
        Query params: start-at, end-at, site-id, stage, version, view-type
        """
        try:
            url = "/network-monitoring/v1/client-onboarding-stage/export"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "site-id": params.site_id,
                "stage": params.stage,
                "version": params.version,
                "view-type": params.view_type,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclientonboardingstagereasonsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: str = Field(..., description="Start timestamp (ISO date format). Must be earlier than end-at. If start-at and end-at are not provided, the default tim")
        end_at: str = Field(..., description="End timestamp (ISO date format). Must be later than start-at. If start-at and end-at are not provided, the default time ")
        site_id: Optional[str] = Field(None, description="Optional site identifier. If omitted, tenant-level aggregation is returned.")
        status: Optional[str] = Field(None, description="Optional status selector. Supported values: `FAILED` (stage failed), `DELAY` (successful with latency above threshold).  [FAILED, DELAY, SUCCESS]")
        stage: Optional[str] = Field(None, description="Optional onboarding stage selector. omit stage to get all supported stages. [assoc, auth, dhcp, dns]")
        version: Optional[str] = Field(None, description="Optional onboarding events version. If missing or non-numeric, default version is used.")
        view_type: Optional[str] = Field(None, description="view-type supports DEFAULT, BY_CLIENT and BY_ATTEMPTS view. DEFAULT view gives consolidated metrics based on every singl [DEFAULT, BY_CLIENT, BY_ATTEM")

    @mcp.tool(name="aruba_central_getclientonboardingstagereasonsv1",
              annotations={"title": "Get top onboarding reasons by stage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclientonboardingstagereasonsv1(params: _M_aruba_central_getclientonboardingstagereasonsv1) -> str:
        """Get top onboarding reasons by stage.

        Spec: monitoring | GET /network-monitoring/v1/client-onboarding-stage/reasons
        Query params: start-at, end-at, site-id, status, stage, version, view-type
        """
        try:
            url = "/network-monitoring/v1/client-onboarding-stage/reasons"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "site-id": params.site_id,
                "status": params.status,
                "stage": params.stage,
                "version": params.version,
                "view-type": params.view_type,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclientonboardingstagecountv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: str = Field(..., description="Start timestamp (ISO date format). Must be earlier than end-at. If start-at and end-at are not provided, the default tim")
        end_at: str = Field(..., description="End timestamp (ISO date format). Must be later than start-at. If start-at and end-at are not provided, the default time ")
        site_id: Optional[str] = Field(None, description="Optional site identifier. If omitted, tenant-level aggregation is returned.")
        field: Optional[str] = Field(None, description="Grouping field key. Supported values and meanings: `topclients` (client MAC), `topaccessdevices` (AP MAC), `band` (radio [topclients, topaccessdevices")
        status: Optional[str] = Field(None, description="Optional status selector. Supported values: `FAILED` (stage failed), `DELAY` (successful with latency above threshold),  [FAILED, DELAY, SUCCESS]")
        stage: Optional[str] = Field(None, description="Optional onboarding stage selector. Omit to get all supported stages. [assoc, auth, dhcp, dns]")
        version: Optional[str] = Field(None, description="Optional onboarding events version. If missing or non-numeric, default version is used.")
        view_type: Optional[str] = Field(None, description="view-type supports DEFAULT, BY_CLIENT and BY_ATTEMPTS view. DEFAULT view gives consolidated metrics based on every singl [DEFAULT, BY_CLIENT, BY_ATTEM")

    @mcp.tool(name="aruba_central_getclientonboardingstagecountv1",
              annotations={"title": "Get top onboarding counts by stage and status for a specific field", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclientonboardingstagecountv1(params: _M_aruba_central_getclientonboardingstagecountv1) -> str:
        """Get top onboarding counts by stage and status for a specific field.

        Spec: monitoring | GET /network-monitoring/v1/client-onboarding-stage/count
        Query params: start-at, end-at, site-id, field, status, stage, version, view-type
        """
        try:
            url = "/network-monitoring/v1/client-onboarding-stage/count"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "site-id": params.site_id,
                "field": params.field,
                "status": params.status,
                "stage": params.stage,
                "version": params.version,
                "view-type": params.view_type,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclientsusage(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")

    @mcp.tool(name="aruba_central_getclientsusage",
              annotations={"title": "Get Clients Usage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclientsusage(params: _M_aruba_central_getclientsusage) -> str:
        """Get Clients Usage.

        Spec: monitoring | GET /network-monitoring/v1/clients-usage
        Query params: filter
        """
        try:
            url = "/network-monitoring/v1/clients-usage"
            p = {k: v for k, v in {
                "filter": params.filter,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaylistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of gateways returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewaylistv1",
              annotations={"title": "List Gateways", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaylistv1(params: _M_aruba_central_getgatewaylistv1) -> str:
        """List Gateways.

        Spec: monitoring | GET /network-monitoring/v1/gateways
        Query params: filter, sort, limit, next
        """
        try:
            url = "/network-monitoring/v1/gateways"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaydetailv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewaydetailv1",
              annotations={"title": "Gateway Details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaydetailv1(params: _M_aruba_central_getgatewaydetailv1) -> str:
        """Gateway Details.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayclustervlanmismatchsummaryv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supported fields and operators are in the below given table.  |")

    @mcp.tool(name="aruba_central_getgatewayclustervlanmismatchsummaryv1",
              annotations={"title": "Gateway cluster VLAN mismatch summary", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayclustervlanmismatchsummaryv1(params: _M_aruba_central_getgatewayclustervlanmismatchsummaryv1) -> str:
        """Gateway cluster VLAN mismatch summary.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/vlan-mismatch
        Query params: filter
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/vlan-mismatch"
            p = {k: v for k, v in {
                "filter": params.filter,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayclusterconnectivitygraphv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")

    @mcp.tool(name="aruba_central_getgatewayclusterconnectivitygraphv1",
              annotations={"title": "Gateway cluster connectivity graph information", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayclusterconnectivitygraphv1(params: _M_aruba_central_getgatewayclusterconnectivitygraphv1) -> str:
        """Gateway cluster connectivity graph information.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/connectivity-graph
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/connectivity-graph"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayvlandetailv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        vlan_id: str = Field(..., description="vlan-id")

    @mcp.tool(name="aruba_central_getgatewayvlandetailv1",
              annotations={"title": "Gateway VLAN detail", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayvlandetailv1(params: _M_aruba_central_getgatewayvlandetailv1) -> str:
        """Gateway VLAN detail.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/vlans/{vlan-id}
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/vlans/{params.vlan_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayclustermemberlistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of gateways returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewayclustermemberlistv1",
              annotations={"title": "List Gateway Cluster members", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayclustermemberlistv1(params: _M_aruba_central_getgatewayclustermemberlistv1) -> str:
        """List Gateway Cluster members.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/members
        Query params: filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/members"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaytunneldetailv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_name: str = Field(..., description="tunnel-name")

    @mcp.tool(name="aruba_central_getgatewaytunneldetailv1",
              annotations={"title": "Gateway tunnel detail", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaytunneldetailv1(params: _M_aruba_central_getgatewaytunneldetailv1) -> str:
        """Gateway tunnel detail.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/tunnels/{params.tunnel_name}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayportslistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of ports returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewayportslistv1",
              annotations={"title": "List Gateway ports", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayportslistv1(params: _M_aruba_central_getgatewayportslistv1) -> str:
        """List Gateway ports.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/ports
        Query params: filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/ports"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayportdetailv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_number: str = Field(..., description="port-number")

    @mcp.tool(name="aruba_central_getgatewayportdetailv1",
              annotations={"title": "Gateway port detail", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayportdetailv1(params: _M_aruba_central_getgatewayportdetailv1) -> str:
        """Gateway port detail.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/ports/{params.port_number}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayclustertunnellistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of tunnels returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewayclustertunnellistv1",
              annotations={"title": "List Gateway Cluster tunnels", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayclustertunnellistv1(params: _M_aruba_central_getgatewayclustertunnellistv1) -> str:
        """List Gateway Cluster tunnels.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/tunnels
        Query params: filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/tunnels"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayvlanlistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of VLANs returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewayvlanlistv1",
              annotations={"title": "List Gateway VLANs", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayvlanlistv1(params: _M_aruba_central_getgatewayvlanlistv1) -> str:
        """List Gateway VLANs.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/vlans
        Query params: filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/vlans"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaytunnellistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of tunnels returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewaytunnellistv1",
              annotations={"title": "List Gateway tunnels", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaytunnellistv1(params: _M_aruba_central_getgatewaytunnellistv1) -> str:
        """List Gateway tunnels.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/tunnels
        Query params: filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/tunnels"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayuplinklistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        sort: Optional[str] = Field(None, description="Comma separated list of sort expressions. Each sort expression is a property name optionally followed by a direction ind")

    @mcp.tool(name="aruba_central_getgatewayuplinklistv1",
              annotations={"title": "List Gateway uplinks", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayuplinklistv1(params: _M_aruba_central_getgatewayuplinklistv1) -> str:
        """List Gateway uplinks.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks
        Query params: sort
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks"
            p = {k: v for k, v in {
                "sort": params.sort,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayhardwarecpuutilizationv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewayhardwarecpuutilizationv1",
              annotations={"title": "Get gateway CPU utilization trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayhardwarecpuutilizationv1(params: _M_aruba_central_getgatewayhardwarecpuutilizationv1) -> str:
        """Get gateway CPU utilization trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/cpu-utilization-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/cpu-utilization-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayhardwarememoryutilizationv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewayhardwarememoryutilizationv1",
              annotations={"title": "Get gateway memory utilization trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayhardwarememoryutilizationv1(params: _M_aruba_central_getgatewayhardwarememoryutilizationv1) -> str:
        """Get gateway memory utilization trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/memory-utilization-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/memory-utilization-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaytunnelthroughputtrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_name: str = Field(..., description="tunnel-name")

    @mcp.tool(name="aruba_central_getgatewaytunnelthroughputtrendv1",
              annotations={"title": "Get gateway tunnel throughput trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaytunnelthroughputtrendv1(params: _M_aruba_central_getgatewaytunnelthroughputtrendv1) -> str:
        """Get gateway tunnel throughput trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/tunnels/{params.tunnel_name}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaytunnelstatustrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_name: str = Field(..., description="tunnel-name")

    @mcp.tool(name="aruba_central_getgatewaytunnelstatustrendv1",
              annotations={"title": "Get gateway tunnel status trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaytunnelstatustrendv1(params: _M_aruba_central_getgatewaytunnelstatustrendv1) -> str:
        """Get gateway tunnel status trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}/status-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/tunnels/{params.tunnel_name}/status-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclustercapacitytrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")

    @mcp.tool(name="aruba_central_getclustercapacitytrendv1",
              annotations={"title": "Get cluster capacity trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclustercapacitytrendv1(params: _M_aruba_central_getclustercapacitytrendv1) -> str:
        """Get cluster capacity trend.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/capacity-trends
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/capacity-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getclustermembercapacitytrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getclustermembercapacitytrendv1",
              annotations={"title": "Get cluster member capacity trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getclustermembercapacitytrendv1(params: _M_aruba_central_getclustermembercapacitytrendv1) -> str:
        """Get cluster member capacity trend.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/capacity-trends/{serial-number}
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/capacity-trends/{params.serial_number}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayportthroughputtrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_number: str = Field(..., description="port-number")

    @mcp.tool(name="aruba_central_getgatewayportthroughputtrendv1",
              annotations={"title": "Get gateway port throughput trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayportthroughputtrendv1(params: _M_aruba_central_getgatewayportthroughputtrendv1) -> str:
        """Get gateway port throughput trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/ports/{params.port_number}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayclustertunnelhealthv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")

    @mcp.tool(name="aruba_central_getgatewayclustertunnelhealthv1",
              annotations={"title": "Get summary of cluster tunnel health", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayclustertunnelhealthv1(params: _M_aruba_central_getgatewayclustertunnelhealthv1) -> str:
        """Get summary of cluster tunnel health.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/tunnels-health-summary
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/tunnels-health-summary"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayclustertunnelsstatussummaryv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        cluster_name: str = Field(..., description="cluster-name")

    @mcp.tool(name="aruba_central_getgatewayclustertunnelsstatussummaryv1",
              annotations={"title": "Get summary of cluster tunnel status", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayclustertunnelsstatussummaryv1(params: _M_aruba_central_getgatewayclustertunnelsstatussummaryv1) -> str:
        """Get summary of cluster tunnel status.

        Spec: monitoring | GET /network-monitoring/v1/clusters/{cluster-name}/tunnels-status-summary
        """
        try:
            url = f"/network-monitoring/v1/clusters/{params.cluster_name}/tunnels-status-summary"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaylantunnelhealthv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewaylantunnelhealthv1",
              annotations={"title": "Get summary of gateway LAN tunnels health", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaylantunnelhealthv1(params: _M_aruba_central_getgatewaylantunnelhealthv1) -> str:
        """Get summary of gateway LAN tunnels health.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/lan-tunnels-health-summary
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/lan-tunnels-health-summary"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaywanavailabilitytrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewaywanavailabilitytrendsv1",
              annotations={"title": "Get gateway WAN availability trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaywanavailabilitytrendsv1(params: _M_aruba_central_getgatewaywanavailabilitytrendsv1) -> str:
        """Get gateway WAN availability trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/wan-availability-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/wan-availability-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayvpnavailabilitytrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewayvpnavailabilitytrendsv1",
              annotations={"title": "Get gateway VPN availability trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayvpnavailabilitytrendsv1(params: _M_aruba_central_getgatewayvpnavailabilitytrendsv1) -> str:
        """Get gateway VPN availability trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/vpn-availability-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/vpn-availability-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayframestrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_number: str = Field(..., description="port-number")

    @mcp.tool(name="aruba_central_getgatewayframestrendv1",
              annotations={"title": "Get gateway port frames trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayframestrendv1(params: _M_aruba_central_getgatewayframestrendv1) -> str:
        """Get gateway port frames trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/frames-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/ports/{params.port_number}/frames-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayframeserrorstrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_number: str = Field(..., description="port-number")

    @mcp.tool(name="aruba_central_getgatewayframeserrorstrendv1",
              annotations={"title": "Get gateway port frames errors trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayframeserrorstrendv1(params: _M_aruba_central_getgatewayframeserrorstrendv1) -> str:
        """Get gateway port frames errors trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/frames-errors-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/ports/{params.port_number}/frames-errors-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayframespacketstrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        port_number: str = Field(..., description="port-number")

    @mcp.tool(name="aruba_central_getgatewayframespacketstrendv1",
              annotations={"title": "Get gateway port frames packets trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayframespacketstrendv1(params: _M_aruba_central_getgatewayframespacketstrendv1) -> str:
        """Get gateway port frames packets trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/frames-packets-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/ports/{params.port_number}/frames-packets-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaytunneldroppedpacketstrendv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        tunnel_name: str = Field(..., description="tunnel-name")

    @mcp.tool(name="aruba_central_getgatewaytunneldroppedpacketstrendv1",
              annotations={"title": "Get gateway tunnel dropped packets trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaytunneldroppedpacketstrendv1(params: _M_aruba_central_getgatewaytunneldroppedpacketstrendv1) -> str:
        """Get gateway tunnel dropped packets trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}/dropped-packet-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/tunnels/{params.tunnel_name}/dropped-packet-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaywantunnelhealthv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewaywantunnelhealthv1",
              annotations={"title": "Get summary of gateway WAN tunnel health", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaywantunnelhealthv1(params: _M_aruba_central_getgatewaywantunnelhealthv1) -> str:
        """Get summary of gateway WAN tunnel health.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/wan-tunnels-health-summary
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/wan-tunnels-health-summary"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaywaninterfacedetailv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        link_tag: str = Field(..., description="link-tag")

    @mcp.tool(name="aruba_central_getgatewaywaninterfacedetailv1",
              annotations={"title": "Get details of gateway uplink", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaywaninterfacedetailv1(params: _M_aruba_central_getgatewaywaninterfacedetailv1) -> str:
        """Get details of gateway uplink.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.link_tag}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayuplinkthroughputtrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        link_tag: str = Field(..., description="link-tag")

    @mcp.tool(name="aruba_central_getgatewayuplinkthroughputtrendsv1",
              annotations={"title": "Get gateway uplink throughput trend", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayuplinkthroughputtrendsv1(params: _M_aruba_central_getgatewayuplinkthroughputtrendsv1) -> str:
        """Get gateway uplink throughput trend.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/throughput-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.link_tag}/throughput-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaywancompressiontrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        link_tag: str = Field(..., description="link-tag")

    @mcp.tool(name="aruba_central_getgatewaywancompressiontrendsv1",
              annotations={"title": "Get gateway WAN compression trends for an uplink", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaywancompressiontrendsv1(params: _M_aruba_central_getgatewaywancompressiontrendsv1) -> str:
        """Get gateway WAN compression trends for an uplink.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/wan-compression-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.link_tag}/wan-compression-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayuplinkprobelistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        link_tag: str = Field(..., description="link-tag")

    @mcp.tool(name="aruba_central_getgatewayuplinkprobelistv1",
              annotations={"title": "List gateway uplink probes", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayuplinkprobelistv1(params: _M_aruba_central_getgatewayuplinkprobelistv1) -> str:
        """List gateway uplink probes.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/probes
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.link_tag}/probes"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayuplinkwanavailabilitytrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        link_tag: str = Field(..., description="link-tag")

    @mcp.tool(name="aruba_central_getgatewayuplinkwanavailabilitytrendsv1",
              annotations={"title": "Get WAN availability trends of gateway uplink", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayuplinkwanavailabilitytrendsv1(params: _M_aruba_central_getgatewayuplinkwanavailabilitytrendsv1) -> str:
        """Get WAN availability trends of gateway uplink.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/wan-availability-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.link_tag}/wan-availability-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayuplinkvpnavailabilitytrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        vlan_id: str = Field(..., description="vlan-id")

    @mcp.tool(name="aruba_central_getgatewayuplinkvpnavailabilitytrendsv1",
              annotations={"title": "Get VPN availability trends of gateway uplink", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayuplinkvpnavailabilitytrendsv1(params: _M_aruba_central_getgatewayuplinkvpnavailabilitytrendsv1) -> str:
        """Get VPN availability trends of gateway uplink.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{vlan-id}/vpn-availability-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.vlan_id}/vpn-availability-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayhardwaretemperaturev1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getgatewayhardwaretemperaturev1",
              annotations={"title": "Get gateway hardware temperature trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayhardwaretemperaturev1(params: _M_aruba_central_getgatewayhardwaretemperaturev1) -> str:
        """Get gateway hardware temperature trends.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/hardware-temperature-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/hardware-temperature-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaydhcppoollistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of DHCP pools returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewaydhcppoollistv1",
              annotations={"title": "Get DHCP pools configured on the gateway", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaydhcppoollistv1(params: _M_aruba_central_getgatewaydhcppoollistv1) -> str:
        """Get DHCP pools configured on the gateway.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/dhcp-pools
        Query params: sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/dhcp-pools"
            p = {k: v for k, v in {
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaydhcpleaselistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="A comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction i")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of DHCP clients returned in the response. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources.  Minimum value: 1 ")

    @mcp.tool(name="aruba_central_getgatewaydhcpleaselistv1",
              annotations={"title": "Get DHCP leases present in the DHCP pool", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaydhcpleaselistv1(params: _M_aruba_central_getgatewaydhcpleaselistv1) -> str:
        """Get DHCP leases present in the DHCP pool.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/dhcp-clients
        Query params: filter, sort, limit, next
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/dhcp-clients"
            p = {k: v for k, v in {
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewayuplinkperformancetrendsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        link_tag: str = Field(..., description="link-tag")
        probe: str = Field(..., description="probe")

    @mcp.tool(name="aruba_central_getgatewayuplinkperformancetrendsv1",
              annotations={"title": "Get uplink probe performance trends", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewayuplinkperformancetrendsv1(params: _M_aruba_central_getgatewayuplinkperformancetrendsv1) -> str:
        """Get uplink probe performance trends.

        Spec: monitoring | GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/probes/{probe}/performance-trends
        """
        try:
            url = f"/network-monitoring/v1/gateways/{params.serial_number}/uplinks/{params.link_tag}/probes/{params.probe}/performance-trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_listtenantsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_listtenantsv1",
              annotations={"title": "Get all MSP tenants information.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_listtenantsv1(params: _M_aruba_central_listtenantsv1) -> str:
        """Get all MSP tenants information..

        Spec: msp | GET /network-msp/v1/list-tenants
        """
        try:
            url = "/network-msp/v1/list-tenants"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getalertconfigs(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        scope_id: str = Field(..., description="The scope identifier for which alert configurations are retrieved. ")
        scope_type: Optional[str] = Field(None, description="The scope type. Determines the level at which the configuration applies.  | Value | Description | |-------|------------- [GLOBAL, SITE, DEVICE]")
        limit: Optional[int] = Field(None, description="Maximum number of alert configurations to return per page. Defaults to `20` when not specified. ")
        next: Optional[int] = Field(None, description="Zero-based offset of the first alert configuration to return. Use together with `limit` to paginate through results. Def")

    @mcp.tool(name="aruba_central_getalertconfigs",
              annotations={"title": "List alert configurations", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getalertconfigs(params: _M_aruba_central_getalertconfigs) -> str:
        """List alert configurations.

        Spec: notifications | GET /network-notifications/v1/alert-config
        Query params: scope-id, scope-type, limit, next
        """
        try:
            url = "/network-notifications/v1/alert-config"
            p = {k: v for k, v in {
                "scope-id": params.scope_id,
                "scope-type": params.scope_type,
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getinsightschemasv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        insight_id: Optional[str] = Field(None, description="Insight type identifier (e.g. `702`). When omitted, all insight schemas are returned. `insight-id` can be obtained from ")

    @mcp.tool(name="aruba_central_getinsightschemasv1",
              annotations={"title": "Get insight schemas", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getinsightschemasv1(params: _M_aruba_central_getinsightschemasv1) -> str:
        """Get insight schemas.

        Spec: notifications | GET /network-notifications/v1/insights-schema
        Query params: insight-id
        """
        try:
            url = "/network-notifications/v1/insights-schema"
            p = {k: v for k, v in {
                "insight-id": params.insight_id,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_listreports(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        search: Optional[str] = Field(None, description="Search the Report based on Name, Type, Status and Saved By")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="Sort expressions. Each sort expression is a property name optionally followed by a direction indicator asc (ascending) o")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources. Minimum value is 1.")
        limit: Optional[int] = Field(None, description="Maximum number of reports to be retrieved. Allowed range is 1 to 100.")

    @mcp.tool(name="aruba_central_listreports",
              annotations={"title": "List Reports", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_listreports(params: _M_aruba_central_listreports) -> str:
        """List Reports.

        Spec: reporting | GET /network-reporting/v1/reports
        Query params: search, filter, sort, next, limit
        """
        try:
            url = "/network-reporting/v1/reports"
            p = {k: v for k, v in {
                "search": params.search,
                "filter": params.filter,
                "sort": params.sort,
                "next": params.next,
                "limit": params.limit,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updateuserreport(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        report_id: str = Field(..., description="report-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updateuserreport",
              annotations={"title": "Update Report", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updateuserreport(params: _M_aruba_central_updateuserreport) -> str:
        """Update Report.

        Spec: reporting | PUT /network-reporting/v1/reports/{report-id}
        """
        try:
            url = f"/network-reporting/v1/reports/{params.report_id}"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deleteuserreport(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        report_id: str = Field(..., description="report-id")

    @mcp.tool(name="aruba_central_deleteuserreport",
              annotations={"title": "Delete Report", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deleteuserreport(params: _M_aruba_central_deleteuserreport) -> str:
        """Delete Report.

        Spec: reporting | DELETE /network-reporting/v1/reports/{report-id}
        """
        try:
            url = f"/network-reporting/v1/reports/{params.report_id}"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_listreportrun(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        report_id: str = Field(..., description="report-id")
        sort: Optional[str] = Field(None, description="Sort expression. Each sort expression is a property name optionally followed by a direction indicator asc (ascending) or")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources. Minimum value is 1.")
        limit: Optional[int] = Field(None, description="Maximum number of reports to be returned. Allowed range is 1 to 100.")

    @mcp.tool(name="aruba_central_listreportrun",
              annotations={"title": "List Report Runs", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_listreportrun(params: _M_aruba_central_listreportrun) -> str:
        """List Report Runs.

        Spec: reporting | GET /network-reporting/v1/reports/{report-id}/report-runs
        Query params: sort, next, limit
        """
        try:
            url = f"/network-reporting/v1/reports/{params.report_id}/report-runs"
            p = {k: v for k, v in {
                "sort": params.sort,
                "next": params.next,
                "limit": params.limit,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deletereportrun(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        report_id: str = Field(..., description="report-id")
        report_run_id: str = Field(..., description="report-run-id")

    @mcp.tool(name="aruba_central_deletereportrun",
              annotations={"title": "Delete Report Run", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deletereportrun(params: _M_aruba_central_deletereportrun) -> str:
        """Delete Report Run.

        Spec: reporting | DELETE /network-reporting/v1/reports/{report-id}/report-runs/{report-run-id}
        """
        try:
            url = f"/network-reporting/v1/reports/{params.report_id}/report-runs/{params.report_run_id}"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_downloadreportlink(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        report_id: str = Field(..., description="report-id")
        report_run_id: str = Field(..., description="report-run-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_downloadreportlink",
              annotations={"title": "Get Download Report Link", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_downloadreportlink(params: _M_aruba_central_downloadreportlink) -> str:
        """Get Download Report Link.

        Spec: reporting | POST /network-reporting/v1/reports/{report-id}/report-runs/{report-run-id}/download-link
        """
        try:
            url = f"/network-reporting/v1/reports/{params.report_id}/report-runs/{params.report_run_id}/download-link"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getlatrendsforapiv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_getlatrendsforapiv1",
              annotations={"title": "Get all the trends of a client for a tenant or a site for a given time range.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getlatrendsforapiv1(params: _M_aruba_central_getlatrendsforapiv1) -> str:
        """Get all the trends of a client for a tenant or a site for a given time range..

        Spec: services | GET /network-services/v1/location-analytics/trends
        """
        try:
            url = "/network-services/v1/location-analytics/trends"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getlasitesinsightsforapiv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_getlasitesinsightsforapiv1",
              annotations={"title": "Get the insights for each site of a tenant for a given time range.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getlasitesinsightsforapiv1(params: _M_aruba_central_getlasitesinsightsforapiv1) -> str:
        """Get the insights for each site of a tenant for a given time range..

        Spec: services | GET /network-services/v1/location-analytics/sites/insights
        """
        try:
            url = "/network-services/v1/location-analytics/sites/insights"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getdevicelocationsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        filter: Optional[str] = Field(None, description="OData 4.0 filter (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT supported). Supports f")
        limit: Optional[int] = Field(None, description="limit")
        next: Optional[str] = Field(None, description="next")
        with_location: Optional[bool] = Field(None, description="Filter for devices with or without location based on this parameter. ")

    @mcp.tool(name="aruba_central_getdevicelocationsv1",
              annotations={"title": "List devices with location information", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getdevicelocationsv1(params: _M_aruba_central_getdevicelocationsv1) -> str:
        """List devices with location information.

        Spec: services | GET /network-services/v1/sites/{site-id}/device-locations
        Query params: filter, limit, next, with-location
        """
        try:
            url = f"/network-services/v1/sites/{params.site_id}/device-locations"
            p = {k: v for k, v in {
                "filter": params.filter,
                "limit": params.limit,
                "next": params.next,
                "with-location": params.with_location,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getlocationbyidv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        location_id: str = Field(..., description="location-id")

    @mcp.tool(name="aruba_central_getlocationbyidv1",
              annotations={"title": "Get location resource", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getlocationbyidv1(params: _M_aruba_central_getlocationbyidv1) -> str:
        """Get location resource.

        Spec: services | GET /network-services/v1/sites/{site-id}/device-locations/{location-id}
        """
        try:
            url = f"/network-services/v1/sites/{params.site_id}/device-locations/{params.location_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getdevicedetailedlocationv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_getdevicedetailedlocationv1",
              annotations={"title": "Get device location details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getdevicedetailedlocationv1(params: _M_aruba_central_getdevicedetailedlocationv1) -> str:
        """Get device location details.

        Spec: services | GET /network-services/v1/sites/{site-id}/devices/{serial-number}/location
        """
        try:
            url = f"/network-services/v1/sites/{params.site_id}/devices/{params.serial_number}/location"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_putdeviceadminlocationv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        serial_number: str = Field(..., description="serial-number")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_putdeviceadminlocationv1",
              annotations={"title": "Set device coordinates", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_putdeviceadminlocationv1(params: _M_aruba_central_putdeviceadminlocationv1) -> str:
        """Set device coordinates.

        Spec: services | POST /network-services/v1/sites/{site-id}/devices/{serial-number}/location
        """
        try:
            url = f"/network-services/v1/sites/{params.site_id}/devices/{params.serial_number}/location"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deldeviceadminlocationv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_deldeviceadminlocationv1",
              annotations={"title": "Delete device coordinates", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deldeviceadminlocationv1(params: _M_aruba_central_deldeviceadminlocationv1) -> str:
        """Delete device coordinates.

        Spec: services | DELETE /network-services/v1/sites/{site-id}/devices/{serial-number}/location
        """
        try:
            url = f"/network-services/v1/sites/{params.site_id}/devices/{params.serial_number}/location"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_radio(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        serial_number: Optional[str] = Field(None, description="AP Serial number to get reporting radio information for radios on that AP")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_radio",
              annotations={"title": "Get reporting radio information of a specific radio MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_radio(params: _M_aruba_central_airmatch_get_radio) -> str:
        """Get reporting radio information of a specific radio MAC.

        Spec: services | GET /network-services/v1/airmatch-radio/{radio-mac}
        Query params: serial-number, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-radio/{params.radio_mac}"
            p = {k: v for k, v in {
                "serial-number": params.serial_number,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_radios(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: Optional[str] = Field(None, description="AP Serial number to get reporting radio information for radios on that AP")
        is_static: Optional[bool] = Field(None, description="Get Static Radio Documents for radios with static channel or power")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_radios",
              annotations={"title": "Get all radios for a tenant or radios based on AP Serial", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_radios(params: _M_aruba_central_airmatch_get_radios) -> str:
        """Get all radios for a tenant or radios based on AP Serial.

        Spec: services | GET /network-services/v1/airmatch-radio
        Query params: serial-number, is-static, limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-radio"
            p = {k: v for k, v in {
                "serial-number": params.serial_number,
                "is-static": params.is_static,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_ap(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_ap",
              annotations={"title": "Get AP information of a specific AP Ethernet MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_ap(params: _M_aruba_central_airmatch_get_ap) -> str:
        """Get AP information of a specific AP Ethernet MAC.

        Spec: services | GET /network-services/v1/airmatch-ap/{serial-number}
        Query params: limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-ap/{params.serial_number}"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_all_ap(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_all_ap",
              annotations={"title": "Get AP information for all APs of a tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_all_ap(params: _M_aruba_central_airmatch_get_all_ap) -> str:
        """Get AP information for all APs of a tenant.

        Spec: services | GET /network-services/v1/airmatch-ap
        Query params: offset, limit
        """
        try:
            url = "/network-services/v1/airmatch-ap"
            p = {k: v for k, v in {
                "offset": params.offset,
                "limit": params.limit,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_ap_radio_relations(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_ap_radio_relations",
              annotations={"title": "Get AP radio relations from edge document", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_ap_radio_relations(params: _M_aruba_central_airmatch_get_ap_radio_relations) -> str:
        """Get AP radio relations from edge document.

        Spec: services | GET /network-services/v1/airmatch-ap-radio-relations/{serial-number}
        Query params: limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-ap-radio-relations/{params.serial_number}"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_priority_rf_events_by_radio_mac(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest Priority RF Event to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest Priority RF Event to end query result")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_priority_rf_events_by_radio_mac",
              annotations={"title": "Get radar and noise RF events of a specific Radio MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_priority_rf_events_by_radio_mac(params: _M_aruba_central_airmatch_get_priority_rf_events_by_radio_mac) -> str:
        """Get radar and noise RF events of a specific Radio MAC.

        Spec: services | GET /network-services/v1/airmatch-priority-rf-events/{radio-mac}
        Query params: start-at, end-at, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-priority-rf-events/{params.radio_mac}"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_all_priority_rf_events(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest Priority RF Event to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest Priority RF Event to end query result")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_all_priority_rf_events",
              annotations={"title": "Get all radar and noise RF events of a tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_all_priority_rf_events(params: _M_aruba_central_airmatch_get_all_priority_rf_events) -> str:
        """Get all radar and noise RF events of a tenant.

        Spec: services | GET /network-services/v1/airmatch-priority-rf-events
        Query params: start-at, end-at, limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-priority-rf-events"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_rf_events_by_radio_mac(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest RF Event to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest RF Event to end query result")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_rf_events_by_radio_mac",
              annotations={"title": "Get RF events of a specific Radio MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_rf_events_by_radio_mac(params: _M_aruba_central_airmatch_get_rf_events_by_radio_mac) -> str:
        """Get RF events of a specific Radio MAC.

        Spec: services | GET /network-services/v1/airmatch-rf-events/{radio-mac}
        Query params: start-at, end-at, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-rf-events/{params.radio_mac}"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_all_rf_events(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest RF Event to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest RF Event to end query result")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_all_rf_events",
              annotations={"title": "Get all RF events of a tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_all_rf_events(params: _M_aruba_central_airmatch_get_all_rf_events) -> str:
        """Get all RF events of a tenant.

        Spec: services | GET /network-services/v1/airmatch-rf-events
        Query params: start-at, end-at, limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-rf-events"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_history_by_radio_mac(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest Radio History to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest Radio History to end query result")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_history_by_radio_mac",
              annotations={"title": "Get radio history of a specific Radio MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_history_by_radio_mac(params: _M_aruba_central_airmatch_get_history_by_radio_mac) -> str:
        """Get radio history of a specific Radio MAC.

        Spec: services | GET /network-services/v1/airmatch-history/{radio-mac}
        Query params: start-at, end-at, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-history/{params.radio_mac}"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_service_config(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_service_config",
              annotations={"title": "Returns Device (AP) Running Configuration", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_service_config(params: _M_aruba_central_airmatch_get_service_config) -> str:
        """Returns Device (AP) Running Configuration.

        Spec: services | GET /network-services/v1/airmatch-service-config
        Query params: limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-service-config"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_global_config_id(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_global_config_id",
              annotations={"title": "Returns the global configuration ID for the tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_global_config_id(params: _M_aruba_central_airmatch_get_global_config_id) -> str:
        """Returns the global configuration ID for the tenant.

        Spec: services | GET /network-services/v1/airmatch-global-config-id
        Query params: limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-global-config-id"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_radio_feas_by_radio_mac(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_radio_feas_by_radio_mac",
              annotations={"title": "Get radio feasibility of a specific radio MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_radio_feas_by_radio_mac(params: _M_aruba_central_airmatch_get_radio_feas_by_radio_mac) -> str:
        """Get radio feasibility of a specific radio MAC.

        Spec: services | GET /network-services/v1/airmatch-radio-feasibility/{radio-mac}
        Query params: limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-radio-feasibility/{params.radio_mac}"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_all_radio_feas(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_all_radio_feas",
              annotations={"title": "Get all radio feasibility for a tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_all_radio_feas(params: _M_aruba_central_airmatch_get_all_radio_feas) -> str:
        """Get all radio feasibility for a tenant.

        Spec: services | GET /network-services/v1/airmatch-radio-feasibility
        Query params: offset, limit
        """
        try:
            url = "/network-services/v1/airmatch-radio-feasibility"
            p = {k: v for k, v in {
                "offset": params.offset,
                "limit": params.limit,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_radio_board_limit(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        radio_mac: str = Field(..., description="radio-mac")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_radio_board_limit",
              annotations={"title": "Get board limits of a specific radio MAC for a given tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_radio_board_limit(params: _M_aruba_central_airmatch_get_radio_board_limit) -> str:
        """Get board limits of a specific radio MAC for a given tenant.

        Spec: services | GET /network-services/v1/airmatch-board-limit/{serial-number}/{radio-mac}
        Query params: limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-board-limit/{params.serial_number}/{params.radio_mac}"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_device_config_by_ap_serial(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_device_config_by_ap_serial",
              annotations={"title": "Returns Device (AP) Configuration for a specific AP Serial number", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_device_config_by_ap_serial(params: _M_aruba_central_airmatch_get_device_config_by_ap_serial) -> str:
        """Returns Device (AP) Configuration for a specific AP Serial number.

        Spec: services | GET /network-services/v1/airmatch-device-config/{serial-number}
        Query params: limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-device-config/{params.serial_number}"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_non_friends(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest Pathloss to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest Pathloss to end query result")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_non_friends",
              annotations={"title": "Get list of non friend (non-neighbor) radios for that radio mac", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_non_friends(params: _M_aruba_central_airmatch_get_non_friends) -> str:
        """Get list of non friend (non-neighbor) radios for that radio mac.

        Spec: services | GET /network-services/v1/airmatch-non-friend/{radio-mac}
        Query params: start-at, end-at, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-non-friend/{params.radio_mac}"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_radio_all_nbr_pathloss(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        start_at: Optional[str] = Field(None, description="Timestamp of oldest Pathloss to start query result")
        end_at: Optional[str] = Field(None, description="Timestamp of newest Pathloss to end query result")
        include_non_friend: Optional[bool] = Field(None, description="Append list of non friend (non-neighbor) pathloss to output (default false) [True, False]")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_radio_all_nbr_pathloss",
              annotations={"title": "Get all neighbor pathloss for a tenant and radio mac", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_radio_all_nbr_pathloss(params: _M_aruba_central_airmatch_get_radio_all_nbr_pathloss) -> str:
        """Get all neighbor pathloss for a tenant and radio mac.

        Spec: services | GET /network-services/v1/airmatch-pathloss/{radio-mac}
        Query params: start-at, end-at, include-non-friend, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-pathloss/{params.radio_mac}"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "include-non-friend": params.include_non_friend,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_process_ap_neighbors_get_req(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        limit: Optional[int] = Field(None, description="Number of AP serial numbers to get (max. 500)")
        cutoff: Optional[int] = Field(None, description="Neighbors up to this max pathloss (max. 150)")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_process_ap_neighbors_get_req",
              annotations={"title": "Get list of AP neighbors for a given AP serial number", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_process_ap_neighbors_get_req(params: _M_aruba_central_airmatch_process_ap_neighbors_get_req) -> str:
        """Get list of AP neighbors for a given AP serial number.

        Spec: services | GET /network-services/v1/airmatch-ap-neighbor-list/{serial-number}
        Query params: limit, cutoff, offset
        """
        try:
            url = f"/network-services/v1/airmatch-ap-neighbor-list/{params.serial_number}"
            p = {k: v for k, v in {
                "limit": params.limit,
                "cutoff": params.cutoff,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_process_partition_get_req(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        band_selected: Optional[str] = Field(None, description="Radio Frequency band filter to return partitions for that band [2.4GHz, 5GHz, 6GHz]")
        type: Optional[str] = Field(None, description="Partition Type filter to return partitions for that partition type. Supported values are normal, opmode, and dynamic [normal, opmode, dynamic]")
        summary: Optional[bool] = Field(None, description="Output Summary for Partition (default false) [True, False]")
        id: Optional[str] = Field(None, description="Request ID used to find specific partition information using provided request id")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_process_partition_get_req",
              annotations={"title": "Get RF partition information", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_process_partition_get_req(params: _M_aruba_central_airmatch_process_partition_get_req) -> str:
        """Get RF partition information.

        Spec: services | GET /network-services/v1/airmatch-partition
        Query params: band-selected, type, summary, id, offset, limit
        """
        try:
            url = "/network-services/v1/airmatch-partition"
            p = {k: v for k, v in {
                "band-selected": params.band_selected,
                "type": params.type,
                "summary": params.summary,
                "id": params.id,
                "offset": params.offset,
                "limit": params.limit,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_process_partition_post_req(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_airmatch_process_partition_post_req",
              annotations={"title": "Send RF Partition Request to Airmatch", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_airmatch_process_partition_post_req(params: _M_aruba_central_airmatch_process_partition_post_req) -> str:
        """Send RF Partition Request to Airmatch.

        Spec: services | POST /network-services/v1/airmatch-partition
        """
        try:
            url = "/network-services/v1/airmatch-partition"
            p = {}
            data = await api_fn("POST", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_friend_partition_key(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        type: Optional[str] = Field(None, description="Partition type [normal, opmode, dynamic]")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_friend_partition_key",
              annotations={"title": "Get rf domain and partition id for a specific radio mac address", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_friend_partition_key(params: _M_aruba_central_airmatch_get_friend_partition_key) -> str:
        """Get rf domain and partition id for a specific radio mac address.

        Spec: services | GET /network-services/v1/airmatch-radio-partition/{radio-mac}
        Query params: type, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-radio-partition/{params.radio_mac}"
            p = {k: v for k, v in {
                "type": params.type,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_process_optimization_post_req(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        runmode: str = Field(..., description="runmode (case-insensitive). Valid values: ON-DEMAND, INCREMENTAL, OPMODE")
        threshold: Optional[bool] = Field(None, description="Threshold value filter used to process partition with user specified channel threshold value [True, False]")
        delay: Optional[str] = Field(None, description="Delay the deployment of solution in minutes; Range [0-360], default 0")
        window: Optional[str] = Field(None, description="Deploy Window in minutes; Range [0-360], default 120")

    @mcp.tool(name="aruba_central_airmatch_process_optimization_post_req",
              annotations={"title": "Sends an optimization request to Airmatch to compute and deploy a solution", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_airmatch_process_optimization_post_req(params: _M_aruba_central_airmatch_process_optimization_post_req) -> str:
        """Sends an optimization request to Airmatch to compute and deploy a solution.

        Spec: services | POST /network-services/v1/airmatch-runnow
        Query params: runmode, threshold, delay, window
        """
        try:
            url = "/network-services/v1/airmatch-runnow"
            p = {k: v for k, v in {
                "runmode": params.runmode,
                "threshold": params.threshold,
                "delay": params.delay,
                "window": params.window,
            }.items() if v is not None}
            data = await api_fn("POST", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_process_optimization_get_req(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        count: Optional[int] = Field(None, description="Number of solutions to return.")
        start_at: Optional[str] = Field(None, description="Filter for solutions with timestamp greater than or equal to the provided timestamp")
        end_at: Optional[str] = Field(None, description="Filter for solutions with timestamp less than or equal to the provided timestamp")
        runmode: Optional[str] = Field(None, description="Runmode Filter to return solutions for that runmode. Valid values are SCHEDULE, ON-DEMAND, INCREMENTAL, OPMODE, and EIRP [SCHEDULED, ON-DEMAND, INCREM")
        rf_domain_id: Optional[int] = Field(None, description="RF Domain ID filter to return solutions for radios in a specific rf domain")
        rf_partition_id: Optional[int] = Field(None, description="RF Partition ID filter to return solutions for radios in a specific rf partition")
        band_selected: Optional[str] = Field(None, description="Radio band filter to return solutions for radios in a specific band [2.4GHz, 5GHz, 6GHz]")
        id: Optional[str] = Field(None, description="Request ID Filter to return specific solution using request id provided by user in query parameter")
        status: Optional[str] = Field(None, description="Filters solution documents based on deployment status field. Valid values are COMPUTED, SENT, RETRIED, DEPLOY_UNSUCCESSF [COMPUTED, SENT, RETRIED, DEP")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_process_optimization_get_req",
              annotations={"title": "Get solver optimizations for a given tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_process_optimization_get_req(params: _M_aruba_central_airmatch_process_optimization_get_req) -> str:
        """Get solver optimizations for a given tenant.

        Spec: services | GET /network-services/v1/airmatch-solution
        Query params: count, start-at, end-at, runmode, rf-domain-id, rf-partition-id, band-selected, id, status, limit
        """
        try:
            url = "/network-services/v1/airmatch-solution"
            p = {k: v for k, v in {
                "count": params.count,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "runmode": params.runmode,
                "rf-domain-id": params.rf_domain_id,
                "rf-partition-id": params.rf_partition_id,
                "band-selected": params.band_selected,
                "id": params.id,
                "status": params.status,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_radio_plan_by_radio_mac(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        radio_mac: str = Field(..., description="radio-mac")
        count: Optional[int] = Field(None, description="Number of solutions to return.")
        start_at: Optional[str] = Field(None, description="Filter for solutions with timestamp greater than or equal to the provided timestamp")
        end_at: Optional[str] = Field(None, description="Filter for solutions with timestamp less than or equal to the provided timestamp")
        runmode: Optional[str] = Field(None, description="Runmode Filter to return solutions for that runmode")
        id: Optional[str] = Field(None, description="Request ID Filter to return specific solution using request id provided by user in query parameter")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_radio_plan_by_radio_mac",
              annotations={"title": "Get solution of a specific Radio MAC", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_radio_plan_by_radio_mac(params: _M_aruba_central_airmatch_get_radio_plan_by_radio_mac) -> str:
        """Get solution of a specific Radio MAC.

        Spec: services | GET /network-services/v1/airmatch-solution/{radio-mac}
        Query params: count, start-at, end-at, runmode, id, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-solution/{params.radio_mac}"
            p = {k: v for k, v in {
                "count": params.count,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "runmode": params.runmode,
                "id": params.id,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_ap_coverage_plan_by_ap_serial(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        id: Optional[str] = Field(None, description="Request ID filter to return specific AP Coverage Plan using request id provided by user in query parameter")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_ap_coverage_plan_by_ap_serial",
              annotations={"title": "Get ap coverage plan for a given AP serial number", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_ap_coverage_plan_by_ap_serial(params: _M_aruba_central_airmatch_get_ap_coverage_plan_by_ap_serial) -> str:
        """Get ap coverage plan for a given AP serial number.

        Spec: services | GET /network-services/v1/airmatch-ap-coverage-plan/{serial-number}
        Query params: id, limit, offset
        """
        try:
            url = f"/network-services/v1/airmatch-ap-coverage-plan/{params.serial_number}"
            p = {k: v for k, v in {
                "id": params.id,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_get_all_ap_coverage_plan(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: Optional[str] = Field(None, description="Request ID filter to return specific AP Coverage Plan using request id provided by user in query parameter")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_get_all_ap_coverage_plan",
              annotations={"title": "Get all AP coverage plan from collection", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_get_all_ap_coverage_plan(params: _M_aruba_central_airmatch_get_all_ap_coverage_plan) -> str:
        """Get all AP coverage plan from collection.

        Spec: services | GET /network-services/v1/airmatch-ap-coverage-plan
        Query params: id, limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-ap-coverage-plan"
            p = {k: v for k, v in {
                "id": params.id,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_airmatch_migration_state_get_req(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        limit: Optional[int] = Field(None, description="Limit for pagination of results")
        offset: Optional[int] = Field(None, description="Offset for pagination of results")

    @mcp.tool(name="aruba_central_airmatch_migration_state_get_req",
              annotations={"title": "Get migration state for a tenant", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_airmatch_migration_state_get_req(params: _M_aruba_central_airmatch_migration_state_get_req) -> str:
        """Get migration state for a tenant.

        Spec: services | GET /network-services/v1/airmatch-state
        Query params: limit, offset
        """
        try:
            url = "/network-services/v1/airmatch-state"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getfirmwaredetailslistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        limit: Optional[str] = Field(None, description="Denotes the maximum number of items returned in the response. Maximum value is 1000. ")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources. The minimum value is 1. ")

    @mcp.tool(name="aruba_central_getfirmwaredetailslistv1",
              annotations={"title": "Get device list with firmware details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getfirmwaredetailslistv1(params: _M_aruba_central_getfirmwaredetailslistv1) -> str:
        """Get device list with firmware details.

        Spec: services | GET /network-services/v1/firmware-details
        Query params: limit, next
        """
        try:
            url = "/network-services/v1/firmware-details"
            p = {k: v for k, v in {
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_startaprangingscanv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="The Site ID where the scan(s) were executed. ")
        floor_id: str = Field(..., description="The Floor ID where the scan(s) were executed. ")
        dry_run: Optional[bool] = Field(None, description="If present, the scan will not be started, but the request will be validated. ")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_startaprangingscanv1",
              annotations={"title": "Start an AP ranging scan (USE WITH CAUTION)", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_startaprangingscanv1(params: _M_aruba_central_startaprangingscanv1) -> str:
        """Start an AP ranging scan (USE WITH CAUTION).

        Spec: services | POST /network-services/v1/ap-ranging-scans
        Query params: site-id, floor-id, dry-run
        """
        try:
            url = "/network-services/v1/ap-ranging-scans"
            p = {k: v for k, v in {
                "site-id": params.site_id,
                "floor-id": params.floor_id,
                "dry-run": params.dry_run,
            }.items() if v is not None}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaprangingscanlistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        limit: Optional[int] = Field(None, description="limit")
        next: Optional[str] = Field(None, description="next")

    @mcp.tool(name="aruba_central_getaprangingscanlistv1",
              annotations={"title": "List AP ranging scans", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaprangingscanlistv1(params: _M_aruba_central_getaprangingscanlistv1) -> str:
        """List AP ranging scans.

        Spec: services | GET /network-services/v1/sitemaps/{site-id}/floors/{floor-id}/ap-ranging-scans
        Query params: limit, next
        """
        try:
            url = f"/network-services/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/ap-ranging-scans"
            p = {k: v for k, v in {
                "limit": params.limit,
                "next": params.next,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaprangingscanv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        scan_id: str = Field(..., description="scan-id")

    @mcp.tool(name="aruba_central_getaprangingscanv1",
              annotations={"title": "Get scan resource", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaprangingscanv1(params: _M_aruba_central_getaprangingscanv1) -> str:
        """Get scan resource.

        Spec: services | GET /network-services/v1/sitemaps/{site-id}/floors/{floor-id}/ap-ranging-scans/{scan-id}
        """
        try:
            url = f"/network-services/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/ap-ranging-scans/{params.scan_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_stopaprangingscanv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        site_id: str = Field(..., description="site-id")
        floor_id: str = Field(..., description="floor-id")
        scan_id: str = Field(..., description="scan-id")

    @mcp.tool(name="aruba_central_stopaprangingscanv1",
              annotations={"title": "Stop a scan", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_stopaprangingscanv1(params: _M_aruba_central_stopaprangingscanv1) -> str:
        """Stop a scan.

        Spec: services | DELETE /network-services/v1/sitemaps/{site-id}/floors/{floor-id}/ap-ranging-scans/{scan-id}
        """
        try:
            url = f"/network-services/v1/sitemaps/{params.site_id}/floors/{params.floor_id}/ap-ranging-scans/{params.scan_id}"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_listclientlocationsforapiv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        filter: Optional[str] = Field(None, description="This is required parameter if latest-location-per-client parameter is used. OData Version 4.0 filter string (limited fun")
        start_at: Optional[int] = Field(None, description="Retrieve data starting at the specified timestamp. Provided in RFC 3339 format. Example: `2023-01-01T23:10:41.123Z`. If ")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of clients returned in the response. (Default: 100) ")
        offset: Optional[int] = Field(None, description="Specifies the zero-based resource offset to start the page from. Default: 0 ")
        latest_location_per_client: Optional[int] = Field(None, description="Provides a list of latest client locations. Only the value of 1 is supported for the moment. It is mutually exclusive fr")
        latest_connected_client_mac: Optional[str] = Field(None, description="Provides the latest location information for a specific client that is connected and associated. Do not provide filter, ")

    @mcp.tool(name="aruba_central_listclientlocationsforapiv1",
              annotations={"title": "Get locations of Wi-Fi clients", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_listclientlocationsforapiv1(params: _M_aruba_central_listclientlocationsforapiv1) -> str:
        """Get locations of Wi-Fi clients.

        Spec: services | GET /network-services/v1/wifi-clients-locations
        Query params: filter, start-at, limit, offset, latest-location-per-client, latest-connected-client-mac
        """
        try:
            url = "/network-services/v1/wifi-clients-locations"
            p = {k: v for k, v in {
                "filter": params.filter,
                "start-at": params.start_at,
                "limit": params.limit,
                "offset": params.offset,
                "latest-location-per-client": params.latest_location_per_client,
                "latest-connected-client-mac": params.latest_connected_client_mac,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_listassettagdatav1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        filter: Optional[str] = Field(None, description="OData 4.0 filter (limited functionality). Supports filtering on field `metadata/labels` only. ")
        mac_address: Optional[str] = Field(None, description="MAC address of the Asset Tag.  Note: The filter, sort, limit, and offset parameters are not applicable if the MAC-addres")
        start_at: Optional[str] = Field(None, description="Retrieve data starting at the specified timestamp. Provided in RFC 3339 format. Example: `2023-01-01T23:10:41.123Z`. If ")
        limit: Optional[int] = Field(None, description="Denotes the maximum number of Asset Tags returned in the response. (Default: 100) ")
        offset: Optional[int] = Field(None, description="Specifies the zero-based resource offset from which to start the page. (Default: 0) ")
        sort: Optional[str] = Field(None, description="Comma-separated list of sort expressions. Each sort expression is a property name optionally followed by a direction ind")

    @mcp.tool(name="aruba_central_listassettagdatav1",
              annotations={"title": "Get a list of Asset Tags", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_listassettagdatav1(params: _M_aruba_central_listassettagdatav1) -> str:
        """Get a list of Asset Tags.

        Spec: services | GET /network-services/v1/asset-tags
        Query params: filter, mac-address, start-at, limit, offset, sort
        """
        try:
            url = "/network-services/v1/asset-tags"
            p = {k: v for k, v in {
                "filter": params.filter,
                "mac-address": params.mac_address,
                "start-at": params.start_at,
                "limit": params.limit,
                "offset": params.offset,
                "sort": params.sort,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getassettagdatabyassettagidv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        asset_tag_id: str = Field(..., description="asset-tag-id")

    @mcp.tool(name="aruba_central_getassettagdatabyassettagidv1",
              annotations={"title": "Get Asset Tag details", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getassettagdatabyassettagidv1(params: _M_aruba_central_getassettagdatabyassettagidv1) -> str:
        """Get Asset Tag details.

        Spec: services | GET /network-services/v1/asset-tags/{asset-tag-id}
        """
        try:
            url = f"/network-services/v1/asset-tags/{params.asset_tag_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_createassettagdatabyassettagidv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        asset_tag_id: str = Field(..., description="asset-tag-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_createassettagdatabyassettagidv1",
              annotations={"title": "Create Asset Tag metadata", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_createassettagdatabyassettagidv1(params: _M_aruba_central_createassettagdatabyassettagidv1) -> str:
        """Create Asset Tag metadata.

        Spec: services | POST /network-services/v1/asset-tags/{asset-tag-id}/metadata
        """
        try:
            url = f"/network-services/v1/asset-tags/{params.asset_tag_id}/metadata"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updateassettagdatabyassettagidv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        asset_tag_id: str = Field(..., description="asset-tag-id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updateassettagdatabyassettagidv1",
              annotations={"title": "Update Asset Tag metadata", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updateassettagdatabyassettagidv1(params: _M_aruba_central_updateassettagdatabyassettagidv1) -> str:
        """Update Asset Tag metadata.

        Spec: services | PUT /network-services/v1/asset-tags/{asset-tag-id}/metadata
        """
        try:
            url = f"/network-services/v1/asset-tags/{params.asset_tag_id}/metadata"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deleteassettagdatabyassettagidv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        asset_tag_id: str = Field(..., description="asset-tag-id")

    @mcp.tool(name="aruba_central_deleteassettagdatabyassettagidv1",
              annotations={"title": "Remove Asset Tag metadata", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deleteassettagdatabyassettagidv1(params: _M_aruba_central_deleteassettagdatabyassettagidv1) -> str:
        """Remove Asset Tag metadata.

        Spec: services | DELETE /network-services/v1/asset-tags/{asset-tag-id}/metadata
        """
        try:
            url = f"/network-services/v1/asset-tags/{params.asset_tag_id}/metadata"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getauditbyidv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: str = Field(..., description="id")

    @mcp.tool(name="aruba_central_getauditbyidv1",
              annotations={"title": "Get Audit log based on the audit id.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getauditbyidv1(params: _M_aruba_central_getauditbyidv1) -> str:
        """Get Audit log based on the audit id..

        Spec: services | GET /network-services/v1/audits/{id}
        """
        try:
            url = f"/network-services/v1/audits/{params.id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_listauditsv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        start_at: str = Field(..., description="Data is required starting from this timestamp, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milli")
        end_at: str = Field(..., description="Data is required up to this timestamp, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milliseconds.")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="Comma separated list of sort expressions. Each sort expression is a property name optionally followed by a direction ind")
        limit: Optional[int] = Field(None, description="Specifies the maximum number of Audits returned in the response list. ")
        offset: Optional[int] = Field(None, description="Number of items to skip before returning results. ")

    @mcp.tool(name="aruba_central_listauditsv1",
              annotations={"title": "Get audit logs belonging to the tenant.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_listauditsv1(params: _M_aruba_central_listauditsv1) -> str:
        """Get audit logs belonging to the tenant..

        Spec: services | GET /network-services/v1/audits
        Query params: start-at, end-at, filter, sort, limit, offset
        """
        try:
            url = "/network-services/v1/audits"
            p = {k: v for k, v in {
                "start-at": params.start_at,
                "end-at": params.end_at,
                "filter": params.filter,
                "sort": params.sort,
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_fco_get_afc_resp_info(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_fco_get_afc_resp_info",
              annotations={"title": "Get AFC channel data of a specific AP.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_fco_get_afc_resp_info(params: _M_aruba_central_fco_get_afc_resp_info) -> str:
        """Get AFC channel data of a specific AP..

        Spec: services | GET /network-services/v1/fco-resp-info/{serial-number}
        """
        try:
            url = f"/network-services/v1/fco-resp-info/{params.serial_number}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_fco_get_all_afc_resp_info(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        limit: Optional[str] = Field(None, description="The maximum number of items to return.")
        offset: Optional[str] = Field(None, description="The offset of the first item in the collection to return.")

    @mcp.tool(name="aruba_central_fco_get_all_afc_resp_info",
              annotations={"title": "Get AFC channel data for all access points belonging to the tenant.", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_fco_get_all_afc_resp_info(params: _M_aruba_central_fco_get_all_afc_resp_info) -> str:
        """Get AFC channel data for all access points belonging to the tenant..

        Spec: services | GET /network-services/v1/fco-resp-info-all
        Query params: limit, offset
        """
        try:
            url = "/network-services/v1/fco-resp-info-all"
            p = {k: v for k, v in {
                "limit": params.limit,
                "offset": params.offset,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getwebhooksv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        pass

    @mcp.tool(name="aruba_central_getwebhooksv1",
              annotations={"title": "List all Webhooks", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getwebhooksv1(params: _M_aruba_central_getwebhooksv1) -> str:
        """List all Webhooks.

        Spec: services | GET /network-services/v1/webhooks
        """
        try:
            url = "/network-services/v1/webhooks"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_createwebhookv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_createwebhookv1",
              annotations={"title": "Create a Webhook", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_createwebhookv1(params: _M_aruba_central_createwebhookv1) -> str:
        """Create a Webhook.

        Spec: services | POST /network-services/v1/webhooks
        """
        try:
            url = "/network-services/v1/webhooks"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getwebhookv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: str = Field(..., description="id")

    @mcp.tool(name="aruba_central_getwebhookv1",
              annotations={"title": "Get a Webhook details by ID", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getwebhookv1(params: _M_aruba_central_getwebhookv1) -> str:
        """Get a Webhook details by ID.

        Spec: services | GET /network-services/v1/webhooks/{id}
        """
        try:
            url = f"/network-services/v1/webhooks/{params.id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_updatewebhookv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: str = Field(..., description="id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_updatewebhookv1",
              annotations={"title": "Update a Webhook by ID", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_updatewebhookv1(params: _M_aruba_central_updatewebhookv1) -> str:
        """Update a Webhook by ID.

        Spec: services | PUT /network-services/v1/webhooks/{id}
        """
        try:
            url = f"/network-services/v1/webhooks/{params.id}"
            p = {}
            data = await api_fn("PUT", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_patchwebhookv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: str = Field(..., description="id")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_patchwebhookv1",
              annotations={"title": "Patch a Webhook by ID", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_patchwebhookv1(params: _M_aruba_central_patchwebhookv1) -> str:
        """Patch a Webhook by ID.

        Spec: services | PATCH /network-services/v1/webhooks/{id}
        """
        try:
            url = f"/network-services/v1/webhooks/{params.id}"
            p = {}
            data = await api_fn("PATCH", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_deletewebhookv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: str = Field(..., description="id")

    @mcp.tool(name="aruba_central_deletewebhookv1",
              annotations={"title": "Delete a Webhook by ID", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_deletewebhookv1(params: _M_aruba_central_deletewebhookv1) -> str:
        """Delete a Webhook by ID.

        Spec: services | DELETE /network-services/v1/webhooks/{id}
        """
        try:
            url = f"/network-services/v1/webhooks/{params.id}"
            p = {}
            data = await api_fn("DELETE", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_rotatewebhookhmackeyv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        id: str = Field(..., description="id")

    @mcp.tool(name="aruba_central_rotatewebhookhmackeyv1",
              annotations={"title": "Rotate HMAC key for a Webhook by ID", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_rotatewebhookhmackeyv1(params: _M_aruba_central_rotatewebhookhmackeyv1) -> str:
        """Rotate HMAC key for a Webhook by ID.

        Spec: services | POST /network-services/v1/webhooks/{id}/rotate-hmac-key
        """
        try:
            url = f"/network-services/v1/webhooks/{params.id}/rotate-hmac-key"
            p = {}
            data = await api_fn("POST", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_eventlistv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        context_type: str = Field(..., description="Type of context (SITE, ACCESS_POINT, SWITCH, GATEWAY, WIRELESS_CLIENT, WIRED_CLIENT, BRIDGE). [SITE, ACCESS_POINT, SWITCH, GATEWAY, WIRELESS_CLIENT]")
        context_identifier: str = Field(..., description="Context Identifier (site ID, device serial number or client MAC address).")
        start_at: str = Field(..., description="Data is required starting from this timestamp, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milli")
        end_at: str = Field(..., description="Data is required up to this timestamp, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milliseconds.")
        site_id: str = Field(..., description="Site ID to filter the event details for a specific site.")
        search: Optional[str] = Field(None, description="Search events by name, serial number, host name, client MAC address or device MAC address. Full text search is not suppo")
        filter: Optional[str] = Field(None, description="OData Version 4.0 filter string (limited functionality). Supports only 'and' conjunction ('or' and 'not' are NOT support")
        sort: Optional[str] = Field(None, description="Sort expressions. A sort expression is a property name optionally followed by a direction indicator asc (ascending) or d")
        next: Optional[str] = Field(None, description="Specifies the pagination cursor for the next page of resources. Minimum value is 1.")
        limit: int = Field(..., description="Maximum number of events to be retrieved. Allowed range is 1 to 1000.")

    @mcp.tool(name="aruba_central_eventlistv1",
              annotations={"title": "List Events", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_eventlistv1(params: _M_aruba_central_eventlistv1) -> str:
        """List Events.

        Spec: troubleshooting | GET /network-troubleshooting/v1/events
        Query params: context-type, context-identifier, start-at, end-at, site-id, search, filter, sort, next, limit
        """
        try:
            url = "/network-troubleshooting/v1/events"
            p = {k: v for k, v in {
                "context-type": params.context_type,
                "context-identifier": params.context_identifier,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "site-id": params.site_id,
                "search": params.search,
                "filter": params.filter,
                "sort": params.sort,
                "next": params.next,
                "limit": params.limit,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_eventextraattributesv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        event_identifier: str = Field(..., description="Unique identifier of the event to retrieve details for.")
        site_id: str = Field(..., description="Site ID to filter the event details for a specific site.")
        time_at: str = Field(..., description="Timestamp of when the event occurred, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milliseconds.")

    @mcp.tool(name="aruba_central_eventextraattributesv1",
              annotations={"title": "Get Event Extra Attributes", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_eventextraattributesv1(params: _M_aruba_central_eventextraattributesv1) -> str:
        """Get Event Extra Attributes.

        Spec: troubleshooting | GET /network-troubleshooting/v1/event-extra-attributes
        Query params: event-identifier, site-id, time-at
        """
        try:
            url = "/network-troubleshooting/v1/event-extra-attributes"
            p = {k: v for k, v in {
                "event-identifier": params.event_identifier,
                "site-id": params.site_id,
                "time-at": params.time_at,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_eventfiltersv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        context_type: str = Field(..., description="Type of context (SITE, ACCESS_POINT, SWITCH, GATEWAY, WIRELESS_CLIENT, WIRED_CLIENT, BRIDGE). [SITE, ACCESS_POINT, SWITCH, GATEWAY, WIRELESS_CLIENT]")
        context_identifier: str = Field(..., description="Context Identifier (site ID, device serial number or client MAC address).")
        start_at: str = Field(..., description="Data is required starting from this timestamp, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milli")
        end_at: str = Field(..., description="Data is required up to this timestamp, provided in RFC 3339 (and ISO 8601) format in the UTC timezone with milliseconds.")
        site_id: str = Field(..., description="Site ID to filter the event details for a specific site.")

    @mcp.tool(name="aruba_central_eventfiltersv1",
              annotations={"title": "Get Event Filters", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_eventfiltersv1(params: _M_aruba_central_eventfiltersv1) -> str:
        """Get Event Filters.

        Spec: troubleshooting | GET /network-troubleshooting/v1/event-filters
        Query params: context-type, context-identifier, start-at, end-at, site-id
        """
        try:
            url = "/network-troubleshooting/v1/event-filters"
            p = {k: v for k, v in {
                "context-type": params.context_type,
                "context-identifier": params.context_identifier,
                "start-at": params.start_at,
                "end-at": params.end_at,
                "site-id": params.site_id,
            }.items() if v is not None}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getappingresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getappingresultv1",
              annotations={"title": "Get AP Ping test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getappingresultv1(params: _M_aruba_central_getappingresultv1) -> str:
        """Get AP Ping test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/ping/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/ping/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaptracerouteresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getaptracerouteresultv1",
              annotations={"title": "Get AP Traceroute test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaptracerouteresultv1(params: _M_aruba_central_getaptracerouteresultv1) -> str:
        """Get AP Traceroute test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/traceroute/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/traceroute/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getapspeedtestresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getapspeedtestresultv1",
              annotations={"title": "Get AP Speedtest status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getapspeedtestresultv1(params: _M_aruba_central_getapspeedtestresultv1) -> str:
        """Get AP Speedtest status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/speedtest/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/speedtest/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaphttpresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getaphttpresultv1",
              annotations={"title": "Get AP HTTP test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaphttpresultv1(params: _M_aruba_central_getaphttpresultv1) -> str:
        """Get AP HTTP test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/http/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/http/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaphttpsresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getaphttpsresultv1",
              annotations={"title": "Get AP HTTPS test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaphttpsresultv1(params: _M_aruba_central_getaphttpsresultv1) -> str:
        """Get AP HTTPS test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/https/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/https/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaptcpresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getaptcpresultv1",
              annotations={"title": "Get AP TCP test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaptcpresultv1(params: _M_aruba_central_getaptcpresultv1) -> str:
        """Get AP TCP test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/tcp/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/tcp/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getapgetarptableresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getapgetarptableresultv1",
              annotations={"title": "Get AP Get Arp Table test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getapgetarptableresultv1(params: _M_aruba_central_getapgetarptableresultv1) -> str:
        """Get AP Get Arp Table test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/getArpTable/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/getArpTable/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getapnslookupresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getapnslookupresultv1",
              annotations={"title": "Get AP Nslookup test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getapnslookupresultv1(params: _M_aruba_central_getapnslookupresultv1) -> str:
        """Get AP Nslookup test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/nslookup/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/nslookup/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_initiateapaaav1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        body: Optional[Dict[str, Any]] = Field(None, description="Request body as JSON object")

    @mcp.tool(name="aruba_central_initiateapaaav1",
              annotations={"title": "Initiate an AAA test on an AP", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_initiateapaaav1(params: _M_aruba_central_initiateapaaav1) -> str:
        """Initiate an AAA test on an AP.

        Spec: troubleshooting | POST /network-troubleshooting/v1/aps/{serial-number}/aaa
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/aaa"
            p = {}
            data = await api_fn("POST", url, params=p, json=params.body or {})
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getapaaaresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getapaaaresultv1",
              annotations={"title": "Get AP AAA test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getapaaaresultv1(params: _M_aruba_central_getapaaaresultv1) -> str:
        """Get AP AAA test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/aaa/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/aaa/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getapshowcommandsresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getapshowcommandsresultv1",
              annotations={"title": "Get 'show' commands status/result (AP)", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getapshowcommandsresultv1(params: _M_aruba_central_getapshowcommandsresultv1) -> str:
        """Get 'show' commands status/result (AP).

        Spec: troubleshooting | GET /network-troubleshooting/v1/aps/{serial-number}/showCommands/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aps/{params.serial_number}/showCommands/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxpingresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxpingresultv1",
              annotations={"title": "Get CX Switch Ping test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxpingresultv1(params: _M_aruba_central_getcxpingresultv1) -> str:
        """Get CX Switch Ping test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/ping/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/ping/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxtracerouteresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxtracerouteresultv1",
              annotations={"title": "Get CX Switch Traceroute test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxtracerouteresultv1(params: _M_aruba_central_getcxtracerouteresultv1) -> str:
        """Get CX Switch Traceroute test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/traceroute/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/traceroute/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxpoebounceresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxpoebounceresultv1",
              annotations={"title": "Get CX Switch Poe Bounce test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxpoebounceresultv1(params: _M_aruba_central_getcxpoebounceresultv1) -> str:
        """Get CX Switch Poe Bounce test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/poeBounce/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/poeBounce/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxportbounceresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxportbounceresultv1",
              annotations={"title": "Get CX Switch Port Bounce test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxportbounceresultv1(params: _M_aruba_central_getcxportbounceresultv1) -> str:
        """Get CX Switch Port Bounce test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/portBounce/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/portBounce/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxcabletestresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxcabletestresultv1",
              annotations={"title": "Get CX Switch Cable Test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxcabletestresultv1(params: _M_aruba_central_getcxcabletestresultv1) -> str:
        """Get CX Switch Cable Test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/cableTest/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/cableTest/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxhttpresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxhttpresultv1",
              annotations={"title": "Get CX Switch Http test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxhttpresultv1(params: _M_aruba_central_getcxhttpresultv1) -> str:
        """Get CX Switch Http test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/http/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/http/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxaaaresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxaaaresultv1",
              annotations={"title": "Get CX Switch Aaa test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxaaaresultv1(params: _M_aruba_central_getcxaaaresultv1) -> str:
        """Get CX Switch Aaa test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/aaa/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/aaa/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getcxshowcommandsresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getcxshowcommandsresultv1",
              annotations={"title": "Get 'show' commands status/result (CX)", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getcxshowcommandsresultv1(params: _M_aruba_central_getcxshowcommandsresultv1) -> str:
        """Get 'show' commands status/result (CX).

        Spec: troubleshooting | GET /network-troubleshooting/v1/cx/{serial-number}/showCommands/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/cx/{params.serial_number}/showCommands/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getpvospingresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getpvospingresultv1",
              annotations={"title": "Get AOS-S Switch Ping test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getpvospingresultv1(params: _M_aruba_central_getpvospingresultv1) -> str:
        """Get AOS-S Switch Ping test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/ping/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/ping/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getpvostracerouteresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getpvostracerouteresultv1",
              annotations={"title": "Get AOS-S Switch Traceroute test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getpvostracerouteresultv1(params: _M_aruba_central_getpvostracerouteresultv1) -> str:
        """Get AOS-S Switch Traceroute test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/traceroute/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/traceroute/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getpvospoebounceresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getpvospoebounceresultv1",
              annotations={"title": "Get AOS-S Switch Poe Bounce test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getpvospoebounceresultv1(params: _M_aruba_central_getpvospoebounceresultv1) -> str:
        """Get AOS-S Switch Poe Bounce test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/poeBounce/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/poeBounce/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getpvosportbounceresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getpvosportbounceresultv1",
              annotations={"title": "Get AOS-S Switch Port Bounce test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getpvosportbounceresultv1(params: _M_aruba_central_getpvosportbounceresultv1) -> str:
        """Get AOS-S Switch Port Bounce test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/portBounce/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/portBounce/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getpvoscabletestresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getpvoscabletestresultv1",
              annotations={"title": "Get AOS-S Switch Cable Test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getpvoscabletestresultv1(params: _M_aruba_central_getpvoscabletestresultv1) -> str:
        """Get AOS-S Switch Cable Test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/cableTest/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/cableTest/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getpvosgetarptableresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getpvosgetarptableresultv1",
              annotations={"title": "Get AOS-S Switch Get Arp Table test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getpvosgetarptableresultv1(params: _M_aruba_central_getpvosgetarptableresultv1) -> str:
        """Get AOS-S Switch Get Arp Table test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/getArpTable/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/getArpTable/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getaossshowcommandsresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getaossshowcommandsresultv1",
              annotations={"title": "Get 'show' commands status/result (AOS-S)", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getaossshowcommandsresultv1(params: _M_aruba_central_getaossshowcommandsresultv1) -> str:
        """Get 'show' commands status/result (AOS-S).

        Spec: troubleshooting | GET /network-troubleshooting/v1/aos-s/{serial-number}/showCommands/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/aos-s/{params.serial_number}/showCommands/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwpingresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwpingresultv1",
              annotations={"title": "Get Gateway Ping test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwpingresultv1(params: _M_aruba_central_getgwpingresultv1) -> str:
        """Get Gateway Ping test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/ping/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/ping/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgatewaypingsweepresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgatewaypingsweepresultv1",
              annotations={"title": "Get PingSweep status/result (Gateway)", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgatewaypingsweepresultv1(params: _M_aruba_central_getgatewaypingsweepresultv1) -> str:
        """Get PingSweep status/result (Gateway).

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/pingSweep/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/pingSweep/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwtracerouteresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwtracerouteresultv1",
              annotations={"title": "Get Gateway Traceroute test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwtracerouteresultv1(params: _M_aruba_central_getgwtracerouteresultv1) -> str:
        """Get Gateway Traceroute test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/traceroute/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/traceroute/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwpoebounceresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwpoebounceresultv1",
              annotations={"title": "Get Gateway Poe Bounce test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwpoebounceresultv1(params: _M_aruba_central_getgwpoebounceresultv1) -> str:
        """Get Gateway Poe Bounce test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/poeBounce/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/poeBounce/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwportbounceresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwportbounceresultv1",
              annotations={"title": "Get Gateway Port Bounce test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwportbounceresultv1(params: _M_aruba_central_getgwportbounceresultv1) -> str:
        """Get Gateway Port Bounce test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/portBounce/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/portBounce/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwiperfresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwiperfresultv1",
              annotations={"title": "Get Gateway Iperf test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwiperfresultv1(params: _M_aruba_central_getgwiperfresultv1) -> str:
        """Get Gateway Iperf test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/iperf/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/iperf/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwhttpresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwhttpresultv1",
              annotations={"title": "Get Gateway Http test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwhttpresultv1(params: _M_aruba_central_getgwhttpresultv1) -> str:
        """Get Gateway Http test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/http/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/http/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwhttpsresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwhttpsresultv1",
              annotations={"title": "Get Gateway Https test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwhttpsresultv1(params: _M_aruba_central_getgwhttpsresultv1) -> str:
        """Get Gateway Https test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/https/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/https/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwgetarptableresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwgetarptableresultv1",
              annotations={"title": "Get Gateway Get Arp Table test status and results", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwgetarptableresultv1(params: _M_aruba_central_getgwgetarptableresultv1) -> str:
        """Get Gateway Get Arp Table test status and results.

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/getArpTable/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/getArpTable/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_getgwshowcommandsresultv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")
        task_id: str = Field(..., description="task-id")

    @mcp.tool(name="aruba_central_getgwshowcommandsresultv1",
              annotations={"title": "Get 'show' commands status/result (Gateway)", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True})
    async def _aruba_central_getgwshowcommandsresultv1(params: _M_aruba_central_getgwshowcommandsresultv1) -> str:
        """Get 'show' commands status/result (Gateway).

        Spec: troubleshooting | GET /network-troubleshooting/v1/gateways/{serial-number}/showCommands/async-operations/{task-id}
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/showCommands/async-operations/{params.task_id}"
            p = {}
            data = await api_fn("GET", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)

    class _M_aruba_central_haltgatewayv1(BaseModel):
        model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
        serial_number: str = Field(..., description="serial-number")

    @mcp.tool(name="aruba_central_haltgatewayv1",
              annotations={"title": "Halt a Gateway", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True})
    async def _aruba_central_haltgatewayv1(params: _M_aruba_central_haltgatewayv1) -> str:
        """Halt a Gateway.

        Spec: troubleshooting | POST /network-troubleshooting/v1/gateways/{serial-number}/halt
        """
        try:
            url = f"/network-troubleshooting/v1/gateways/{params.serial_number}/halt"
            p = {}
            data = await api_fn("POST", url, params=p)
            return json.dumps(data, indent=2)
        except Exception as e:
            return err_fn(e)
