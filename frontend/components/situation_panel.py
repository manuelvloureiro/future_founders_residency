from fasthtml.common import Button, Div, NotStr, Span

from .forecast_strip import forecast_strip
from .stage import stage_card, stage_header


CLOCK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ARROW_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'


def why_now_timeline() -> Div:
    steps = [
        {
            "label": "Wed",
            "title": "First signal",
            "detail": "Met Éireann run flagged Sat–Sun divergence",
            "conf": 62,
            "state": "past",
        },
        {
            "label": "Thu",
            "title": "Confidence rising",
            "detail": "Sales data and 2 forecast runs corroborate",
            "conf": 73,
            "state": "past",
        },
        {
            "label": "Fri",
            "title": "Demand uptick — trigger",
            "detail": "Dublin barbecue-pack basket-adds +9% vs 4-week Friday morning baseline; Cork flat",
            "conf": 87,
            "state": "active",
        },
    ]

    nodes = []
    for i, s in enumerate(steps):
        is_active = s["state"] == "active"
        if is_active:
            dot_cls = "w-3 h-3 rounded-full bg-emerald-500 ring-4 ring-emerald-200 joey-pulse"
            label_cls = "text-[11px] font-semibold uppercase tracking-wider text-emerald-700 block"
            title_cls = "text-sm font-semibold text-slate-900 mt-0.5 block"
            detail_cls = "text-xs text-slate-600 leading-tight mt-0.5 block"
            conf_cls = "text-[11px] font-bold text-emerald-700 mt-1 block"
        else:
            dot_cls = "w-2.5 h-2.5 rounded-full bg-slate-300 ring-2 ring-slate-100"
            label_cls = "text-[11px] font-semibold uppercase tracking-wider text-slate-400 block"
            title_cls = "text-sm font-medium text-slate-600 mt-0.5 block"
            detail_cls = "text-xs text-slate-500 leading-tight mt-0.5 block"
            conf_cls = "text-[11px] font-semibold text-slate-400 mt-1 block"

        children = [
            Div(
                Span(cls=dot_cls),
                cls="flex items-center justify-center mb-1.5 relative z-10",
            ),
            Span(s["label"], cls=label_cls),
            Span(s["title"], cls=title_cls),
            Span(s["detail"], cls=detail_cls),
            Span(f"{s['conf']}% conf.", cls=conf_cls),
        ]

        if i < len(steps) - 1:
            line_color = "bg-emerald-300" if s["state"] == "past" else "bg-slate-200"
            children.append(
                Div(cls=f"absolute top-[5px] left-[55%] w-[90%] h-px {line_color} z-0")
            )

        nodes.append(
            Div(*children, cls="flex-1 text-center px-2 relative")
        )

    return Div(
        Div(
            Span("⚡", cls="text-sm"),
            Span(
                "Why now?",
                cls="text-[10px] uppercase tracking-wider text-slate-500 font-semibold ml-1.5",
            ),
            Span(
                "Friday AM · day before BBQ weekend",
                cls="text-[10px] text-slate-400 ml-auto",
            ),
            cls="flex items-center mb-3",
        ),
        Div(
            *nodes,
            cls="flex items-start",
        ),
        cls="px-4 py-3 bg-gradient-to-br from-slate-50 to-white border border-slate-200 rounded-lg mb-4",
    )


def metric_chip(
    label: str,
    value: str,
    tone: str = "slate",
    sublabel: str | None = None,
    value_size: str = "text-sm",
) -> Div:
    value_tone_map = {
        "slate": "text-slate-700",
        "rose": "text-rose-600",
        "emerald": "text-emerald-600",
        "amber": "text-amber-700",
    }
    container_tone_map = {
        "slate": "bg-slate-50 border-slate-100",
        "rose": "bg-rose-50 border-rose-200",
        "emerald": "bg-emerald-50 border-emerald-200",
        "amber": "bg-amber-50 border-amber-200",
    }
    sub_tone_map = {
        "slate": "text-slate-400",
        "rose": "text-rose-600",
        "emerald": "text-emerald-600",
        "amber": "text-amber-600",
    }
    children = [
        Span(label, cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold block"),
        Span(value, cls=f"{value_size} font-semibold {value_tone_map.get(tone, value_tone_map['slate'])} block mt-0.5"),
    ]
    if sublabel:
        children.append(
            Span(sublabel, cls=f"text-[10px] {sub_tone_map.get(tone, sub_tone_map['slate'])} font-medium block mt-0.5")
        )
    return Div(
        *children,
        cls=f"px-3 py-2 rounded-lg border {container_tone_map.get(tone, container_tone_map['slate'])}",
    )


def situation_panel(bbq: dict) -> Div:
    dublin = bbq["cities"]["dublin"]
    cork = bbq["cities"]["cork"]
    delta = abs(dublin["temp_c"] - cork["temp_c"])

    return stage_card(
        stage_header(
            "02",
            "Situation",
            f"Detected {bbq['headline'].lower()}",
            status="High impact",
            status_tone="amber",
        ),
        Div(
            Div(
                Div(
                    Span(
                        "Headline",
                        cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold",
                    ),
                    Div(
                        Div(
                            Div(
                                Span(f"{dublin['temp_c']}°C", cls="text-3xl font-bold text-slate-900"),
                                Span(dublin["emoji"], cls="text-2xl ml-1"),
                                cls="flex items-center justify-center",
                            ),
                            Span("Dublin", cls="text-sm text-slate-500 font-medium block text-center mt-0.5"),
                            cls="flex flex-col items-center",
                        ),
                        Span("vs", cls="text-xs text-slate-400 mx-4 self-center"),
                        Div(
                            Div(
                                Span(f"{cork['temp_c']}°C", cls="text-3xl font-bold text-slate-900"),
                                Span(cork["emoji"], cls="text-2xl ml-1"),
                                cls="flex items-center justify-center",
                            ),
                            Span("Cork", cls="text-sm text-slate-500 font-medium block text-center mt-0.5"),
                            cls="flex flex-col items-center",
                        ),
                        cls="flex items-center mt-1",
                    ),
                    Span(
                        f"Δ {delta}°C — exceeds 10°C divergence threshold",
                        cls="text-xs text-amber-700 bg-amber-50 inline-block px-2 py-0.5 rounded mt-2 border border-amber-200",
                    ),
                    cls="mb-4",
                ),
                Div(
                    metric_chip(
                        "Dublin stock",
                        f"{dublin['current_stock_units']:,} u",
                        tone="amber",
                        sublabel="1.5 d cover · stocks out Sat 15:00",
                    ),
                    metric_chip(
                        "Cork stock",
                        f"{cork['current_stock_units']:,} u",
                        tone="rose",
                        sublabel="14 d cover · ~180 kg waste risk",
                    ),
                    cls="grid grid-cols-2 gap-2 mb-4",
                ),
                why_now_timeline(),
                forecast_strip(bbq["forecast"]),
                Div(
                    Div(
                        Div(NotStr(CLOCK_ICON), cls="w-4 h-4 text-slate-400 shrink-0 mt-0.5"),
                        Div(
                            Span(
                                f"{bbq['last_comparable']['label']} · {bbq['last_comparable']['date']}",
                                cls="text-[10px] uppercase tracking-wider text-slate-500 font-semibold block",
                            ),
                            Span(
                                bbq["last_comparable"]["note"],
                                cls="text-xs text-slate-700 leading-relaxed mt-1 block",
                            ),
                        ),
                        cls="flex gap-2",
                    ),
                    cls="bg-gradient-to-br from-slate-50 to-white border border-slate-200 rounded-lg p-3 mt-4",
                ),
                Button(
                    Span("Show me why", cls="mr-1.5"),
                    Div(NotStr(ARROW_ICON), cls="w-3.5 h-3.5"),
                    cls="w-full mt-4 px-4 py-2.5 text-sm font-medium text-emerald-700 bg-white border border-emerald-200 rounded-lg hover:bg-emerald-50 transition-colors flex items-center justify-center",
                    hx_get="/why",
                    hx_target="#why-drawer",
                    hx_swap="outerHTML",
                ),
                cls="w-full",
            ),
            cls="flex flex-col gap-6",
        ),
    )
