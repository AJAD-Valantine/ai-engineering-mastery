import json

from backend.mcp_setup.client import get_tool
from backend.schemas import ToolException
from backend.state import TravelState

CITY_TO_IATA = {
    "new york": "JFK",
    "nyc": "JFK",
    "tokyo": "NRT",
    "london": "LHR",
    "paris": "CDG",
    "singapore": "SIN",
    "dubai": "DXB",
    "bali": "DPS",
    "bangkok": "BKK",
    "rome": "FCO",
    "barcelona": "BCN",
    "madrid": "MAD",
    "frankfurt": "FRA",
    "amsterdam": "AMS",
    "mumbai": "BOM",
    "delhi": "DEL",
    "colombo": "CMB",
    "sydney": "SYD",
    "seoul": "ICN",
    "hong kong": "HKG",
    "istanbul": "IST",
    "zurich": "ZRH",
}


def resolve_iata(name_or_code: str) -> str:
    clean = name_or_code.lower().strip()
    if len(clean) == 3 and clean.isalpha():
        return clean.upper()
    for city, iata in CITY_TO_IATA.items():
        if city in clean:
            return iata
    return clean[:3].upper()


def _parse_mcp_output(res) -> dict:
    """Safely parse MCP tool output whether it returns a dict or JSON string."""
    if isinstance(res, dict):
        return res
    if isinstance(res, str):
        try:
            return json.loads(res)
        except json.JSONDecodeError:
            return {}
    return {}


async def flight(state: TravelState) -> dict:
    print("\n--- [Node 1/5] Running Flight Node (Parallel) ---")
    origin = state["origin"]
    destination = state["destination"]
    travelers = state["travelers"]
    depart_date = state["depart_date"]
    budget = state["flight_budget_usd"]

    dep_iata = resolve_iata(origin)
    arr_iata = resolve_iata(destination)

    tool = await get_tool("search_flights")

    raw = {}
    if tool:
        try:
            res = await tool.ainvoke(
                {
                    "departure_iata": dep_iata,
                    "arrival_iata": arr_iata,
                    "limit": 5,
                }
            )
            raw = _parse_mcp_output(res)
        except (ToolException, Exception) as e:  # noqa: BLE001
            print(f"[Flight] MCP tool error: {e}")

    flights = raw.get("flights", [])

    lines = [
        f"### Flights: {origin} ({dep_iata}) → {destination} ({arr_iata})",
        f"**Departure Date:** {depart_date} | **Travelers:** {travelers} | **Budget:** ${budget}/person",
        "",
    ]

    if flights:
        for f in flights:
            lines += [
                f"- **{f.get('airline', 'Airline')}** ({f.get('flight_number', 'N/A')})",
                f"  Departs: {f.get('dep_airport')} ({f.get('dep_iata')}) at {f.get('dep_time')}",
                f"  Arrives: {f.get('arr_airport')} ({f.get('arr_iata')}) at {f.get('arr_time')}",
                f"  Status: {f.get('status', 'scheduled')}",
            ]
    else:
        lines.append(
            "_No live schedules returned — LLM will estimate realistic carriers and fares for this route._"
        )

    return {"flight_results": "\n".join(lines)}
