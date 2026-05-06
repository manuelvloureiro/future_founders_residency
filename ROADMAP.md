# Joey Demo — Implementation Roadmap

**Tagline:** Agentic Dynamic Pricing for Retailers.

**Goal:** ship a visual demo of "Joey" (the *agent of the retailer*) plus a pitch deck that slices the demo between slides. Python backend serves the data via API; TypeScript frontend renders the UI. Work is split into independent units that multiple agents execute in parallel.

**Scenario:** A grocery category manager opens Joey on Monday. Joey has detected that next weekend is a barbecue weekend, with diverging weather between Dublin (24°C sunny) and Cork (13°C rainy). Joey recommends reallocating 400 BBQ packs Cork → Dublin and adjusting prices in both cities. The manager can approve, modify, reject, or drill into "show me why" to see the reasoning trace.

**Pitch context:** the demo is sliced **between slides** during the pitch — short live moments that prove each claim, not one big reveal. Pitch arc: problem → background → why now → solution (demo slice) → how it works (demo slice) → business model → market → team → vision → ask. See `PITCH.md` for the full storyboard.

---

## How agents coordinate

Each work unit below has a **slug** (e.g. `backend-setup`). Agents claim and execute work using git worktrees:

### Claiming work
1. Agent lists existing worktrees: `git worktree list`
2. Agent scans the slugs in this roadmap and picks the first unclaimed unit whose **dependencies are met** (all listed deps have been merged to `main`).
3. Agent creates a worktree and branch for that slug:
   ```
   git worktree add ../joey-<slug> -b work/<slug>
   ```
   If the worktree or branch already exists, another agent claimed it — skip to the next available unit.

### Executing work
4. Agent works entirely inside its worktree (`../joey-<slug>/`).
5. Agent commits with a message that references the work unit:
   ```
   [<slug>] <description of what was done>
   ```
   This makes conflict resolution unambiguous — anyone reading the log knows which roadmap unit produced each commit.

### Merging back
6. From the main repo, agent merges the branch:
   ```
   git checkout main
   git merge work/<slug> --no-ff -m "Merge work/<slug>: <unit title>"
   ```
7. If there are merge conflicts, the agent resolves them by understanding which work unit each conflicting chunk belongs to (identifiable from the `[<slug>]` commit messages). The current unit's intent takes priority for files it owns; shared files (e.g. `page.tsx`, `types.ts`) require understanding both units' intent and preserving both contributions.
8. After a successful merge, agent cleans up:
   ```
   git worktree remove ../joey-<slug>
   git branch -d work/<slug>
   ```

### Rules
- An agent must **never** work directly on `main`. All work happens on `work/<slug>` branches.
- An agent must **check dependencies are merged** before starting. If deps aren't ready, pick a different unit or wait.
- If two agents need to modify the same file, the later merger resolves conflicts. Commit messages with `[<slug>]` prefixes make this tractable.
- The `[integration]` and `[polish]` units are special — they touch many files and should run alone after their deps are all merged.

---

## Stack (locked — no decisions for the agent)

### Backend (`backend/`)
- Python 3.11+
- FastAPI + Uvicorn
- Pydantic models for all data types
- **No** database, **no** ORM, **no** auth
- Serves mock data from an in-memory module

### Frontend (`frontend/`)
- Next.js 15 (App Router) + TypeScript
- Tailwind CSS v4
- Framer Motion (animations only)
- **No** chart library — inline SVG bars/lines
- **No** map library — hand-rolled inline SVG of Ireland
- Fetches all data from the Python backend API

---

## Wave 1 — Foundation (parallel, no dependencies)

These units have zero cross-dependencies and can all run simultaneously.

### `backend-setup` — Backend setup + data layer
**Slug:** `backend-setup`
**Deps:** none
**Files:** `backend/main.py`, `backend/models.py`, `backend/data.py`, `backend/requirements.txt`

- [ ] Create `backend/` directory structure
- [ ] Set up Python venv, install `fastapi`, `uvicorn`, `pydantic`
- [ ] Add `requirements.txt`
- [ ] Create `models.py` with all Pydantic models (see `AGENT_BRIEF.md`)
- [ ] Create `data.py` with the full mock dataset (see `AGENT_BRIEF.md`)
- [ ] Create `main.py` with FastAPI app, CORS middleware (allow `localhost:3000`), endpoints:
  - `GET /health` → `{"status": "ok"}`
  - `GET /api/scenario` → full scenario object
  - `POST /api/scenario/approve` → confirmation message
- [ ] Verify `uvicorn main:app --reload` boots clean on port 8000

**Done when:** all three endpoints return correct responses.

---

### `frontend-setup` — Frontend setup + types + API helpers
**Slug:** `frontend-setup`
**Deps:** none
**Files:** `frontend/lib/types.ts`, `frontend/lib/api.ts`, `frontend/app/globals.css`, `frontend/app/layout.tsx`

- [ ] Install `framer-motion` if not already installed
- [ ] Delete boilerplate from `app/page.tsx` and `app/globals.css` (keep Tailwind directives)
- [ ] Add Inter font via `next/font` in `layout.tsx`
- [ ] Create `lib/types.ts` with TypeScript interfaces matching backend Pydantic models
- [ ] Create `lib/api.ts` with typed fetch helpers (`fetchScenario`, `approveInsight`)
- [ ] Verify `npm run dev` boots clean

**Done when:** blank page renders at `localhost:3000` with Inter loaded; types compile cleanly.

---

### `leaf-ireland-map` — IrelandMap component
**Slug:** `leaf-ireland-map`
**Deps:** none
**Files:** `frontend/components/IrelandMap.tsx`

- [ ] Inline SVG Ireland outline, viewBox `"0 0 500 600"`
- [ ] 2 pinned cities with pulse animation (Framer Motion)
- [ ] Weather emoji overlay near each pin
- [ ] Price chips on each pin showing old → new price
- [ ] Animated stock-flow arrow Cork→Dublin with "+400 units" label
- [ ] Arrow draws over 1.5s on mount

**Done when:** component renders correctly when given props matching `BbqScenario` shape. Import types locally or inline — don't depend on `lib/types.ts` existing yet.

---

### `leaf-forecast-strip` — ForecastStrip component
**Slug:** `leaf-forecast-strip`
**Deps:** none
**Files:** `frontend/components/ForecastStrip.tsx`

- [ ] Props: `forecast: ForecastDay[]`
- [ ] Grid: 3 columns (Fri/Sat/Sun) × 2 rows (Dublin/Cork)
- [ ] Each cell shows emoji + temperature
- [ ] Day labels above, city labels on left

**Done when:** component renders correctly with mock forecast data.

---

### `leaf-charts` — MiniBarChart + MiniLineChart components
**Slug:** `leaf-charts`
**Deps:** none
**Files:** `frontend/components/MiniBarChart.tsx`, `frontend/components/MiniLineChart.tsx`

- [ ] `MiniBarChart.tsx` — inline SVG ~280×120px, grouped bars (Dublin green, Cork amber)
- [ ] `MiniLineChart.tsx` — inline SVG ~280×80px, single polyline in Joey green with circle markers

**Done when:** both render correctly with mock data.

---

### `leaf-stat-block` — StatBlock component
**Slug:** `leaf-stat-block`
**Deps:** none
**Files:** `frontend/components/StatBlock.tsx`

- [ ] Props: `value: string`, `label: string`, `delta?: 'up' | 'down' | 'neutral'`
- [ ] Large number + label + optional delta arrow

**Done when:** component renders correctly with mock props.

---

### `pitch-deck` — Pitch storyboard slides
**Slug:** `pitch-deck`
**Deps:** none
**Files:** `pitch/` (new directory) — one slide per markdown file or a single `slides.md`; presentation tool TBD (Keynote / Pitch / Tome / plain HTML — agent picks lightest viable)

- [ ] Read `PITCH.md` end-to-end before building anything — that's the canonical content
- [ ] One slide per section: Problem, Insight, Why now, Solution (demo slot), How it works (demo slot), Business model, Market, Team, Vision, Ask
- [ ] Picture-led, story-style — minimise bullet text on slides; speaker notes carry the talking points from `PITCH.md`
- [ ] Mark the two demo-slot slides clearly so the presenter knows to switch to the live Joey demo
- [ ] Lock the tagline **"Agentic Dynamic Pricing for Retailers"** on the title slide and footer
- [ ] Flag any unresolved items from `PITCH.md` § "Open questions" inline as TODO speaker notes (don't fabricate the Ocado £105M number — leave it as TODO until verified)

**Done when:** deck is rehearsable end-to-end; demo slots are explicit; speaker notes mirror `PITCH.md`.

---

## Wave 2 — Composite components (parallel, after Wave 1 deps merge)

These units compose Wave 1 leaf components. Each depends on specific Wave 1 units.

### `column-situation` — Situation column component
**Slug:** `column-situation`
**Deps:** `frontend-setup`, `leaf-forecast-strip`
**Files:** `frontend/components/Situation.tsx`

- [ ] Headline: "Dublin {tempC}°C {emoji} · Cork {tempC}°C {emoji}"
- [ ] Summary paragraph
- [ ] Embedded `<ForecastStrip>`
- [ ] Last-comparable note as a callout box

**Done when:** renders standalone with typed props from `lib/types.ts`.

---

### `column-actions` — Actions column component
**Slug:** `column-actions`
**Deps:** `frontend-setup`, `leaf-stat-block`
**Files:** `frontend/components/Actions.tsx`

- [ ] "Recommended actions" header + numbered list
- [ ] Three `<StatBlock>` in a row (margin, waste, sell-through)
- [ ] Four buttons: Approve (primary green), Modify (outline), Reject (outline), Show me why (link-style)
- [ ] Approve click triggers parent callback

**Done when:** renders standalone with typed props.

---

### `drawer-why` — WhyDrawer component
**Slug:** `drawer-why`
**Deps:** `frontend-setup`, `leaf-charts`
**Files:** `frontend/components/WhyDrawer.tsx`

- [ ] Slide-up panel via Framer Motion `AnimatePresence`, 70vh height
- [ ] Lists why-bullets with claim + source label
- [ ] Each bullet expandable to show evidence (`MiniBarChart`, `MiniLineChart`, or stat row)
- [ ] Closes on backdrop click or close button

**Done when:** drawer opens/closes smoothly; bullets expand with charts.

---

## Wave 3 — Composition (parallel, after Wave 2 deps merge)

### `card-recommendation` — RecommendationCard component
**Slug:** `card-recommendation`
**Deps:** `column-situation`, `column-actions`, `leaf-ireland-map`
**Files:** `frontend/components/RecommendationCard.tsx`

- [ ] 3-column layout: `Situation` | `IrelandMap` | `Actions`
- [ ] BBQ insight renders full card; others render "Preview unavailable" stub
- [ ] `opacity-60 pointer-events-none` when approved

**Done when:** card renders the full BBQ scenario.

---

### `topbar` — TopBar component
**Slug:** `topbar`
**Deps:** `frontend-setup`
**Files:** `frontend/components/TopBar.tsx`

- [ ] Greeting + subgreeting on left, monitoring label with pulsing dot on right
- [ ] Row of 3 insight pills with selected state styling
- [ ] Pill click calls `onSelect`

**Done when:** renders standalone with typed props.

---

## Wave 4 — Integration (sequential, after all above merge)

### `integration` — Page wiring
**Slug:** `integration`
**Deps:** `backend-setup`, `card-recommendation`, `topbar`, `drawer-why`
**Files:** `frontend/app/page.tsx`

- [ ] Client component fetches scenario from backend on mount
- [ ] Manages state: `selectedId`, `whyOpen`, `approved`, `toast`, `scenario`
- [ ] Composes `TopBar` → `RecommendationCard` → `WhyDrawer`
- [ ] Pill click swaps selection
- [ ] "Show me why" opens drawer; "Approve" calls backend, dims card, shows toast

**Done when:** full demo flow works end-to-end with data from the Python backend.

---

## Wave 5 — Polish (sequential, after integration merges)

### `polish` — Visual polish + verification
**Slug:** `polish`
**Deps:** `integration`
**Files:** any — cross-cutting

- [ ] Typography pass: Inter sizing, weights, line-height
- [ ] Color pass: Joey green `#16a34a`, neutral grays, warning amber
- [ ] Spacing pass: consistent padding/gap rhythm
- [ ] Animation feel: pulse timing, arrow draw duration, drawer easing
- [ ] Run full verification checklist (see `AGENT_BRIEF.md` § Verification)

**Done when:** every checklist item passes.

---

## Out of scope (do not build)

- Database, ORM, or persistent storage
- Authentication, user accounts
- Mobile responsiveness (desktop-only is fine for a demo)
- Dark mode, theme switching
- Functional implementations of the heatwave or Six Nations pills
- Real weather API, real LLM calls
- Any frontend route other than `/`
- Tests
- README updates beyond what's already here

---

## Parallelism map

```
Wave 1 (all parallel, no deps):
  backend-setup ─────────────────┐
  frontend-setup ────────────────┤
  leaf-ireland-map ──────────────┤
  leaf-forecast-strip ───────────┤
  leaf-charts ───────────────────┤
  leaf-stat-block ───────────────┤
  pitch-deck ────────────────────┘  (independent — pitch storyboard, no code deps)
                                 │
Wave 2 (parallel, partial deps): │
  column-situation ──────(needs frontend-setup + leaf-forecast-strip)
  column-actions ────────(needs frontend-setup + leaf-stat-block)
  drawer-why ────────────(needs frontend-setup + leaf-charts)
  topbar ────────────────(needs frontend-setup)
                                 │
Wave 3 (parallel, partial deps): │
  card-recommendation ───(needs column-situation + column-actions + leaf-ireland-map)
                                 │
Wave 4 (sequential):             │
  integration ───────────(needs backend-setup + card-recommendation + topbar + drawer-why)
                                 │
Wave 5 (sequential):             │
  polish ────────────────(needs integration)
```

**Critical path:** `frontend-setup` → `column-situation` → `card-recommendation` → `integration` → `polish`

**Max parallelism:** 7 agents in Wave 1 (6 code + 1 pitch deck), 4 in Wave 2, then sequential convergence.
