# Joey Demo — Agent Build Brief

You are building a visual demo with a Python backend and TypeScript frontend. Follow this brief exactly. Do not invent features, data, or copy beyond what's specified here.

## What you're building

**Tagline:** Agentic Dynamic Pricing for Retailers. Joey is the *agent of the retailer* — it controls the **now**: pricing, allocation, and promotions reacting per-store, per-hour, against weather, sales velocity, inventory, and social signal.

**Pitch role:** the demo is sliced **between slides** during the pitch (see `PITCH.md`). It needs to read instantly and dramatise the core claim: a category manager opens Joey and finds a *decision already drafted*, not a dashboard to interpret.

A **Python (FastAPI) backend** that serves mock scenario data via REST API, and a **Next.js TypeScript frontend** at `/` that demonstrates Joey. One screen, three zones:

1. **Top bar** — greeting + 3 insight pills (one selected) + tagline strip
2. **Recommendation card** — 3-column layout: situation (left), Ireland map (center), actions (right)
3. **Why drawer** — slides up from the bottom when "Show me why" is clicked

The user is a grocery category manager. Joey has detected a barbecue weekend with diverging weather between Dublin and Cork. The *failure mode without Joey* is concrete and must come through in the copy: Dublin stocks out Saturday afternoon, Cork bins ~180 kg of meat. The manager could not have caught both in time manually.

---

## Stack (do not deviate)

### Backend (`backend/`)
- Python 3.11+, FastAPI, Uvicorn
- Pydantic models for request/response schemas
- CORS middleware allowing `http://localhost:3000`
- **No** database, **no** ORM, **no** auth, **no** external APIs

### Frontend (`frontend/`)
- Next.js 15 App Router, TypeScript, Tailwind v4
- Framer Motion for animations
- **No** chart library, **no** map library, **no** routing beyond `/`
- All data fetched from the Python backend at `http://localhost:8000`

---

## File layout

### Backend
```
backend/
  main.py            # FastAPI app, CORS, route definitions
  models.py          # Pydantic models (Insight, CityState, etc.)
  data.py            # Mock scenario data
  requirements.txt   # fastapi, uvicorn, pydantic
```

### Frontend
```
frontend/
  app/
    page.tsx
    layout.tsx
    globals.css
  components/
    TopBar.tsx
    RecommendationCard.tsx
    Situation.tsx
    IrelandMap.tsx
    Actions.tsx
    WhyDrawer.tsx
    ForecastStrip.tsx
    MiniBarChart.tsx
    MiniLineChart.tsx
    StatBlock.tsx
  lib/
    api.ts             # Typed fetch helpers for backend endpoints
    types.ts           # TypeScript interfaces matching Pydantic models
```

---

## Backend API endpoints

### `GET /api/scenario`
Returns the full scenario object (see data below). Response schema matches the `Scenario` Pydantic model.

### `POST /api/scenario/approve`
Request body: `{ "insight_id": "bbq" }`
Response: `{ "message": "Reallocation scheduled · Prices update Wed 00:00" }`

### `GET /health`
Returns: `{ "status": "ok" }`

---

## `backend/data.py` — full content

This is the **single source of truth** for all data, copy, and numbers. Use these values exactly. Do not change a number, label, or string.

```python
from models import (
    Scenario, Insight, BbqScenario, CityState, Pin,
    ForecastDay, CityForecast, LastComparable, Reallocation,
    Impact, WhyBullet, LineEvidence, BarEvidence, StatEvidence, BarItem,
)

scenario = Scenario(
    greeting="Good morning, Aoife.",
    subgreeting="3 decisions drafted overnight. 1 needs you now.",
    monitoring_label="Joey · agentic dynamic pricing · live · updated 2 min ago",

    insights=[
        Insight(id="bbq", icon="🔥", title="Barbecue weekend", subtitle="Dublin / Cork divergence", selected=True, available=True),
        Insight(id="heatwave", icon="☀️", title="Heatwave forecast", subtitle="Ice cream category", selected=False, available=False),
        Insight(id="sixnations", icon="🏉", title="Six Nations Saturday", subtitle="Snacks / beer uplift", selected=False, available=False),
    ],

    bbq=BbqScenario(
        headline="Barbecue weekend Sat–Sun",
        summary="Dublin will be hot and dry while Cork sees rain. Without action: Dublin stocks out Saturday afternoon, Cork bins ~180 kg of meat. Joey has drafted the reallocation and price changes — approve to commit.",

        cities={
            "dublin": CityState(
                name="Dublin", temp_c=24, condition="sunny", emoji="☀️",
                current_stock_units=1800, current_price_eur=12.5,
                recommended_price_eur=13.2, price_delta_pct=5.6,
                last_comparable_units=2400, pin=Pin(x=295, y=215),
            ),
            "cork": CityState(
                name="Cork", temp_c=13, condition="rain", emoji="🌧️",
                current_stock_units=1800, current_price_eur=12.5,
                recommended_price_eur=11.4, price_delta_pct=-8.8,
                last_comparable_units=600, pin=Pin(x=215, y=395),
            ),
        },

        forecast=[
            ForecastDay(day="Fri", dublin=CityForecast(temp_c=21, emoji="⛅"), cork=CityForecast(temp_c=15, emoji="🌦️")),
            ForecastDay(day="Sat", dublin=CityForecast(temp_c=24, emoji="☀️"), cork=CityForecast(temp_c=13, emoji="🌧️")),
            ForecastDay(day="Sun", dublin=CityForecast(temp_c=25, emoji="☀️"), cork=CityForecast(temp_c=14, emoji="🌧️")),
        ],

        last_comparable=LastComparable(
            label="Last comparable weekend",
            date="2025-06-14",
            note="Dublin sold 2,400 BBQ packs · Cork sold 600. Allocation was even — Dublin stocked out by Saturday 3pm.",
        ),

        reallocation=Reallocation(from_city="Cork", to_city="Dublin", units=400, departs="Thu 06:00", arrives="Thu 11:30"),

        actions=[
            "Reallocate 400 BBQ packs Cork → Dublin (truck Thu 06:00)",
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
                        BarItem(label="2023-07", dublin=2100, cork=580),
                        BarItem(label="2024-05", dublin=2350, cork=620),
                        BarItem(label="2025-06", dublin=2400, cork=600),
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
```

---

## `backend/models.py` — Pydantic models

```python
from __future__ import annotations
from typing import Literal, Union
from pydantic import BaseModel, Field


class Pin(BaseModel):
    x: int
    y: int


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


class CityForecast(BaseModel):
    temp_c: int
    emoji: str


class ForecastDay(BaseModel):
    day: str
    dublin: CityForecast
    cork: CityForecast


class Reallocation(BaseModel):
    from_city: str = Field(serialization_alias="from")
    to_city: str = Field(serialization_alias="to")
    units: int
    departs: str
    arrives: str


class LastComparable(BaseModel):
    label: str
    date: str
    note: str


class Impact(BaseModel):
    margin_eur: int
    waste_kg: int
    sell_through_pct: int


class LineEvidence(BaseModel):
    type: Literal["line"]
    label: str
    points: list[int]


class BarItem(BaseModel):
    label: str
    dublin: int
    cork: int


class BarEvidence(BaseModel):
    type: Literal["bar"]
    label: str
    bars: list[BarItem]


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


class Insight(BaseModel):
    id: Literal["bbq", "heatwave", "sixnations"]
    icon: str
    title: str
    subtitle: str
    selected: bool
    available: bool


class BbqScenario(BaseModel):
    headline: str
    summary: str
    cities: dict[str, CityState]
    forecast: list[ForecastDay]
    last_comparable: LastComparable
    reallocation: Reallocation
    actions: list[str]
    impact: Impact
    why: list[WhyBullet]


class Scenario(BaseModel):
    greeting: str
    subgreeting: str
    monitoring_label: str
    insights: list[Insight]
    bbq: BbqScenario


class ApproveRequest(BaseModel):
    insight_id: str
```

---

## `frontend/lib/types.ts` — TypeScript interfaces

These must match the JSON shape returned by the backend (camelCase via Pydantic aliasing or snake_case — pick one and be consistent).

```ts
export type City = 'dublin' | 'cork';

export interface Insight {
  id: 'bbq' | 'heatwave' | 'sixnations';
  icon: string;
  title: string;
  subtitle: string;
  selected: boolean;
  available: boolean;
}

export interface CityState {
  name: string;
  temp_c: number;
  condition: string;
  emoji: string;
  current_stock_units: number;
  current_price_eur: number;
  recommended_price_eur: number;
  price_delta_pct: number;
  last_comparable_units: number;
  pin: { x: number; y: number };
}

export interface CityForecast {
  temp_c: number;
  emoji: string;
}

export interface ForecastDay {
  day: string;
  dublin: CityForecast;
  cork: CityForecast;
}

export interface Reallocation {
  from: string;
  to: string;
  units: number;
  departs: string;
  arrives: string;
}

export interface Impact {
  margin_eur: number;
  waste_kg: number;
  sell_through_pct: number;
}

export type WhyEvidence =
  | { type: 'line'; label: string; points: number[] }
  | { type: 'bar'; label: string; bars: { label: string; dublin: number; cork: number }[] }
  | { type: 'stat'; label: string; dublin: string; cork: string };

export interface WhyBullet {
  claim: string;
  source: string;
  evidence: WhyEvidence;
}

export interface BbqScenario {
  headline: string;
  summary: string;
  cities: { dublin: CityState; cork: CityState };
  forecast: ForecastDay[];
  last_comparable: { label: string; date: string; note: string };
  reallocation: Reallocation;
  actions: string[];
  impact: Impact;
  why: WhyBullet[];
}

export interface Scenario {
  greeting: string;
  subgreeting: string;
  monitoring_label: string;
  insights: Insight[];
  bbq: BbqScenario;
}
```

---

## Component contracts

### `IrelandMap.tsx`
- Inline SVG, viewBox `"0 0 500 600"`, width 100%, max-width 400px
- Render a simplified Ireland outline as a single `<path>`. If you cannot produce a recognizable outline, fall back to a soft-rounded rectangle with the label "Ireland" — readability beats accuracy
- Two pins at the coordinates from `scenario.bbq.cities.<city>.pin`
- Each pin: filled circle with continuous pulse animation (`scale: [1, 1.25, 1]`, 2s loop) using Framer Motion
- Dublin pin color `#16a34a` (Joey green), Cork pin color `#f59e0b` (amber)
- Weather emoji rendered as `<text>` near each pin
- City name label below each pin
- Price chip near each pin showing `€12.50 → €13.20` (Dublin) and `€12.50 → €11.40` (Cork)
- Animated arrow from Cork pin to Dublin pin: SVG path with `stroke-dasharray` animation, arrowhead marker, label "+400 units" at midpoint
- Arrow draws over 1.5s on mount, then stays visible

### `ForecastStrip.tsx`
- Props: `forecast: ForecastDay[]`
- Grid: 3 columns (one per day) × 2 rows (Dublin top, Cork bottom)
- Each cell shows emoji + temperature
- Day labels (Fri/Sat/Sun) above the grid
- City labels (DUB/COR) on the left

### `MiniBarChart.tsx`
- Props: `bars: { label: string; dublin: number; cork: number }[]`
- Inline SVG, ~280×120px
- Grouped bars: Dublin (green) and Cork (amber) per label
- Y-axis implicit (max bar = 90% height)
- Labels under each group

### `MiniLineChart.tsx`
- Props: `points: number[]`
- Inline SVG, ~280×80px
- Single polyline in Joey green, with circle markers at each point
- Y-axis range: min(points) − 5 to max(points) + 5

### `StatBlock.tsx`
- Props: `value: string`, `label: string`, `delta?: 'up' | 'down' | 'neutral'`
- Large number (text-3xl, font-semibold), small label below
- Optional small arrow indicator in green (up) / red (down)

### `Situation.tsx` (left column)
- Headline: "Dublin {tempC}°C {emoji} · Cork {tempC}°C {emoji}" in large semibold text
- Summary paragraph (`scenario.bbq.summary`)
- `<ForecastStrip>` embedded
- Last-comparable note rendered as a callout box

### `Actions.tsx` (right column)
- "Recommended actions" header
- Numbered list of `scenario.bbq.actions`
- Three `<StatBlock>` in a row: margin (`+€8,200`, up), waste (`−180 kg`, down=good=green), sell-through (`+12%`, up)
- Four buttons: **Approve** (primary green), **Modify** (outline), **Reject** (outline), **Show me why** (link-style)
- Approve click: parent receives callback, dims card via opacity-60, shows toast "Reallocation scheduled · Prices update Wed 00:00"

### `WhyDrawer.tsx`
- Props: `open: boolean`, `onClose: () => void`, `bullets: WhyBullet[]`
- Slides up from bottom using Framer Motion `AnimatePresence`, height 70vh, max-width 1100px, centered, with backdrop
- Each bullet: claim text, source label, expandable to show evidence (`MiniBarChart`, `MiniLineChart`, or stat row)
- Close button top-right; backdrop click also closes

### `RecommendationCard.tsx`
- Props: `insight: Insight`, `bbq: BbqScenario`, `onShowWhy: () => void`, `onApprove: () => void`, `approved: boolean`
- If `insight.id === 'bbq'`: render 3-column grid (`Situation` | `IrelandMap` | `Actions`)
- Else: render a centered "Preview unavailable in this demo" stub
- Apply `opacity-60 pointer-events-none` when `approved`

### `TopBar.tsx`
- Props: `insights: Insight[]`, `selectedId: string`, `onSelect: (id: string) => void`, `greeting: string`, `subgreeting: string`, `monitoringLabel: string`
- Greeting (large) + subgreeting (medium) on the left
- Monitoring label (small, with a tiny green pulsing dot) on the right
- Below greeting/right-rail row: a thin tagline strip rendering the literal text **"Agentic Dynamic Pricing for Retailers"** (uppercase, tracked, `text-xs text-neutral-500`). This anchors the demo for viewers walking into the screen mid-pitch.
- Row of 3 pills below the tagline strip; selected pill has filled green background, others have white background with border
- Clicking a pill calls `onSelect`

### `frontend/lib/api.ts`
- `fetchScenario(): Promise<Scenario>` — `GET http://localhost:8000/api/scenario`
- `approveInsight(insightId: string): Promise<{ message: string }>` — `POST http://localhost:8000/api/scenario/approve`
- Both use typed return values from `lib/types.ts`

### `app/page.tsx`
- Client component (`'use client'`)
- On mount: fetch scenario from backend via `fetchScenario()`; show loading state until resolved
- State: `selectedId` (default `'bbq'`), `whyOpen` (default false), `approved` (default false), `toast` (default null), `scenario` (from API)
- Composes `TopBar` → `RecommendationCard` → `WhyDrawer`
- Renders toast as a fixed bottom-right element when set; auto-dismisses after 3s
- Approve handler: call `approveInsight(selectedId)`, set `approved=true`, set toast text from response, fire setTimeout to clear toast

### `app/layout.tsx`
- Inter font via `next/font/google`
- Body classes: `bg-neutral-50 text-neutral-900 antialiased`

---

## Visual system

- Accent: `#16a34a` (Joey green)
- Warning/secondary: `#f59e0b` (amber)
- Neutrals: Tailwind `neutral-50` (bg), `neutral-200` (borders), `neutral-600` (subtle text), `neutral-900` (primary text)
- Card: `bg-white rounded-2xl border border-neutral-200 shadow-sm p-8`
- Page max-width: `max-w-7xl mx-auto px-8 py-10`
- Font sizes: greeting `text-3xl`, subgreeting `text-lg`, headline `text-2xl`, body `text-sm`/`text-base`

---

## Do NOT

- Do not add a database, ORM, or persistent storage
- Do not add authentication or user accounts
- Do not add frontend routing beyond `/`
- Do not make heatwave or Six Nations pills functional
- Do not add code comments explaining what code does
- Do not invent data or copy not present in `backend/data.py`
- Do not add tests
- Do not add a README beyond what already exists in the repo
- Do not install chart or map libraries
- Do not call any external APIs (weather, LLM, etc.)

---

## Verification checklist (run before declaring done)

### Backend
1. `pip install -r requirements.txt` succeeds
2. `uvicorn main:app --reload` starts with no errors on port 8000
3. `GET /health` returns `{"status": "ok"}`
4. `GET /api/scenario` returns the full scenario JSON with correct data
5. `POST /api/scenario/approve` with `{"insight_id": "bbq"}` returns the confirmation message

### Frontend
6. `npm run dev` starts with no errors on port 3000
7. `npx tsc --noEmit` passes with no errors
8. Page at `/` loads data from the backend and shows: greeting, "Agentic Dynamic Pricing for Retailers" tagline strip, 3 pills (BBQ selected), recommendation card with 3 columns, no console errors
9. Map renders Ireland-ish outline with 2 pulsing pins (Dublin green, Cork amber), weather emojis, price chips, animated arrow Cork→Dublin with "+400 units" label
10. Forecast strip shows Fri/Sat/Sun for both cities
11. Clicking heatwave or Six Nations pill swaps the card to "Preview unavailable"
12. Clicking the BBQ pill restores the full card
13. "Show me why" opens the drawer; backdrop click closes it
14. Drawer bullets are expandable, charts render inline
15. "Approve" calls the backend, dims the card, and shows a toast that auto-dismisses
16. No TypeScript errors, no console errors, no unused imports

If any item fails, fix it before reporting done.
