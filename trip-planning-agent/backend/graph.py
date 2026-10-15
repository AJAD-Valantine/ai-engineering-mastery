from backend.core.config import get_settings
from backend.nodes.daily_plan import daily_plan
from backend.nodes.flight import flight
from backend.nodes.hotel import hotel
from backend.nodes.response import response
from backend.nodes.weather import weather
from backend.schemas import TravelRequest, TripResponse
from backend.state import TravelState
from langgraph.graph import END, START, StateGraph

settings = get_settings()

graph = StateGraph(TravelState)

graph.add_node("flight", flight)
graph.add_node("hotel", hotel)
graph.add_node("weather", weather)
graph.add_node("daily_plan", daily_plan)
graph.add_node("response", response)

graph.add_edge(START, "flight")
graph.add_edge(START, "hotel")
graph.add_edge(START, "weather")

graph.add_edge("flight", "daily_plan")
graph.add_edge("hotel", "daily_plan")
graph.add_edge("weather", "daily_plan")

graph.add_edge("daily_plan", "response")
graph.add_edge("response", END)

travel_graph = graph.compile()


async def run_travel_agent(request: TravelRequest):
    """Executes the parallel 5-node LangGraph workflow asynchronously."""

    initial_state: TravelState = {
        "origin": request.origin.strip(),
        "destination": request.destination.strip(),
        "depart_date": request.depart_date,
        "return_date": request.return_date,
        "flight_budget_usd": request.flight_budget_usd,
        "hotel_budget_usd": request.hotel_budget_usd,
        "travelers": request.travelers,
        "flight_results": "",
        "hotel_results": "",
        "weather_result": "",
        "itinerary": "",
        "llm_calls": 0,
        "final_response": None,
    }

    # Must use ainvoke() because all node functions are async
    result = await travel_graph.ainvoke(
        initial_state,
    )

    final_response: TripResponse | None = result.get("final_response")

    return final_response
