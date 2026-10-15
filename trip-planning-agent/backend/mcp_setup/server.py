import requests
from backend.core.config import get_settings
from backend.schemas import ToolException
from mcp.server.fastmcp import FastMCP

settings = get_settings()

mcp = FastMCP("TravelTools MCP Server")


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Fetch real-time current weather metrics for a specified destination city."""
    api_key = settings.weather_api_key.get_secret_value()

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=8,
        )
        data = response.json()

        if response.status_code != 200:
            return {
                "error": data.get("message", f"HTTP {response.status_code}"),
                "city": city,
            }

        return {
            "city": data.get("name", city),
            "country": data.get("sys", {}).get("country", ""),
            "temperature_c": data.get("main", {}).get("temp"),
            "feels_like_c": data.get("main", {}).get("feels_like"),
            "humidity_percent": data.get("main", {}).get("humidity"),
            "condition": data.get("weather", [{}])[0].get("description", "Clear"),
            "wind_speed_ms": data.get("wind", {}).get("speed"),
        }
    except (ToolException, Exception) as exc:  # noqa: BLE001
        return {"error": f"Failed to fetch weather: {exc!s}", "city": city}


@mcp.tool()
def get_forecast(city: str) -> dict:
    """Fetch 5-interval upcoming weather forecast for a specified destination city."""
    api_key = settings.weather_api_key.get_secret_value()

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=8,
        )
        data = response.json()

        if response.status_code != 200:
            return {
                "error": data.get("message", f"HTTP {response.status_code}"),
                "city": city,
            }

        forecast_entries = []
        for item in data.get("list", [])[:6]:
            forecast_entries.append(
                {
                    "datetime": item.get("dt_txt"),
                    "temperature_c": item.get("main", {}).get("temp"),
                    "weather": item.get("weather", [{}])[0].get("description", ""),
                    "humidity_percent": item.get("main", {}).get("humidity"),
                }
            )

        return {"city": city, "forecast": forecast_entries}
    except (ToolException, Exception) as exc:  # noqa: BLE001
        return {"error": f"Failed to fetch forecast: {exc!s}", "city": city}


@mcp.tool()
def search_flights(
    departure_iata: str = "", arrival_iata: str = "", limit: int = 5
) -> dict:
    """Search live flight schedules from AviationStack API using 3-letter IATA codes."""
    api_key = settings.aviationstack_api_key.get_secret_value()

    params = {"access_key": api_key, "limit": min(limit, 20)}
    if departure_iata and len(departure_iata) == 3:
        params["dep_iata"] = departure_iata.upper()
    if arrival_iata and len(arrival_iata) == 3:
        params["arr_iata"] = arrival_iata.upper()

    try:
        response = requests.get(
            settings.aviationstack_endpoint, params=params, timeout=10
        )
        data = response.json()

        if response.status_code != 200 or "data" not in data:
            return {
                "error": data.get("error", {}).get(
                    "message", f"HTTP {response.status_code}"
                ),
                "flights": [],
            }

        flights = []
        for flight in data.get("data", []):
            airline = flight.get("airline") or {}
            flight_meta = flight.get("flight") or {}
            dep = flight.get("departure") or {}
            arr = flight.get("arrival") or {}

            flights.append(
                {
                    "airline": airline.get("name") or "Commercial Airline",
                    "flight_number": flight_meta.get("iata")
                    or flight_meta.get("number")
                    or f"FLT-{departure_iata or 'DEP'}",
                    "dep_airport": dep.get("airport") or "Departure Airport",
                    "dep_iata": dep.get("iata") or departure_iata.upper() or "DEP",
                    "dep_time": dep.get("scheduled") or "Scheduled",
                    "arr_airport": arr.get("airport") or "Arrival Airport",
                    "arr_iata": arr.get("iata") or arrival_iata.upper() or "ARR",
                    "arr_time": arr.get("scheduled") or "Scheduled",
                    "status": flight.get("flight_status") or "scheduled",
                }
            )

        return {"flights": flights, "count": len(flights)}
    except (ToolException, Exception) as exc:  # noqa: BLE001
        return {"error": f"Flight search failed: {exc!s}", "flights": []}


if __name__ == "__main__":
    mcp.run()
