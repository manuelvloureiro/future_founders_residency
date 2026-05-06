from fasthtml.common import Button, Div, H3, NotStr, P, Span

from .charts import mini_bar_chart, mini_line_chart


CHEVRON_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
DOC_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'


def evidence_block(evidence: dict) -> Div:
    if evidence["type"] == "bar":
        return Div(
            Div(
                Span(
                    evidence["label"],
                    cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold",
                ),
                cls="mb-2",
            ),
            Div(
                mini_bar_chart(evidence["bars"]),
                Div(
                    Div(
                        Span(cls="w-2.5 h-2.5 rounded-sm bg-emerald-600 inline-block"),
                        Span("Dublin", cls="text-xs text-slate-600 ml-1.5"),
                        cls="flex items-center",
                    ),
                    Div(
                        Span(cls="w-2.5 h-2.5 rounded-sm bg-amber-500 inline-block"),
                        Span("Cork", cls="text-xs text-slate-600 ml-1.5"),
                        cls="flex items-center",
                    ),
                    cls="space-y-1",
                ),
                cls="flex items-center gap-6",
            ),
            cls="mt-3 p-4 bg-slate-50 rounded-lg border border-slate-100",
        )

    if evidence["type"] == "line":
        return Div(
            Div(
                Span(
                    evidence["label"],
                    cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold",
                ),
                cls="mb-2",
            ),
            mini_line_chart(evidence["points"]),
            cls="mt-3 p-4 bg-slate-50 rounded-lg border border-slate-100",
        )

    return Div(
        Div(
            Span(
                evidence["label"],
                cls="text-[10px] uppercase tracking-wider text-slate-400 font-semibold",
            ),
            cls="mb-2",
        ),
        Div(
            Div(
                Span(evidence["dublin"], cls="text-3xl font-bold text-rose-600 block leading-none"),
                Span("Dublin · days of cover", cls="text-[11px] text-slate-500 mt-1 block"),
                cls="flex-1",
            ),
            Div(
                Span(evidence["cork"], cls="text-3xl font-bold text-emerald-600 block leading-none"),
                Span("Cork · days of cover", cls="text-[11px] text-slate-500 mt-1 block"),
                cls="flex-1",
            ),
            cls="flex gap-6",
        ),
        cls="mt-3 p-4 bg-slate-50 rounded-lg border border-slate-100",
    )


def why_bullet(b: dict, idx: int, expanded_idx: int | None) -> Div:
    expanded = expanded_idx == idx
    chevron_cls = "w-4 h-4 text-slate-400 transition-transform" + (" rotate-180" if expanded else "")

    target = "" if expanded else f"?expand={idx}"

    children = [
        Div(
            Div(
                Span(
                    str(idx + 1),
                    cls="w-6 h-6 rounded-md bg-slate-100 text-slate-600 text-xs font-semibold flex items-center justify-center shrink-0",
                ),
                Div(
                    P(b["claim"], cls="text-sm text-slate-800 font-medium leading-snug"),
                    Div(
                        Div(NotStr(DOC_ICON), cls="w-3 h-3 text-slate-400"),
                        Span(b["source"], cls="text-[11px] text-slate-500 ml-1"),
                        cls="flex items-center mt-1",
                    ),
                    cls="flex-1 min-w-0",
                ),
                Div(NotStr(CHEVRON_ICON), cls=chevron_cls),
                cls="flex items-start gap-3",
            ),
            cls="cursor-pointer",
            hx_get=f"/why{target}",
            hx_target="#why-drawer",
            hx_swap="outerHTML",
        ),
    ]
    if expanded:
        children.append(evidence_block(b["evidence"]))

    return Div(
        *children,
        cls="p-4 bg-white border border-slate-200 rounded-lg hover:border-slate-300 transition-colors",
    )


def why_drawer_closed() -> Div:
    return Div(id="why-drawer")


def why_drawer_open(bullets: list[dict], expanded_idx: int | None = None) -> Div:
    return Div(
        Div(
            cls="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 joey-fade-in",
            hx_get="/why/close",
            hx_target="#why-drawer",
            hx_swap="outerHTML",
        ),
        Div(
            Div(
                Div(
                    Span(
                        cls="w-10 h-1 rounded-full bg-slate-200 mx-auto block mb-4",
                    ),
                    cls="px-8 pt-3",
                ),
                Div(
                    Div(
                        Span(
                            "Reasoning trace",
                            cls="text-[10px] uppercase tracking-wider text-emerald-600 font-semibold",
                        ),
                        H3(
                            "Why Keith recommends this plan",
                            cls="text-lg font-semibold text-slate-900 mt-1",
                        ),
                        Span(
                            f"{len(bullets)} signals · cross-checked against historical comparables",
                            cls="text-xs text-slate-500 mt-1 block",
                        ),
                    ),
                    Button(
                        "×",
                        cls="text-slate-400 hover:text-slate-600 text-2xl leading-none w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center",
                        hx_get="/why/close",
                        hx_target="#why-drawer",
                        hx_swap="outerHTML",
                    ),
                    cls="flex items-start justify-between px-8 pb-4",
                ),
                Div(
                    Span(
                        "Signals",
                        cls="px-3 py-1.5 text-xs font-semibold text-slate-900 border-b-2 border-emerald-500 -mb-px",
                    ),
                    Span(
                        "Comparables",
                        cls="px-3 py-1.5 text-xs font-medium text-slate-400",
                    ),
                    Span(
                        "Simulation",
                        cls="px-3 py-1.5 text-xs font-medium text-slate-400",
                    ),
                    Span(
                        "Audit log",
                        cls="px-3 py-1.5 text-xs font-medium text-slate-400",
                    ),
                    cls="flex items-center gap-2 px-8 border-b border-slate-200",
                ),
                cls="border-b border-slate-100",
            ),
            Div(
                *[why_bullet(b, i, expanded_idx) for i, b in enumerate(bullets)],
                cls="px-8 py-6 space-y-3 overflow-y-auto",
                style="max-height: calc(75vh - 180px);",
            ),
            cls="fixed bottom-0 left-0 right-0 z-50 bg-white rounded-t-2xl shadow-2xl max-w-5xl mx-auto joey-slide-up",
            style="max-height: 75vh;",
        ),
        id="why-drawer",
    )
