from fasthtml.common import Button, Div, NotStr, Span

from .ireland_map import ireland_map
from .stage import stage_card, stage_header


LOCATION_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 7-8 12-8 12s-8-5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'


CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
ARROW_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
TRUCK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="6" width="14" height="11" rx="1"/><path d="M15 9h4l3 4v4h-7z"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/></svg>'
TAG_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12V8a2 2 0 0 0-2-2h-7l-9 9 7 7 9-9z"/><circle cx="7.5" cy="7.5" r="1.2"/></svg>'
TAGDOWN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12V8a2 2 0 0 0-2-2h-7l-9 9 7 7 9-9z"/><path d="M7.5 7.5l0 0"/><path d="M11 14l4 0M13 12l0 4"/></svg>'


def action_row(idx: int, icon: str, text: str, badge: str, badge_tone: str) -> Div:
    tone_map = {
        "emerald": "bg-emerald-50 text-emerald-700",
        "amber": "bg-amber-50 text-amber-700",
        "sky": "bg-sky-50 text-sky-700",
    }
    return Div(
        Div(
            Span(
                str(idx),
                cls="w-5 h-5 rounded-full bg-slate-900 text-white text-[10px] font-semibold flex items-center justify-center shrink-0",
            ),
            Div(NotStr(icon), cls="w-4 h-4 text-slate-500 shrink-0"),
            cls="flex items-center gap-2 shrink-0",
        ),
        Span(text, cls="text-sm text-slate-700 flex-1"),
        Span(
            badge,
            cls=f"text-[10px] font-semibold px-2 py-0.5 rounded {tone_map[badge_tone]} shrink-0",
        ),
        cls="flex items-center gap-3 px-3 py-2.5 bg-slate-50 hover:bg-white border border-transparent hover:border-slate-200 rounded-lg transition-colors",
    )


def impact_metric(value: str, label: str, sublabel: str, tone: str) -> Div:
    tone_map = {
        "emerald": "text-emerald-600",
        "rose": "text-rose-600",
        "sky": "text-sky-600",
    }
    return Div(
        Span(value, cls=f"text-2xl font-bold {tone_map[tone]} block"),
        Span(label, cls="text-xs text-slate-500 block mt-0.5"),
        Span(sublabel, cls="text-[10px] text-slate-400 block"),
        cls="flex flex-col",
    )


def confidence_ring(pct: int) -> Div:
    radius = 26
    circumference = 2 * 3.14159 * radius
    offset = circumference * (1 - pct / 100)
    svg = f"""
    <svg viewBox="0 0 64 64" class="w-16 h-16 -rotate-90">
      <circle cx="32" cy="32" r="{radius}" stroke="#e2e8f0" stroke-width="5" fill="none"/>
      <circle cx="32" cy="32" r="{radius}" stroke="#10b981" stroke-width="5" fill="none"
              stroke-linecap="round"
              stroke-dasharray="{circumference}"
              stroke-dashoffset="{offset}"/>
    </svg>
    """
    return Div(
        Div(NotStr(svg)),
        Div(
            Span(f"{pct}%", cls="text-sm font-bold text-slate-900 block leading-none"),
            Span("conf.", cls="text-[9px] text-slate-400 leading-none"),
            cls="absolute inset-0 flex flex-col items-center justify-center",
        ),
        cls="relative w-16 h-16",
    )


def recommendation_panel(bbq: dict, on_show_why_target: str = "#why-drawer") -> Div:
    impact = bbq["impact"]
    realloc = bbq["reallocation"]

    actions_meta = [
        (TRUCK_ICON, bbq["actions"][0], f"{realloc['units']} units", "sky"),
        (TAG_ICON, bbq["actions"][1], "+5.6%", "emerald"),
        (TAGDOWN_ICON, bbq["actions"][2], "−8.8%", "amber"),
    ]

    map_column = Div(
        Div(
            Div(NotStr(LOCATION_ICON), cls="w-3.5 h-3.5 text-slate-400"),
            Span(
                "Geographic divergence",
                cls="text-[10px] uppercase tracking-wider text-slate-500 font-semibold",
            ),
            cls="flex items-center gap-1.5 mb-2",
        ),
        ireland_map(bbq["cities"]),
        Div(
            Div(
                Span(cls="w-2 h-2 rounded-full bg-emerald-500 inline-block"),
                Span("Dublin · stock-out risk", cls="text-[11px] text-slate-600 ml-1.5"),
                cls="flex items-center",
            ),
            Div(
                Span(cls="w-2 h-2 rounded-full bg-amber-500 inline-block"),
                Span("Cork · waste risk", cls="text-[11px] text-slate-600 ml-1.5"),
                cls="flex items-center",
            ),
            cls="flex items-center justify-center gap-4 mt-2",
        ),
        cls="bg-slate-50 rounded-lg p-4 border border-slate-100",
    )

    return stage_card(
        stage_header(
            "03",
            "Recommendation",
            "Keith's proposed plan",
            status="3 actions",
            status_tone="sky",
        ),
        Div(
            Div(
            Div(
                Div(
                    Span(
                        "Plan",
                        cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold",
                    ),
                    cls="mb-2",
                ),
                Div(
                    *[action_row(i + 1, ico, txt, bd, tone) for i, (ico, txt, bd, tone) in enumerate(actions_meta)],
                    cls="space-y-2",
                ),
                Div(
                    Div(
                        Span("🛡️", cls="text-sm"),
                        Span(
                            "Guardrails",
                            cls="text-[10px] uppercase tracking-wider text-slate-500 font-semibold ml-1.5",
                        ),
                        cls="flex items-center mb-1.5",
                    ),
                    Div(
                        Span(
                            "Price floor €11.00",
                            cls="text-[11px] px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-600",
                        ),
                        Span(
                            "Max 3 packs / customer",
                            cls="text-[11px] px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-600",
                        ),
                        Span(
                            "6h price-change cooldown",
                            cls="text-[11px] px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-600",
                        ),
                        Span(
                            "Margin ≥ 12%",
                            cls="text-[11px] px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-600",
                        ),
                        cls="flex flex-wrap gap-1.5",
                    ),
                    cls="mt-3 px-3 py-2.5 bg-slate-50 border border-slate-100 rounded-lg",
                ),
                cls="lg:col-span-2",
            ),
            Div(
                Div(
                    Div(
                        Span(
                            "Projected impact",
                            cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold",
                        ),
                        confidence_ring(87),
                        cls="flex items-start justify-between mb-3",
                    ),
                    Div(
                        impact_metric(
                            f"+€{impact['margin_eur']:,}",
                            "Margin uplift",
                            "vs do-nothing",
                            "emerald",
                        ),
                        impact_metric(
                            f"{impact['waste_kg']} kg",
                            "Waste avoided",
                            "Cork meat",
                            "emerald",
                        ),
                        impact_metric(
                            f"+{impact['sell_through_pct']}%",
                            "Sell-through",
                            "Dublin",
                            "sky",
                        ),
                        cls="grid grid-cols-3 gap-3 pt-3 border-t border-slate-100",
                    ),
                    cls="bg-gradient-to-br from-emerald-50/50 to-white border border-emerald-100 rounded-lg p-4",
                ),
                Div(
                    Span("Logistics window", cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold block"),
                    Div(
                        Span("🚚", cls="text-lg"),
                        Span(
                            f"{realloc['from_city']} → {realloc['to_city']}",
                            cls="text-sm font-semibold text-slate-700 ml-1",
                        ),
                        cls="flex items-center mt-1",
                    ),
                    Div(
                        Span(f"Departs {realloc['departs']}", cls="text-xs text-slate-500"),
                        Span("·", cls="text-slate-300 mx-1.5"),
                        Span(f"Arrives {realloc['arrives']}", cls="text-xs text-slate-500"),
                        cls="flex items-center mt-1",
                    ),
                    cls="bg-slate-50 border border-slate-100 rounded-lg p-3 mt-3",
                ),
                Button(
                    Span("Show me why", cls="mr-1.5"),
                    Div(NotStr(ARROW_ICON), cls="w-3.5 h-3.5"),
                    cls="w-full mt-3 px-4 py-2.5 text-sm font-medium text-emerald-700 bg-white border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors flex items-center justify-center",
                    hx_get="/why",
                    hx_target=on_show_why_target,
                    hx_swap="outerHTML",
                ),
            ),
            cls="flex flex-col gap-6",
            ),
            map_column,
            cls="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
    )
