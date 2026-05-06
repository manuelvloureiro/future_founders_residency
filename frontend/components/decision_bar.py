from fasthtml.common import Div, NotStr, Span

from .recommendation_panel import projected_impact_strip
from .stage import stage_card


CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'


def decision_bar(approved: bool, action_states: dict | None = None, bbq: dict | None = None) -> Div:
    action_states = action_states or {0: "pending", 1: "pending", 2: "pending"}
    counts = {
        "approved": sum(1 for v in action_states.values() if v == "approved"),
        "escalated": sum(1 for v in action_states.values() if v == "escalated"),
        "rejected": sum(1 for v in action_states.values() if v == "rejected"),
        "pending": sum(1 for v in action_states.values() if v == "pending"),
    }
    total = len(action_states)
    decided = total - counts["pending"]

    if approved or (counts["pending"] == 0 and counts["approved"] == total):
        status_pill = Span(
            Div(NotStr(CHECK_ICON), cls="w-3.5 h-3.5"),
            Span("All approved · scheduled", cls="ml-1.5"),
            cls="inline-flex items-center px-2.5 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded",
        )
        body = Span(
            "Reallocation truck dispatching Sat 04:00 · price changes go live tonight 00:00",
            cls="text-sm text-slate-600",
        )
    elif counts["pending"] == 0:
        status_pill = Span(
            Div(NotStr(CHECK_ICON), cls="w-3.5 h-3.5"),
            Span("All lines decided", cls="ml-1.5"),
            cls="inline-flex items-center px-2.5 py-1 bg-sky-100 text-sky-700 text-xs font-semibold rounded",
        )
        body = Span(
            f"{counts['approved']} approved · {counts['escalated']} escalated · {counts['rejected']} rejected",
            cls="text-sm text-slate-600",
        )
    else:
        status_pill = Span(
            Span(cls="w-1.5 h-1.5 rounded-full bg-amber-500 inline-block joey-pulse"),
            Span(f"{decided} of {total} decided", cls="ml-1.5"),
            cls="inline-flex items-center px-2.5 py-1 bg-amber-50 text-amber-700 text-xs font-semibold rounded border border-amber-200",
        )
        body = Span(
            "Approve, escalate, or reject each line above. IDM executes once every line is decided.",
            cls="text-sm text-slate-600",
        )

    chip_cls = "text-[10px] font-semibold px-2 py-0.5 rounded inline-flex items-center"
    chips = Div(
        Span(f"✓ {counts['approved']}", cls=f"{chip_cls} bg-emerald-50 text-emerald-700"),
        Span(f"↑ {counts['escalated']}", cls=f"{chip_cls} bg-amber-50 text-amber-700 ml-1.5"),
        Span(f"✕ {counts['rejected']}", cls=f"{chip_cls} bg-rose-50 text-rose-700 ml-1.5"),
        Span(f"○ {counts['pending']}", cls=f"{chip_cls} bg-slate-100 text-slate-600 ml-1.5"),
        cls="flex items-center",
    )

    impact_block = (
        projected_impact_strip(bbq["impact"]) if bbq else Div()
    )

    return stage_card(
        Div(
            Div(
                Div(
                    Span(
                        "04",
                        cls="w-6 h-6 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center shrink-0",
                    ),
                    Div(
                        Div(
                            Span("Decision", cls="text-sm font-semibold text-slate-900"),
                            status_pill,
                            cls="flex items-center gap-2",
                        ),
                        body,
                        cls="flex flex-col",
                    ),
                    cls="flex items-center gap-3",
                ),
                chips,
                cls="flex items-center justify-between gap-4",
            ),
            impact_block,
            cls="flex flex-col gap-3",
        ),
    )
