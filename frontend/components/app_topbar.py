from fasthtml.common import Div, NotStr, Span


SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
BELL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9z"/><path d="M10 21a2 2 0 0 0 4 0"/></svg>'
HELP_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 0 1 5 0c0 1.5-2.5 2-2.5 4M12 17h.01"/></svg>'


def decisions_counter(decisions_today: int) -> Div:
    return Div(
        Div(
            Span(
                str(decisions_today),
                cls="text-base font-bold text-slate-900 tabular-nums leading-none",
                id="decisions-count",
            ),
            Span(
                "decisions today",
                cls="text-[10px] uppercase tracking-wider text-slate-500 font-semibold ml-1.5",
            ),
            cls="flex items-baseline",
        ),
        Div(
            Span("vs", cls="text-[10px] text-slate-400"),
            Span("1.2/wk human baseline", cls="text-[10px] text-slate-500 font-medium ml-1"),
            cls="flex items-center gap-0.5 mt-0.5",
        ),
        cls="px-3 py-1.5 bg-gradient-to-br from-emerald-50 to-white border border-emerald-200 rounded-md leading-tight",
    )


def app_topbar(monitoring_label: str, decisions_today: int = 47) -> Div:
    return Div(
        Div(
            Div(
                Span("Workspace", cls="text-slate-400"),
                Span("/", cls="text-slate-300"),
                Span("Insights", cls="text-slate-400"),
                Span("/", cls="text-slate-300"),
                Span("Barbecue weekend", cls="text-slate-900 font-medium"),
                cls="flex items-center gap-2 text-xs",
            ),
            cls="flex items-center",
        ),
        Div(
            Div(
                Div(
                    NotStr(SEARCH_ICON),
                    cls="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                Span(
                    "Search insights, SKUs, stores…",
                    cls="text-sm text-slate-400",
                ),
                Span(
                    "⌘K",
                    cls="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-semibold text-slate-400 bg-slate-100 border border-slate-200 rounded px-1.5 py-0.5",
                ),
                cls="relative pl-9 pr-12 py-2 w-80 bg-slate-50 border border-slate-200 rounded-lg flex items-center",
            ),
            Div(
                Span(
                    cls="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block joey-pulse"
                ),
                Span("Live", cls="text-xs font-medium text-slate-700"),
                Span("·", cls="text-slate-300"),
                Span("IE", cls="text-xs text-slate-500"),
                cls="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 border border-emerald-200 rounded-md",
            ),
            decisions_counter(decisions_today),
            Div(
                Div(NotStr(HELP_ICON), cls="w-4 h-4 text-slate-500"),
                cls="p-2 hover:bg-slate-100 rounded-lg cursor-pointer",
            ),
            Div(
                Div(NotStr(BELL_ICON), cls="w-4 h-4 text-slate-500"),
                Span(
                    cls="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-emerald-500 ring-2 ring-white"
                ),
                cls="p-2 hover:bg-slate-100 rounded-lg cursor-pointer relative",
            ),
            cls="flex items-center gap-3",
        ),
        cls="sticky top-0 z-20 bg-white/80 backdrop-blur border-b border-slate-200 px-8 h-14 flex items-center justify-between",
    )
