from fasthtml.common import Button, Div, NotStr, Span

from .recommendation_panel import projected_impact_strip


ARROW_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'


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

    has_actionable = counts["approved"] + counts["escalated"] > 0
    if approved:
        proceed_label = "Approved"
        proceed_cls = "bg-emerald-600 text-white border-emerald-600 cursor-default opacity-90"
        proceed_disabled = True
    elif has_actionable:
        proceed_label = "Proceed"
        proceed_cls = "bg-emerald-600 text-white border-emerald-600 hover:bg-emerald-700 hover:border-emerald-700"
        proceed_disabled = False
    else:
        proceed_label = "Proceed"
        proceed_cls = "bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed"
        proceed_disabled = True

    proceed_btn_kwargs = {
        "cls": f"inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold rounded-lg border transition-colors {proceed_cls}",
    }
    if not proceed_disabled:
        proceed_btn_kwargs["hx_get"] = "/summary"
        proceed_btn_kwargs["hx_target"] = "#summary-modal"
        proceed_btn_kwargs["hx_swap"] = "outerHTML"
    else:
        proceed_btn_kwargs["disabled"] = True

    proceed_btn = Button(
        Span(proceed_label),
        Div(NotStr(ARROW_ICON), cls="w-3.5 h-3.5"),
        **proceed_btn_kwargs,
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
        Div(proceed_btn, cls="flex justify-end mt-3"),
        cls="mt-4 pt-4 border-t border-slate-100",
    )
