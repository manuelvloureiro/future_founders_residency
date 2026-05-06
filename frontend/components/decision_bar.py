from fasthtml.common import Div, Span

from .recommendation_panel import projected_impact_strip


_TONE_PILL = {
    "emerald": "bg-emerald-100 text-emerald-700 border-emerald-200",
    "sky": "bg-sky-100 text-sky-700 border-sky-200",
    "amber": "bg-amber-50 text-amber-700 border-amber-200",
}


def decision_footer(approved: bool, action_states: dict | None, bbq: dict | None) -> Div:
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
        status_label = "All approved · scheduled"
        status_tone = "emerald"
        body_text = "Reallocation truck dispatching Sat 04:00 · price changes go live tonight 00:00"
    elif counts["pending"] == 0:
        status_label = "All lines decided"
        status_tone = "sky"
        body_text = f"{counts['approved']} approved · {counts['escalated']} escalated · {counts['rejected']} rejected"
    else:
        status_label = f"{decided} of {total} decided"
        status_tone = "amber"
        body_text = "Approve, escalate, or reject each line above. IDM executes once every line is decided."

    chip_cls = "text-[10px] font-semibold px-2 py-0.5 rounded inline-flex items-center"
    chips = Div(
        Span(f"✓ {counts['approved']}", cls=f"{chip_cls} bg-emerald-50 text-emerald-700"),
        Span(f"↑ {counts['escalated']}", cls=f"{chip_cls} bg-amber-50 text-amber-700 ml-1.5"),
        Span(f"✕ {counts['rejected']}", cls=f"{chip_cls} bg-rose-50 text-rose-700 ml-1.5"),
        Span(f"○ {counts['pending']}", cls=f"{chip_cls} bg-slate-100 text-slate-600 ml-1.5"),
        cls="flex items-center",
    )

    status_pill = Span(
        status_label,
        cls=f"inline-flex items-center px-2.5 py-1 text-xs font-semibold rounded border {_TONE_PILL[status_tone]}",
    )

    impact_block = (
        projected_impact_strip(bbq["impact"], action_states=action_states) if bbq else Div()
    )

    return Div(
        Div(
            Div(
                Span("Decision", cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold mr-2"),
                status_pill,
                cls="flex items-center",
            ),
            chips,
            cls="flex items-center justify-between gap-4",
        ),
        Span(body_text, cls="text-xs text-slate-500 block mt-1"),
        Div(impact_block, cls="mt-3"),
        cls="mt-4 pt-4 border-t border-slate-100",
    )
