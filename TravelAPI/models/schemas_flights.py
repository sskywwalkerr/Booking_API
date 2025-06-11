from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any


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


class AirlineDestinationParams(BaseModel):
    airlineCode: str = Field(
        ...,
        pattern=r"^[A-Z0-9]{2}$",
        description="IATA код авиакомпании"
    )#BA
    max: int = Field(50, ge=1, le=500)
    arrivalCountryCode: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{2}$",
        description="IATA код страны назначения"
    )


class AirlineLocationParams(BaseModel):
    subType: str = Field(
        ...,
        pattern=r"^(AIRPORT|CITY|AIRPORT,CITY)$",
        description="Тип локации: AIRPORT, CITY или AIRPORT,CITY"
    )
    keyword: str = Field(
        ...,
        pattern=r"^[A-Za-z0-9./:\-'()]+$",
        description="Ключевое слово, которое должно представлять начало слова в названии или коде города или аэропорта (например, BA)"
    )
    countryCode: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{2}$",
        description="IATA код страны местоположения (например, FR)"
    )
    page_limit: Optional[int] = Field(10, ge=1, le=50, description="Лимит результатов")
    page_offset: Optional[int] = Field(0, ge=0, description="Смещение пагинации")
    sort: Optional[str] = Field(None, description="Поле для сортировки(analytics.travelers.score)")
    view: Optional[str] = Field(
        "FULL",
        pattern=r"^(LIGHT|FULL)$",
        description="Уровень детализации ответа: LIGHT или FULL"
    )

    class Config:
        allow_population_by_field_name = True
        fields = {
            "page_limit": "page[limit]",
            "page_offset": "page[offset]"
        }


class FlightOfferPricingRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="Данные предложений перелета")


class FlightOffersPriceParams(BaseModel):
    include: Optional[str] = Field(
        None,
        description="Дополнительные ресурсы: credit-card-fees,bags,other-services,detailed-fare-rules"
    )
    forceClass: Optional[bool] = Field(
        False,
        description="Принудительное использование класса бронирования"
    )
