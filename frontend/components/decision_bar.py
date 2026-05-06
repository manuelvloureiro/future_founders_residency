from fasthtml.common import Div, Span

from .recommendation_panel import projected_impact_strip
from .stage import stage_card, stage_header


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
        subtitle = "All approved · scheduled"
        status_tone = "emerald"
        body_text = "Reallocation truck dispatching Sat 04:00 · price changes go live tonight 00:00"
    elif counts["pending"] == 0:
        subtitle = "All lines decided"
        status_tone = "sky"
        body_text = f"{counts['approved']} approved · {counts['escalated']} escalated · {counts['rejected']} rejected"
    else:
        subtitle = f"{decided} of {total} decided"
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

    impact_block = (
        projected_impact_strip(bbq["impact"]) if bbq else Div()
    )

    return stage_card(
        stage_header(
            "04",
            "Decision",
            subtitle,
            status=f"{decided}/{total} decided",
            status_tone=status_tone,
        ),
        Div(
            Span(body_text, cls="text-sm text-slate-600"),
            chips,
            cls="flex items-center justify-between gap-4",
        ),
        impact_block,
    )
