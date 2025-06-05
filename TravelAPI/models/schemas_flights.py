from fastapi.openapi.models import Schema
from pydantic import BaseModel, Field, validator, model_validator
from typing import Optional


class FlightSearchParams(BaseModel):
    originLocationCode: str = Field(..., description="IATA код отправления")
    destinationLocationCode: str = Field(..., description="IATA код назначения")
    departureDate: str = Field(..., pattern=r"\d{4}-\d{2}-\d{2}", description="Дата вылета YYYY-MM-DD")
    returnDate: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Дата возврата YYYY-MM-DD"
    )
    adults: int = Field(1, ge=1, le=9)
    children: Optional[int] = Field(0, ge=0, le=9)
    infants: Optional[int] = Field(0, ge=0)
    travelClass: Optional[str] = Field(None, pattern=r"(ECONOMY|PREMIUM_ECONOMY|BUSINESS|FIRST)")
    includedAirlineCodes: Optional[str] = None
    excludedAirlineCodes: Optional[str] = None
    nonStop: bool = False
    currencyCode: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{3}$",
        description="Валюта по ISO 4217 (например, EUR)"
    )
    maxPrice: Optional[int] = Field(None, ge=0)
    max: int = Field(250, ge=1, le=250)

    @validator('infants')
    def check_infants_not_more_than_adults(cls, v, values):
        if 'adults' in values and v > values['adults']:
            raise ValueError('Infants cannot exceed number of adults')
        return v


# class FlightDestinationParams(BaseModel):
#     origin: str = Field(..., description="IATA код отправления")
#     departureDate: str = Field(..., pattern=r"\d{4}-\d{2}-\d{2}", description="Дата вылета YYYY-MM-DD")
#     oneWay: bool = False
#     duration: Optional[int] = Field(None)
#     nonStop: bool = False
#     maxPrice: Optional[int] = Field(None, ge=0)
#     viewBy: Optional[str] = Field(
#         None,
#         pattern=r"^(DATE|DESTINATION|DURATION|WEEK|COUNTRY)$",
#         description="Как группировать результаты. По умолчанию DATE (если oneWay=True), иначе DURATION."
#     )
#
#     @model_validator(mode='after')
#     def set_default_view_by(self):
#         if self.viewBy is None:
#             if self.oneWay:
#                 self.viewBy = "DATE"
#             else:
#                 self.viewBy = "DURATION"
#         return self


class AirlineDestinationParams(BaseModel):
    airlineCode: str = Field(
        ...,
        pattern=r"^[A-Z0-9]{2}$",
        description="IATA код авиакомпании"
    )#BA
    arrivalCountryCode: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{2}$",
        description="IATA код страны назначения"
    )
    max: int = Field(50, ge=1, le=500)