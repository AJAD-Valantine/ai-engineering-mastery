from backend.graph import run_travel_agent
from backend.schemas import TravelRequest, TripResponse
from fastapi import FastAPI

app = FastAPI()


@app.post("/api/agent")
async def travel_planner(request_data: TravelRequest) -> TripResponse | None:
    return await run_travel_agent(request_data)
