from fasthtml.common import Div, P, Span

from .decision_bar import decision_bar
from .recommendation_panel import recommendation_panel
from .signal_strip import signal_strip
from .situation_panel import situation_panel
from .stage import stage_card, stage_connector, stage_header


def thinking_overlay(message: str) -> Div:
    return Div(
        Div(
            Div(
                Div(
                    Span(
                        cls="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block joey-thinking-dot"
                    ),
                    Span(
                        cls="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block joey-thinking-dot ml-1"
                    ),
                    Span(
                        cls="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block joey-thinking-dot ml-1"
                    ),
                    cls="flex items-center mr-3 shrink-0",
                ),
                Div(
                    Span(
                        "IDM is thinking",
                        cls="text-[10px] uppercase tracking-wider text-emerald-700 font-semibold block",
                    ),
                    Span(
                        message,
                        cls="text-sm text-slate-700 font-medium block",
                    ),
                ),
                cls="flex items-center",
            ),
            Div(cls="joey-skeleton h-3 mt-3 w-2/3"),
            Div(cls="joey-skeleton h-3 mt-2 w-1/2"),
            Div(cls="joey-skeleton h-3 mt-2 w-3/4"),
            cls="bg-white rounded-xl border border-emerald-200 shadow-sm p-6",
        ),
        cls="joey-stage-thinking",
    )


def stage_wrap(real_stage: Div, thinking_msg: str | None) -> Div:
    children = [Div(real_stage, cls="joey-stage-real")]
    if thinking_msg is not None:
        children.append(thinking_overlay(thinking_msg))
    return Div(*children, cls="joey-stage-wrap")


def unavailable_stage(insight: dict) -> Div:
    return stage_card(
        stage_header(
            "—",
            insight["title"],
            insight["subtitle"],
            status="Queued",
            status_tone="slate",
        ),
        Div(
            Div(
                Span("⏳", cls="text-3xl"),
                P(
                    "Preview unavailable in this demo",
                    cls="text-slate-500 text-sm mt-3",
                ),
                P(
                    "IDM is still gathering signals for this insight. Check back when it moves to Pending review.",
                    cls="text-slate-400 text-xs mt-1",
                ),
                cls="text-center py-8",
            ),
            cls="flex items-center justify-center",
        ),
    )


def workflow(
    scenario: dict,
    selected_id: str,
    approved: bool,
    fast: bool = False,
    actions: dict | None = None,
) -> Div:
    insight = next(
        (i for i in scenario["insights"] if i["id"] == selected_id),
        scenario["insights"][0],
    )

    workflow_cls = "space-y-4"
    if fast:
        workflow_cls += " joey-fast"

    if insight["id"] == "bbq":
        bbq = scenario["bbq"]
        action_states = actions or {0: "pending", 1: "pending", 2: "pending"}
        stages = [
            stage_wrap(signal_strip(scenario, selected_id), None),
            stage_wrap(
                situation_panel(bbq),
                "Reading weather, sales, and inventory feeds…",
            ),
            stage_wrap(
                recommendation_panel(bbq, action_states=action_states),
                "Simulating reallocation + price changes against guardrails…",
            ),
            stage_wrap(
                decision_bar(approved, action_states=action_states, bbq=bbq),
                "Preparing plan for your review…",
            ),
        ]
    else:
        stages = [
            stage_wrap(signal_strip(scenario, selected_id), None),
            stage_wrap(unavailable_stage(insight), None),
        ]

    if approved and insight["id"] == "bbq":
        outer_extra = " opacity-60 pointer-events-none"
    else:
        outer_extra = ""

    return Div(
        *stages,
        cls=f"{workflow_cls}{outer_extra}",
        id="workflow",
    )
