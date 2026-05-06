from fasthtml.common import Div, NotStr, Span


JOEY_LOGO = """
<svg viewBox="0 0 32 32" class="w-7 h-7">
  <defs>
    <linearGradient id="joey-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22c55e"/>
      <stop offset="100%" stop-color="#0ea5e9"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#joey-grad)"/>
  <path d="M11 11 h6 a4 4 0 0 1 4 4 v3 a4 4 0 0 1 -4 4 h-1 a3 3 0 0 1 -3 -3" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="20.5" cy="11.5" r="1.6" fill="white"/>
</svg>
"""


def nav_item(icon_svg: str, label: str, active: bool = False, badge: str | None = None) -> Div:
    base = "group flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors"
    if active:
        cls = f"{base} bg-white/10 text-white"
    else:
        cls = f"{base} text-slate-400 hover:text-white hover:bg-white/5"

    children = [
        Div(NotStr(icon_svg), cls="w-4 h-4 shrink-0"),
        Span(label, cls="flex-1"),
    ]
    if badge:
        children.append(
            Span(
                badge,
                cls="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300",
            )
        )

    return Div(*children, cls=cls)


ICON_INSIGHTS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/><circle cx="12" cy="12" r="4"/></svg>'
ICON_INVENTORY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7l9-4 9 4v10l-9 4-9-4V7z"/><path d="M3 7l9 4 9-4M12 11v10"/></svg>'
ICON_PRICING = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12V8a2 2 0 0 0-2-2h-7l-9 9 7 7 9-9z"/><circle cx="7.5" cy="7.5" r="1.2"/></svg>'
ICON_FORECAST = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18l5-6 4 4 8-9"/><path d="M21 7v5h-5"/></svg>'
ICON_RUNS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_SETTINGS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>'


def sidebar() -> Div:
    return Div(
        Div(
            Div(
                NotStr(JOEY_LOGO),
                Div(
                    Span("IDM", cls="text-white font-semibold tracking-tight"),
                    Span(
                        "The agentic retailer",
                        cls="text-[11px] text-emerald-400/80 -mt-0.5 block font-medium",
                    ),
                    cls="flex flex-col leading-tight",
                ),
                cls="flex items-center gap-2.5 px-3 py-4",
            ),
            cls="border-b border-white/5",
        ),
        Div(
            Div(
                "Workspace",
                cls="px-3 mt-4 mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500",
            ),
            nav_item(ICON_INSIGHTS, "Insights", active=True, badge="3"),
            nav_item(ICON_INVENTORY, "Inventory"),
            nav_item(ICON_PRICING, "Pricing"),
            nav_item(ICON_FORECAST, "Forecasts"),
            nav_item(ICON_RUNS, "Runs"),
            Div(
                "Account",
                cls="px-3 mt-6 mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500",
            ),
            nav_item(ICON_SETTINGS, "Settings"),
            cls="px-2 py-2 flex-1 overflow-y-auto",
        ),
        Div(
            Div(
                Div(
                    "🛒",
                    cls="w-8 h-8 rounded-full bg-slate-800 text-white text-sm flex items-center justify-center",
                ),
                Div(
                    Span(
                        "Keith",
                        cls="text-sm text-white font-medium block leading-tight",
                    ),
                    Span(
                        "Category Manager · Fresh & meat",
                        cls="text-[11px] text-slate-400 block leading-tight",
                    ),
                ),
                cls="flex items-center gap-2.5",
            ),
            cls="border-t border-white/5 px-4 py-3",
        ),
        cls="fixed left-0 top-0 bottom-0 w-52 bg-slate-950 flex flex-col z-30",
    )
