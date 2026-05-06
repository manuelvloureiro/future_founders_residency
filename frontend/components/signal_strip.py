from fasthtml.common import Button, Div, NotStr, Span

from .stage import stage_card, stage_header


INSIGHT_DETAIL = {
    "bbq": {
        "summary": "Diverging weekend weather is splitting BBQ demand across the country. IDM proposes shifting stock from rain-hit Cork to sunny Dublin and adjusting prices to clear inventory before spoilage.",
        "tags": ["Weather signal", "Fresh meat", "2 cities", "48h window"],
        "sources": {"weather": True, "social": False, "pos": True, "inventory": True, "events": False},
    },
    "heatwave": {
        "summary": "A 4-day heatwave is forecast nationwide. IDM is monitoring ice cream and frozen-dessert sell-through across all 142 stores to pre-position inventory.",
        "tags": ["Weather signal", "Frozen", "Nationwide", "96h window"],
        "sources": {"weather": True, "social": False, "pos": True, "inventory": False, "events": False},
    },
    "sixnations": {
        "summary": "Ireland plays at home this weekend. Historical data shows snacks and beer uplift of ~30% in catchment areas around the stadium and major pubs.",
        "tags": ["Event signal", "Snacks & beer", "Catchment areas", "72h window"],
        "sources": {"weather": False, "social": True, "pos": False, "inventory": False, "events": True},
    },
}

SOURCE_META = [
    ("weather", "🌤", "Weather"),
    ("social", "💬", "Social"),
    ("pos", "🧾", "Sales"),
    ("inventory", "📦", "Stock"),
    ("events", "🎟", "Events"),
]


def source_row(insight_id: str) -> Div:
    sources = INSIGHT_DETAIL.get(insight_id, {}).get("sources", {})
    pills = []
    for key, icon, label in SOURCE_META:
        active = sources.get(key, False)
        if active:
            cls = "inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[9px] font-semibold bg-emerald-100 text-emerald-700 border border-emerald-200"
        else:
            cls = "inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[9px] font-medium bg-slate-50 text-slate-400 border border-slate-100"
        pills.append(
            Span(
                Span(icon, cls="text-[10px] leading-none"),
                Span(label, cls="leading-none"),
                cls=cls,
                title=label + (" (signal active)" if active else " (no signal)"),
            )
        )
    return Div(*pills, cls="flex flex-wrap gap-1 mt-2.5")


def insight_detail_box(insight: dict) -> Div:
    detail = INSIGHT_DETAIL.get(insight["id"])
    if not detail:
        return Div()

    return Div(
        Div(
            Span(
                "Description",
                cls="text-[10px] uppercase tracking-wider text-emerald-700 font-semibold",
            ),
            Span(insight["icon"], cls="text-base"),
            cls="flex items-center justify-between mb-2",
        ),
        Span(
            detail["summary"],
            cls="text-sm text-slate-700 leading-relaxed block",
        ),
        Div(
            *[
                Span(
                    t,
                    cls="text-[10px] font-medium px-2 py-0.5 rounded bg-white border border-emerald-200 text-emerald-700",
                )
                for t in detail["tags"]
            ],
            cls="flex flex-wrap gap-1.5 mt-3",
        ),
        cls="mt-3 p-4 rounded-lg bg-gradient-to-br from-emerald-50/70 to-white border border-emerald-100",
    )


def insight_card(insight: dict, selected_id: str) -> Button:
    is_selected = insight["id"] == selected_id
    is_available = insight.get("available", False)

    if is_selected:
        cls = (
            "group relative flex-1 text-left p-4 rounded-lg border-2 border-emerald-500 "
            "bg-gradient-to-br from-emerald-50 to-white shadow-sm transition-all"
        )
        status_pill = Span(
            Span(cls="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block joey-pulse"),
            Span("Active", cls="ml-1.5"),
            cls="inline-flex items-center text-[10px] font-semibold uppercase tracking-wider text-emerald-700",
        )
    elif is_available:
        cls = (
            "group flex-1 text-left p-4 rounded-lg border border-slate-200 bg-white "
            "hover:border-slate-300 hover:shadow-sm transition-all"
        )
        status_pill = Span(
            "Pending review",
            cls="text-[10px] font-semibold uppercase tracking-wider text-slate-400",
        )
    else:
        cls = (
            "group flex-1 text-left p-4 rounded-lg border border-dashed border-slate-200 "
            "bg-slate-50/50 hover:bg-slate-50 transition-all"
        )
        status_pill = Span(
            "Queued",
            cls="text-[10px] font-semibold uppercase tracking-wider text-slate-400",
        )

    confidence = {"bbq": 87, "heatwave": 64, "sixnations": 71}.get(insight["id"], 50)
    severity = {"bbq": "High", "heatwave": "Med", "sixnations": "Med"}.get(
        insight["id"], "Low"
    )
    sev_color = {"High": "text-rose-600 bg-rose-50", "Med": "text-amber-600 bg-amber-50", "Low": "text-slate-600 bg-slate-100"}[severity]

    return Button(
        Div(
            Div(
                Span(insight["icon"], cls="text-2xl"),
                status_pill,
                cls="flex items-start justify-between mb-3",
            ),
            Div(
                Span(insight["title"], cls="text-sm font-semibold text-slate-900 block"),
                Span(insight["subtitle"], cls="text-xs text-slate-500 block mt-0.5"),
            ),
            source_row(insight["id"]),
            Div(
                Span(
                    severity,
                    cls=f"text-[10px] font-semibold px-1.5 py-0.5 rounded {sev_color}",
                ),
                Span(f"{confidence}% conf.", cls="text-[10px] text-slate-400 ml-auto"),
                cls="flex items-center gap-2 mt-3 pt-3 border-t border-slate-100",
            ),
        ),
        cls=cls,
        hx_get=f"/select/{insight['id']}",
        hx_target="#workflow",
        hx_swap="outerHTML",
    )


def signal_strip(scenario: dict, selected_id: str) -> Div:
    selected = next(
        (i for i in scenario["insights"] if i["id"] == selected_id),
        scenario["insights"][0],
    )
    return stage_card(
        stage_header(
            "01",
            "Signal",
            "What IDM is noticing",
            status=f"{len(scenario['insights'])} active",
            status_tone="emerald",
        ),
        Div(
            *[insight_card(i, selected_id) for i in scenario["insights"]],
            cls="flex gap-3",
        ),
        insight_detail_box(selected),
    )
