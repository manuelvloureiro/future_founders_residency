# Joey Demo — Implementation Roadmap

**Goal:** ship a single-page visual demo of "Joey," an agentic retail planning assistant, in ~3 hours. Built by a coding agent from a fully-specified brief.

**Scenario:** A grocery category manager opens Joey on Monday. Joey has detected that next weekend is a barbecue weekend, with diverging weather between Dublin (24°C sunny) and Cork (13°C rainy). Joey recommends reallocating 400 BBQ packs Cork → Dublin and adjusting prices in both cities. The manager can approve, modify, reject, or drill into "show me why" to see the reasoning trace.

---

## Stack (locked — no decisions for the agent)

- Next.js 15 (App Router) + TypeScript
- Tailwind CSS v4
- Framer Motion (animations only)
- **No** chart library — inline SVG bars/lines
- **No** map library — hand-rolled inline SVG of Ireland
- **No** backend, API routes, auth, routing beyond `/`

---

## Phase 0 — Project setup (15 min)

- [ ] `npx create-next-app@latest` with TypeScript + Tailwind + App Router, no src dir, no ESLint prompts
- [ ] `npm i framer-motion`
- [ ] Delete boilerplate from `app/page.tsx` and `app/globals.css` (keep Tailwind directives)
- [ ] Add Inter font via `next/font`
- [ ] Verify `npm run dev` boots clean

**Done when:** blank page renders at `localhost:3000` with Inter loaded.

---

## Phase 1 — Data layer (20 min)

- [ ] Create `data/scenario.ts` with the full mock dataset (see `AGENT_BRIEF.md` for exact contents)
- [ ] Create `data/types.ts` with TypeScript interfaces for Insight, CityState, ForecastDay, WhyBullet, etc.
- [ ] Export a single `scenario` object containing everything the UI needs

**Done when:** `scenario.ts` compiles and exports the full object; no UI consumes it yet.

---

## Phase 2 — Leaf components (60 min)

Build pure prop-driven components, bottom-up. Each is a single file, no internal state unless noted.

- [ ] `components/IrelandMap.tsx` — inline SVG Ireland outline, 2 pinned cities with pulse animation, weather emoji overlay, animated stock-flow arrow Cork→Dublin with "+400 units" label, price chips on each pin showing old → new
- [ ] `components/ForecastStrip.tsx` — Fri/Sat/Sun × Dublin/Cork grid with weather emoji + temp
- [ ] `components/MiniBarChart.tsx` — pure SVG, 5–10 bars, used in why drawer for last-year sales
- [ ] `components/MiniLineChart.tsx` — pure SVG, single polyline, used in why drawer for forecast confidence
- [ ] `components/StatBlock.tsx` — large number + label + delta arrow, for impact metrics

**Done when:** each renders correctly when given props from `scenario.ts`. Not yet wired into the page.

---

## Phase 3 — Column components (40 min)

- [ ] `components/Situation.tsx` — left column: headline temps, sentence summary, embedded `ForecastStrip`, last-comparable-weekend stat line
- [ ] `components/Actions.tsx` — right column: ordered list of recommended actions, 3 `StatBlock`s for impact (margin €, waste kg, sell-through %), 4 buttons (Approve, Modify, Reject, Show me why)

**Done when:** both render standalone with mock props.

---

## Phase 4 — Why drawer (30 min)

- [ ] `components/WhyDrawer.tsx` — slide-up panel via Framer Motion `AnimatePresence`
- [ ] Lists why-bullets from `scenario.ts`, each with a claim + source label
- [ ] Each bullet expands inline to show evidence (number stat, `MiniBarChart`, or `MiniLineChart`)
- [ ] Closes on backdrop click or close button

**Done when:** drawer opens/closes smoothly; each bullet expandable; charts render inside.

---

## Phase 5 — Card composition (20 min)

- [ ] `components/RecommendationCard.tsx` — 3-column layout composing `Situation` + `IrelandMap` + `Actions`
- [ ] Receives selected insight as a prop; renders BBQ scenario fully, others render a "preview unavailable" stub

**Done when:** card renders the full BBQ scenario when given the selected insight.

---

## Phase 6 — Top bar + page wiring (20 min)

- [ ] `components/TopBar.tsx` — greeting + 3 insight pills, selected state styling
- [ ] `app/page.tsx` — manages `selectedInsightId` state, composes `TopBar` + `RecommendationCard` + `WhyDrawer`
- [ ] Pill click swaps selection (BBQ is the only fully populated one)
- [ ] "Show me why" button opens drawer; "Approve" triggers a toast + dims the card

**Done when:** the full demo flow works end-to-end from a fresh page load.

---

## Phase 7 — Polish + verification (45 min)

- [ ] Typography pass: Inter sizing, weights, line-height
- [ ] Color pass: single accent (Joey green `#16a34a`), neutral grays, one warning amber
- [ ] Spacing pass: consistent padding/gap rhythm
- [ ] Animation feel: pulse timing, arrow draw duration, drawer easing
- [ ] Run verification checklist (see `AGENT_BRIEF.md` § Verification)

**Done when:** every checklist item passes.

---

## Out of scope (do not build)

- Backend, API routes, `fetch` calls, environment variables
- Authentication, user accounts, persistence
- Mobile responsiveness (desktop-only is fine for a demo)
- Dark mode, theme switching
- Functional implementations of the heatwave or Six Nations pills
- Real weather API, real LLM calls
- Any route other than `/`
- Tests
- README updates beyond what's already here

---

## Time budget summary

| Phase | Time | Cumulative |
|-------|------|------------|
| 0. Setup | 15 min | 0:15 |
| 1. Data | 20 min | 0:35 |
| 2. Leaf components | 60 min | 1:35 |
| 3. Columns | 40 min | 2:15 |
| 4. Why drawer | 30 min | 2:45 |
| 5. Card | 20 min | 3:05 |
| 6. Top bar + wiring | 20 min | 3:25 |
| 7. Polish | 45 min | 4:10 |

Tight against 3 hours — **cut polish first, then the why-drawer charts (replace with text-only bullets), then the heatwave/Six Nations pills (hide them).** The map and the BBQ recommendation card are non-negotiable.
