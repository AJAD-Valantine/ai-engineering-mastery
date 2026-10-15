import json

from backend.mcp_setup.client import get_tool
from backend.schemas import ToolException
from backend.state import TravelState


def _parse_mcp_output(res) -> dict:
    if isinstance(res, dict):
        return res
    if isinstance(res, str):
        try:
            return json.loads(res)
        except json.JSONDecodeError:
            return {}
    return {}


async def weather(state: TravelState) -> dict:
    print("\n--- [Node 3/5] Running Weather Node (Parallel) ---")
    destination = state["destination"]

    current_tool = await get_tool("get_current_weather")
    forecast_tool = await get_tool("get_forecast")

    current, forecast = {}, {}

    if current_tool:
        try:
            res = await current_tool.ainvoke({"city": destination})
            current = _parse_mcp_output(res)
        except (ToolException, Exception) as e:  # noqa: BLE001
            print(f"[Weather] Current weather MCP error: {e}")

    if forecast_tool:
        try:
            res = await forecast_tool.ainvoke({"city": destination})
            forecast = _parse_mcp_output(res)
        except (ToolException, Exception) as e:  # noqa: BLE001
            print(f"[Weather] Forecast MCP error: {e}")

    lines = [f"### Weather in {destination}"]

    if current and "error" not in current:
        lines += [
            f"- **Temperature:** {current.get('temperature_c')}°C (Feels like {current.get('feels_like_c')}°C)",
            f"- **Condition:** {str(current.get('condition', 'Clear')).title()}",
            f"- **Humidity:** {current.get('humidity_percent')}%",
            f"- **Wind Speed:** {current.get('wind_speed_ms')} m/s",
        ]
    else:
        lines.append(
            "- Live weather unavailable — LLM will use seasonal climate averages."
        )

    forecast_list = forecast.get("forecast", []) if isinstance(forecast, dict) else []
    if forecast_list:
        lines.append("\n**Upcoming Forecast (3-hour intervals):**")
        for entry in forecast_list:
            # Matches the "weather" key returned by get_forecast in server.py
            cond = str(entry.get("weather", "")).title()
            lines.append(
                f"- {entry.get('datetime')}: {entry.get('temperature_c')}°C, {cond}"
            )

    return {"weather_result": "\n".join(lines)}
