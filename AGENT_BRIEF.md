# Joey Demo — Agent Build Brief

You are building a single-page visual demo. Follow this brief exactly. Do not invent features, data, or copy beyond what's specified here.

## What you're building

A Next.js page at `/` that demonstrates "Joey," an agentic retail planning assistant. One screen, three zones:

1. **Top bar** — greeting + 3 insight pills (one selected)
2. **Recommendation card** — 3-column layout: situation (left), Ireland map (center), actions (right)
3. **Why drawer** — slides up from the bottom when "Show me why" is clicked

The user is a grocery category manager. Joey has detected a barbecue weekend with diverging weather between Dublin and Cork.

---

## Stack (do not deviate)

- Next.js 15 App Router, TypeScript, Tailwind v4
- Framer Motion for animations
- **No** chart library, **no** map library, **no** backend, **no** API routes, **no** auth, **no** routing beyond `/`

---

## File layout

```
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
data/
  scenario.ts
  types.ts
```

---

## `data/scenario.ts` — full content

This is the **single source of truth** for all data, copy, and numbers. Use these values exactly. Do not change a number, label, or string.

```ts
import type { Scenario } from './types';

export const scenario: Scenario = {
  greeting: 'Good morning, Aoife.',
  subgreeting: '3 strategic insights this week.',
  monitoringLabel: 'Joey · monitoring · updated 2 min ago',

  insights: [
    {
      id: 'bbq',
      icon: '🔥',
      title: 'Barbecue weekend',
      subtitle: 'Dublin / Cork divergence',
      selected: true,
      available: true,
    },
    {
      id: 'heatwave',
      icon: '☀️',
      title: 'Heatwave forecast',
      subtitle: 'Ice cream category',
      selected: false,
      available: false,
    },
    {
      id: 'sixnations',
      icon: '🏉',
      title: 'Six Nations Saturday',
      subtitle: 'Snacks / beer uplift',
      selected: false,
      available: false,
    },
  ],

  bbq: {
    headline: 'Barbecue weekend Sat–Sun',
    summary:
      'Dublin will be hot and dry while Cork sees rain. Without action, Dublin stocks out Saturday afternoon and Cork throws away ~180 kg of meat.',

    cities: {
      dublin: {
        name: 'Dublin',
        tempC: 24,
        condition: 'sunny',
        emoji: '☀️',
        currentStockUnits: 1800,
        currentPriceEur: 12.5,
        recommendedPriceEur: 13.2,
        priceDeltaPct: 5.6,
        lastComparableUnits: 2400,
        pin: { x: 295, y: 215 },
      },
      cork: {
        name: 'Cork',
        tempC: 13,
        condition: 'rain',
        emoji: '🌧️',
        currentStockUnits: 1800,
        currentPriceEur: 12.5,
        recommendedPriceEur: 11.4,
        priceDeltaPct: -8.8,
        lastComparableUnits: 600,
        pin: { x: 215, y: 395 },
      },
    },

    forecast: [
      { day: 'Fri', dublin: { tempC: 21, emoji: '⛅' }, cork: { tempC: 15, emoji: '🌦️' } },
      { day: 'Sat', dublin: { tempC: 24, emoji: '☀️' }, cork: { tempC: 13, emoji: '🌧️' } },
      { day: 'Sun', dublin: { tempC: 25, emoji: '☀️' }, cork: { tempC: 14, emoji: '🌧️' } },
    ],

    lastComparable: {
      label: 'Last comparable weekend',
      date: '2025-06-14',
      note: 'Dublin sold 2,400 BBQ packs · Cork sold 600. Allocation was even — Dublin stocked out by Saturday 3pm.',
    },

    reallocation: {
      from: 'Cork',
      to: 'Dublin',
      units: 400,
      departs: 'Thu 06:00',
      arrives: 'Thu 11:30',
    },

    actions: [
      'Reallocate 400 BBQ packs Cork → Dublin (truck Thu 06:00)',
      'Raise Dublin price €12.50 → €13.20 (+5.6%)',
      'Drop Cork price €12.50 → €11.40 (−8.8%) — early-bird clearance',
    ],

    impact: {
      marginEur: 8200,
      wasteKg: -180,
      sellThroughPct: 12,
    },

    why: [
      {
        claim: 'Met Éireann forecasts a 11°C delta between Dublin and Cork on Saturday.',
        source: 'Met Éireann · 87% confidence',
        evidence: {
          type: 'line',
          label: 'Forecast confidence over last 5 runs',
          points: [82, 84, 85, 86, 87],
        },
      },
      {
        claim: '3 prior BBQ weekends with >10°C Dublin/Cork delta showed ~4× demand skew toward the warmer city.',
        source: 'Internal sales · 2023–2025',
        evidence: {
          type: 'bar',
          label: 'Dublin units vs Cork units (3 historical weekends)',
          bars: [
            { label: '2023-07', dublin: 2100, cork: 580 },
            { label: '2024-05', dublin: 2350, cork: 620 },
            { label: '2025-06', dublin: 2400, cork: 600 },
          ],
        },
      },
      {
        claim: 'Dublin stocks out Saturday 15:00 at current pace; Cork carries 14 days of cover.',
        source: 'Inventory snapshot · 06:00 today',
        evidence: {
          type: 'stat',
          label: 'Days of cover at current sell rate',
          dublin: '1.5',
          cork: '14',
        },
      },
    ],
  },
};
```

---

## `data/types.ts` — exact interfaces

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
  tempC: number;
  condition: string;
  emoji: string;
  currentStockUnits: number;
  currentPriceEur: number;
  recommendedPriceEur: number;
  priceDeltaPct: number;
  lastComparableUnits: number;
  pin: { x: number; y: number };
}

export interface ForecastDay {
  day: string;
  dublin: { tempC: number; emoji: string };
  cork: { tempC: number; emoji: string };
}

export interface Reallocation {
  from: string;
  to: string;
  units: number;
  departs: string;
  arrives: string;
}

export interface Impact {
  marginEur: number;
  wasteKg: number;
  sellThroughPct: number;
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
  lastComparable: { label: string; date: string; note: string };
  reallocation: Reallocation;
  actions: string[];
  impact: Impact;
  why: WhyBullet[];
}

export interface Scenario {
  greeting: string;
  subgreeting: string;
  monitoringLabel: string;
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
- Row of 3 pills below; selected pill has filled green background, others have white background with border
- Clicking a pill calls `onSelect`

### `app/page.tsx`
- Client component (`'use client'`)
- State: `selectedId` (default `'bbq'`), `whyOpen` (default false), `approved` (default false), `toast` (default null)
- Composes `TopBar` → `RecommendationCard` → `WhyDrawer`
- Renders toast as a fixed bottom-right element when set; auto-dismisses after 3s
- Approve handler: set `approved=true`, set toast text, fire setTimeout to clear toast

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

- Do not add a backend, API routes, `fetch`, or environment variables
- Do not add authentication or user accounts
- Do not add routing beyond `/`
- Do not make heatwave or Six Nations pills functional
- Do not add code comments explaining what code does
- Do not invent data or copy not present in `scenario.ts`
- Do not add tests
- Do not add a README beyond what already exists in the repo
- Do not install chart or map libraries

---

## Verification checklist (run before declaring done)

1. `npm run dev` starts with no errors
2. `npx tsc --noEmit` passes with no errors
3. Page at `/` shows: greeting, 3 pills (BBQ selected), recommendation card with 3 columns, no console errors
4. Map renders Ireland-ish outline with 2 pulsing pins (Dublin green, Cork amber), weather emojis, price chips, animated arrow Cork→Dublin with "+400 units" label
5. Forecast strip shows Fri/Sat/Sun for both cities
6. Clicking heatwave or Six Nations pill swaps the card to "Preview unavailable"
7. Clicking the BBQ pill restores the full card
8. "Show me why" opens the drawer; backdrop click closes it
9. Drawer bullets are expandable, charts render inline
10. "Approve" dims the card and shows a toast that auto-dismisses
11. No TypeScript errors, no console errors, no unused imports

If any item fails, fix it before reporting done.
