from backend.llm import llm
from backend.schemas import DailyPlan, TripResponse
from backend.state import TravelState
from langchain_core.messages import HumanMessage, SystemMessage

FINAL_RESPONSE_PROMPT = """You are TripMate AI. Synthesize the gathered travel data into the final structured travel response.

Trip Overview:
- Route: {origin} to {destination}
- Dates: {depart_date} to {return_date}
- Travelers: {travelers}
- Budgets: Flights ${flight_budget_usd}/person, Hotels ${hotel_budget_usd}/night

Weather Data:
{weather_result}

Flight Data:
{flight_results}

Hotel Data:
{hotel_results}

Drafted Daily Itinerary:
{itinerary}

Populate every field of the TripResponse schema:
- summary: Executive summary of the trip, total estimated cost, and vibe.
- weather: Summary of current weather, forecast, and packing essentials.
- flights: Best flight options, IATA codes, and booking advice.
- hotels: Top recommended hotels matching the ${hotel_budget_usd}/night budget.
- daily_plan: A dictionary mapping each day (e.g., "Day 1", "Day 2") to an object with "morning", "afternoon", and "evening" plans.
- tips: Local etiquette, transit cards, currency, and safety tips.
"""


async def response(state: TravelState) -> dict:
    print("\n--- [Node 5/5] Running Final Response Node (LLM Call 2) ---")

    prompt = FINAL_RESPONSE_PROMPT.format(
        origin=state["origin"],
        destination=state["destination"],
        depart_date=state["depart_date"],
        return_date=state["return_date"],
        travelers=state["travelers"],
        flight_budget_usd=state["flight_budget_usd"],
        hotel_budget_usd=state["hotel_budget_usd"],
        weather_result=state.get("weather_result", ""),
        flight_results=state.get("flight_results", ""),
        hotel_results=state.get("hotel_results", ""),
        itinerary=state.get("itinerary", ""),
    )

    messages = [
        SystemMessage(
            content="You are TripMate AI. Return a complete, valid JSON object matching the TripResponse schema."
        ),
        HumanMessage(content=prompt),
    ]

    try:
        # Enforce Pydantic TripResponse schema
        structured_llm = llm.with_structured_output(TripResponse)
        trip_response: TripResponse = await structured_llm.ainvoke(messages) # pyright: ignore[reportAssignmentType]
    except Exception as exc:  # noqa: BLE001
        print(f"[Response] Structured output fallback triggered: {exc}")
        # Graceful fallback if a small local model fails strict JSON schema validation
        trip_response = TripResponse(
            summary=f"Trip from {state['origin']} to {state['destination']} ({state['depart_date']} to {state['return_date']}) for {state['travelers']} traveler(s).",
            weather=state.get("weather_result", ""),
            flights=state.get("flight_results", ""),
            hotels=state.get("hotel_results", ""),
            daily_plan={
                "Day 1": DailyPlan(
                    morning="Arrive, check in, and explore the neighborhood.",
                    afternoon=state.get(
                        "itinerary", "Local sightseeing and cultural landmarks."
                    )[:300],
                    evening="Welcome dinner at a local specialty restaurant.",
                )
            },
            tips="Carry a universal adapter, register for local transit passes, and book major attractions in advance.",
        )

    return {
        "final_response": trip_response,
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
