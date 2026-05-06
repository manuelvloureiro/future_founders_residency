from models import (
    Scenario, Insight, BbqScenario, Cities, CityState, Pin,
    ForecastDay, ForecastCity, LastComparable, Reallocation,
    Impact, WhyBullet, LineEvidence, BarEvidence, BarEntry, StatEvidence,
)

scenario = Scenario(
    greeting="Good morning, Keith.",
    subgreeting="3 strategic insights.",
    monitoring_label="IDM · monitoring · updated 2 min ago",
    insights=[
        Insight(id="sixnations", icon="🏉", title="Six Nations game", subtitle="Snacks / beer uplift", selected=False, available=True),
        Insight(id="bbq", icon="🔥", title="Barbecue weekend", subtitle="Dublin / Cork divergence", selected=True, available=True),
        Insight(id="heatwave", icon="☀️", title="Heatwave forecast", subtitle="Ice cream category", selected=False, available=False),
    ],
    bbq=BbqScenario(
        headline="Barbecue weekend Sat–Sun",
        summary="Dublin will be hot and dry while Cork sees rain. Without action, Dublin stocks out Saturday afternoon and Cork throws away ~180 kg of meat.",
        cities=Cities(
            dublin=CityState(
                name="Dublin",
                temp_c=24,
                condition="sunny",
                emoji="☀️",
                current_stock_units=1800,
                current_price_eur=12.50,
                recommended_price_eur=13.20,
                price_delta_pct=5.6,
                last_comparable_units=2400,
                pin=Pin(x=295, y=215),
            ),
            cork=CityState(
                name="Cork",
                temp_c=13,
                condition="rain",
                emoji="🌧️",
                current_stock_units=2400,
                current_price_eur=12.50,
                recommended_price_eur=11.40,
                price_delta_pct=-8.8,
                last_comparable_units=600,
                pin=Pin(x=215, y=395),
            ),
        ),
        forecast=[
            ForecastDay(day="Fri", dublin=ForecastCity(temp_c=21, emoji="⛅"), cork=ForecastCity(temp_c=15, emoji="🌦️")),
            ForecastDay(day="Sat", dublin=ForecastCity(temp_c=24, emoji="☀️"), cork=ForecastCity(temp_c=13, emoji="🌧️")),
            ForecastDay(day="Sun", dublin=ForecastCity(temp_c=25, emoji="☀️"), cork=ForecastCity(temp_c=14, emoji="🌧️")),
        ],
        last_comparable=LastComparable(
            label="Last comparable weekend",
            date="2025-06-14",
            note="Dublin sold 2,400 BBQ packs · Cork sold 600. Allocation was even — Dublin stocked out by Saturday 3pm.",
        ),
        reallocation=Reallocation(
            from_city="Cork",
            to_city="Dublin",
            units=400,
            departs="Sat 04:00",
            arrives="Sat 09:30",
        ),
        actions=[
            "Reallocate 400 BBQ packs Cork → Dublin (truck Sat 04:00)",
            "Raise Dublin price €12.50 → €13.20 (+5.6%)",
            "Drop Cork price €12.50 → €11.40 (−8.8%) — early-bird clearance",
        ],
        impact=Impact(margin_eur=8200, waste_kg=-180, sell_through_pct=12),
        why=[
            WhyBullet(
                claim="Met Éireann forecasts a 11°C delta between Dublin and Cork on Saturday.",
                source="Met Éireann · 87% confidence",
                evidence=LineEvidence(type="line", label="Forecast confidence over last 5 runs", points=[82, 84, 85, 86, 87]),
            ),
            WhyBullet(
                claim="3 prior BBQ weekends with >10°C Dublin/Cork delta showed ~4× demand skew toward the warmer city.",
                source="Internal sales · 2023–2025",
                evidence=BarEvidence(
                    type="bar",
                    label="Dublin units vs Cork units (3 historical weekends)",
                    bars=[
                        BarEntry(label="2023-07", dublin=2100, cork=580),
                        BarEntry(label="2024-05", dublin=2350, cork=620),
                        BarEntry(label="2025-06", dublin=2400, cork=600),
                    ],
                ),
            ),
            WhyBullet(
                claim="Dublin stocks out Saturday 15:00 at current pace; Cork carries 14 days of cover.",
                source="Inventory snapshot · 06:00 today",
                evidence=StatEvidence(type="stat", label="Days of cover at current sell rate", dublin="1.5", cork="14"),
            ),
        ],
    ),
)
