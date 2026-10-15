from datetime import UTC, date, datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TravelRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
    )

    origin: str = Field(
        min_length=2,
        max_length=100,
        description="Departure city or airport",
        examples=["Colombo", "CMB"],
    )

    destination: str = Field(
        min_length=2,
        max_length=100,
        description="Arrival city or airport",
        examples=["Tokyo", "NRT"],
    )

    depart_date: date = Field(
        description="Travel departure date",
    )

    return_date: date = Field(
        description="Travel return date",
    )

    flight_budget_usd: int = Field(
        gt=0,
        le=100_000,
        description="Total flight budget in USD",
    )

    hotel_budget_usd: int = Field(
        gt=0,
        le=100_000,
        description="Total hotel budget in USD",
    )

    travelers: int = Field(
        ge=1,
        le=20,
        description="Number of travelers",
    )

    @field_validator("origin", "destination", mode="before")
    @classmethod
    def normalize_location(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("origin", "destination")
    @classmethod
    def validate_location(cls, value: str) -> str:
        if not any(char.isalnum() for char in value):
            raise ValueError("Location must contain letters or numbers")
        return value

    @field_validator("depart_date", "return_date", mode="before")
    @classmethod
    def reject_datetime_for_date(cls, value: object) -> object:
        if isinstance(value, datetime):
            raise TypeError("Provide a date, not a datetime")
        return value

    @model_validator(mode="after")
    def validate_trip(self)  -> Self:
        if self.origin.casefold() == self.destination.casefold():
            raise ValueError("Origin and destination must be different")

        if self.depart_date < datetime.now(tz=UTC).date():
            raise ValueError("Departure date cannot be in the past")

        if self.return_date < self.depart_date:
            raise ValueError("Return date must be on or after departure")

        return self


class DailyPlan(BaseModel):
    morning: str
    afternoon: str
    evening: str


class TripResponse(BaseModel):
    summary: str
    weather: str
    flights: str
    hotels: str
    daily_plan: dict[str, DailyPlan]
    tips: str


class ToolException(Exception):
    pass
