# Keith Demo API

FastAPI backend serving the Keith demo scenario data and approval flow.

## Running

```bash
uv run uvicorn main:app --reload
```

CORS is open to `http://localhost:3000`.

## Endpoints

### `GET /health`

Liveness probe.

**Response 200**

```json
{ "status": "ok" }
```

---

### `GET /api/scenario`

Returns the full demo scenario: greeting copy, the list of insight cards, and the BBQ scenario detail (city states, forecast, reallocation plan, projected impact, and "why" evidence bullets).

**Response 200** — `Scenario`

```jsonc
{
  "greeting": "string",
  "subgreeting": "string",
  "monitoring_label": "string",
  "insights": [
    {
      "id": "bbq" | "heatwave" | "sixnations",
      "icon": "string",
      "title": "string",
      "subtitle": "string",
      "selected": true,
      "available": true
    }
  ],
  "bbq": {
    "headline": "string",
    "summary": "string",
    "cities": {
      "dublin": { /* CityState */ },
      "cork":   { /* CityState */ }
    },
    "forecast": [
      {
        "day": "string",
        "dublin": { "temp_c": 0, "emoji": "string" },
        "cork":   { "temp_c": 0, "emoji": "string" }
      }
    ],
    "last_comparable": { "label": "string", "date": "string", "note": "string" },
    "reallocation": {
      "from_city": "string",
      "to_city": "string",
      "units": 0,
      "departs": "string",
      "arrives": "string"
    },
    "actions": ["string"],
    "impact": { "margin_eur": 0, "waste_kg": 0, "sell_through_pct": 0 },
    "why": [
      {
        "claim": "string",
        "source": "string",
        "evidence": { /* line | bar | stat — see below */ }
      }
    ]
  }
}
```

`CityState` fields: `name`, `temp_c`, `condition`, `emoji`, `current_stock_units`, `current_price_eur`, `recommended_price_eur`, `price_delta_pct`, `last_comparable_units`, `pin: { x, y }`.

`why[].evidence` is a discriminated union on `type`:

- `line` — `{ type: "line", label, points: number[] }`
- `bar` — `{ type: "bar",  label, bars: [{ label, dublin, cork }] }`
- `stat` — `{ type: "stat", label, dublin: string, cork: string }`

---

### `POST /api/scenario/approve`

Approves a recommended action for an insight. Currently returns a fixed confirmation message; no state is persisted.

**Request body** — `ApproveRequest`

```json
{ "insight_id": "bbq" }
```

**Response 200** — `ApproveResponse`

```json
{ "message": "Reallocation scheduled · Prices update Wed 00:00" }
```
