from fasthtml.common import Button, Div, NotStr, Span


SCROLL_TO_STAGE = (
    "var w = this.closest('.joey-stage-wrap');"
    "if (w) { w.scrollIntoView({behavior: 'smooth', block: 'start'}); }"
)


def stage_header(
    number: str,
    title: str,
    subtitle: str,
    status: str | None = None,
    status_tone: str = "slate",
) -> Div:
    tone_map = {
        "slate": "bg-slate-100 text-slate-600 border-slate-200",
        "emerald": "bg-emerald-50 text-emerald-700 border-emerald-200",
        "amber": "bg-amber-50 text-amber-700 border-amber-200",
        "sky": "bg-sky-50 text-sky-700 border-sky-200",
    }
    status_cls = tone_map.get(status_tone, tone_map["slate"])

    if number.strip().isdigit():
        number_node = Button(
            number,
            type="button",
            onclick=SCROLL_TO_STAGE,
            title=f"Jump to stage {number}",
            cls="w-7 h-7 rounded-md bg-slate-900 text-white text-xs font-semibold flex items-center justify-center shrink-0 hover:bg-emerald-600 transition-colors cursor-pointer",
        )
    else:
        number_node = Span(
            number,
            cls="w-7 h-7 rounded-md bg-slate-900 text-white text-xs font-semibold flex items-center justify-center shrink-0",
        )

    children = [
        Div(
            number_node,
            Div(
                Div(
                    Span(title, cls="text-lg font-semibold text-slate-900"),
                    Span(
                        subtitle,
                        cls="text-base text-slate-500 ml-2",
                    ),
                    cls="flex items-baseline flex-wrap",
                ),
                cls="flex flex-col",
            ),
            cls="flex items-center gap-3",
        )
    ]

    if status:
        children.append(
            Span(
                status,
                cls=f"text-xs font-semibold uppercase tracking-wider px-2.5 py-1 rounded border {status_cls}",
            )
        )

    return Div(*children, cls="flex items-center justify-between mb-4")


def stage_card(*children, accent: str | None = None) -> Div:
    base = "bg-white rounded-xl border border-slate-200 shadow-sm"
    if accent == "top":
        base = (
            "bg-white rounded-xl border border-slate-200 shadow-sm "
            "border-t-2 border-t-emerald-500"
        )
    return Div(*children, cls=f"{base} p-6")


CONNECTOR = """
<div class="flex justify-center my-2">
  <svg viewBox="0 0 8 24" class="w-2 h-6 text-slate-300">
    <line x1="4" y1="0" x2="4" y2="24" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 3"/>
  </svg>
</div>
"""


def stage_connector() -> Div:
    return Div(NotStr(CONNECTOR))
