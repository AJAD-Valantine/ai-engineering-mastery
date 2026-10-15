from datetime import date
from typing import TypedDict

from backend.schemas import TripResponse


class TravelState(TypedDict):
    origin: str
    destination: str
    depart_date: date
    return_date: date
    flight_budget_usd: int
    hotel_budget_usd: int
    travelers: int

    flight_results: str
    hotel_results: str
    weather_result: str
    itinerary: str
    llm_calls: int
    final_response: TripResponse | None
