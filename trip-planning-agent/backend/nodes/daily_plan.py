from backend.llm import llm
from backend.state import TravelState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

DAILY_PLAN_PROMPT = """Create a realistic day-by-day travel itinerary for {travelers} traveler(s) visiting {destination} from {origin}.

Trip Dates: {depart_date} to {return_date} ({total_days} days)

Destination Weather:
{weather_result}

Available Flights:
{flight_results}

Available Hotels:
{hotel_results}

Instructions:
1. Provide a plan for each day from Day 1 to Day {total_days}.
2. Break each day into Morning, Afternoon, and Evening activities.
3. Adapt outdoor vs. indoor activities to the weather forecast.
4. Include practical transit tips and local food recommendations.
5. Keep the response concise and well-structured.
"""


async def daily_plan(state: TravelState) -> dict:
    print("\n--- [Node 4/5] Running Daily Plan Node (LLM Call 1) ---")
    depart_date = state["depart_date"]
    return_date = state["return_date"]
    total_days = max((return_date - depart_date).days, 1)

    prompt = DAILY_PLAN_PROMPT.format(
        origin=state["origin"],
        destination=state["destination"],
        depart_date=depart_date,
        return_date=return_date,
        total_days=total_days,
        travelers=state["travelers"],
        weather_result=state.get("weather_result", "Seasonal conditions"),
        flight_results=state.get("flight_results", "Standard commercial routes"),
        hotel_results=state.get("hotel_results", "Standard city accommodations"),
    )

    response: AIMessage = await llm.ainvoke(
        [
            SystemMessage(
                content="You are an expert international travel planner. Design practical, time-optimized daily itineraries."
            ),
            HumanMessage(content=prompt),
        ]
    )

    return {
        "itinerary": str(response.content),
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
