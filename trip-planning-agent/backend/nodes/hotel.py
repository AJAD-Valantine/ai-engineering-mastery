import json

from backend.mcp_setup.client import get_tool
from backend.schemas import ToolException
from backend.state import TravelState


def _parse_tavily_output(res) -> list:
    """Extract results list from Tavily MCP response."""
    if isinstance(res, str):
        try:
            res = json.loads(res)
        except json.JSONDecodeError:
            return [{"title": "Tavily Search Result", "url": "", "content": res}]
    if isinstance(res, dict):
        return res.get("results", [])
    if isinstance(res, list):
        return res
    return []


async def hotel(state: TravelState) -> dict:
    print("\n--- [Node 2/5] Running Hotel Node (Parallel) ---")
    destination = state["destination"]
    budget = state["hotel_budget_usd"]
    travelers = state["travelers"]
    depart_date = state["depart_date"]
    return_date = state["return_date"]
    nights = max((return_date - depart_date).days, 1)

    # Fetch Tavily tool via get_tool()
    tavily_tool = await get_tool("tavily_search") or await get_tool("tavily-search")

    raw_results = []
    if tavily_tool:
        query = (
            f"Best hotels in {destination} under ${budget} per night "
            f"for {travelers} guests ({nights} nights)"
        )
        try:
            res = await tavily_tool.ainvoke({"query": query, "max_results": 5})
            raw_results = _parse_tavily_output(res)
        except (ToolException, Exception) as e:  # noqa: BLE001
            print(f"[Hotel] Tavily MCP error: {e}")

    lines = [
        f"### Hotels in {destination}",
        f"**Max Budget:** ${budget:,}/night | **Nights:** {nights} | **Travelers:** {travelers}",
        "",
    ]

    if raw_results:
        for i, item in enumerate(raw_results[:5], 1):
            if isinstance(item, dict):
                title = item.get("title", f"Option {i}").strip()
                url = item.get("url", "").strip()
                snippet = item.get("content", item.get("snippet", "")).strip()[:220]
                lines += [
                    f"**{i}. {title}**",
                    f"  URL: {url}",
                    f"  Details: {snippet}",
                    "",
                ]
            else:
                lines.append(f"- {str(item)[:250]}")
    else:
        lines.append(
            "_Live hotel search unavailable — LLM will recommend top-rated stays within budget._"
        )

    return {"hotel_results": "\n".join(lines)}
