from __future__ import annotations
from typing import Literal, Union
from pydantic import BaseModel


class Pin(BaseModel):
    x: float
    y: float


class CityState(BaseModel):
    name: str
    temp_c: int
    condition: str
    emoji: str
    current_stock_units: int
    current_price_eur: float
    recommended_price_eur: float
    price_delta_pct: float
    last_comparable_units: int
    pin: Pin


class ForecastCity(BaseModel):
    temp_c: int
    emoji: str


class ForecastDay(BaseModel):
    day: str
    dublin: ForecastCity
    cork: ForecastCity


class LastComparable(BaseModel):
    label: str
    date: str
    note: str


class Reallocation(BaseModel):
    from_city: str
    to_city: str
    units: int
    departs: str
    arrives: str


class Impact(BaseModel):
    margin_eur: int
    waste_kg: int
    sell_through_pct: int


class LineEvidence(BaseModel):
    type: Literal["line"]
    label: str
    points: list[int]


class BarEntry(BaseModel):
    label: str
    dublin: int
    cork: int


class BarEvidence(BaseModel):
    type: Literal["bar"]
    label: str
    bars: list[BarEntry]


class StatEvidence(BaseModel):
    type: Literal["stat"]
    label: str
    dublin: str
    cork: str


WhyEvidence = Union[LineEvidence, BarEvidence, StatEvidence]


class WhyBullet(BaseModel):
    claim: str
    source: str
    evidence: WhyEvidence


class Cities(BaseModel):
    dublin: CityState
    cork: CityState


class BbqScenario(BaseModel):
    headline: str
    summary: str
    cities: Cities
    forecast: list[ForecastDay]
    last_comparable: LastComparable
    reallocation: Reallocation
    actions: list[str]
    impact: Impact
    why: list[WhyBullet]


class Insight(BaseModel):
    id: Literal["bbq", "heatwave", "sixnations"]
    icon: str
    title: str
    subtitle: str
    selected: bool
    available: bool


class Scenario(BaseModel):
    greeting: str
    subgreeting: str
    monitoring_label: str
    insights: list[Insight]
    bbq: BbqScenario


class ApproveRequest(BaseModel):
    insight_id: str


class ApproveResponse(BaseModel):
    message: str
