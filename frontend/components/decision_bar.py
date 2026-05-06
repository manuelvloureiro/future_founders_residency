from fasthtml.common import Button, Div, NotStr, Span

from .stage import stage_card, stage_header


CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
EDIT_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'
X_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'


def decision_bar(approved: bool) -> Div:
    if approved:
        status_pill = Span(
            Div(NotStr(CHECK_ICON), cls="w-3.5 h-3.5"),
            Span("Approved · scheduled", cls="ml-1.5"),
            cls="inline-flex items-center px-2.5 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded",
        )
        body = Span(
            "Reallocation truck dispatching Thu 06:00 · price changes go live Wed 00:00",
            cls="text-sm text-slate-600",
        )
        approve_btn = Button(
            Div(NotStr(CHECK_ICON), cls="w-4 h-4 mr-1.5"),
            Span("Approved"),
            cls="px-5 py-2.5 bg-emerald-600 text-white text-sm font-semibold rounded-lg shadow-sm flex items-center cursor-default opacity-90",
            disabled=True,
        )
    else:
        status_pill = Span(
            Span(cls="w-1.5 h-1.5 rounded-full bg-amber-500 inline-block joey-pulse"),
            Span("Awaiting your decision", cls="ml-1.5"),
            cls="inline-flex items-center px-2.5 py-1 bg-amber-50 text-amber-700 text-xs font-semibold rounded border border-amber-200",
        )
        body = Span(
            "Keith will execute these actions automatically once approved.",
            cls="text-sm text-slate-600",
        )
        approve_btn = Button(
            Div(NotStr(CHECK_ICON), cls="w-4 h-4 mr-1.5"),
            Span("Approve plan"),
            cls="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors flex items-center",
            hx_post="/approve",
            hx_target="#workflow",
            hx_swap="outerHTML",
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
                cls="flex items-center",
            ),
            Div(
                Button(
                    Div(NotStr(EDIT_ICON), cls="w-4 h-4 mr-1.5"),
                    Span("Modify"),
                    cls="px-4 py-2.5 border border-slate-200 text-sm font-medium rounded-lg hover:bg-slate-50 transition-colors text-slate-700 flex items-center",
                ),
                Button(
                    Div(NotStr(X_ICON), cls="w-4 h-4 mr-1.5"),
                    Span("Reject"),
                    cls="px-4 py-2.5 border border-slate-200 text-sm font-medium rounded-lg hover:bg-rose-50 hover:border-rose-200 hover:text-rose-700 transition-colors text-slate-700 flex items-center",
                ),
                approve_btn,
                cls="flex items-center gap-2",
            ),
            cls="flex items-center justify-between",
        ),
    )
