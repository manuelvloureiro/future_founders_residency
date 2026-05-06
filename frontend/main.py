import asyncio

from fasthtml.common import Div, Link, Main, Script, Span, Style, fast_app, serve

from api import approve_insight, fetch_scenario
from components.app_topbar import app_topbar
from components.sidebar import sidebar
from components.workflow import workflow
from components.why_drawer import why_drawer_closed, why_drawer_open

state = {
    "selected_id": "bbq",
    "approved": False,
    "actions": {0: "pending", 1: "pending", 2: "pending"},
    "scenario": None,
    "scenario_lock": asyncio.Lock(),
    "toast": None,
}


def reset_actions():
    state["actions"] = {0: "approved", 1: "pending", 2: "escalated"}


async def get_scenario() -> dict:
    if state["scenario"] is None:
        async with state["scenario_lock"]:
            if state["scenario"] is None:
                state["scenario"] = await fetch_scenario()
    return state["scenario"]


HEAD_STYLES = """
@keyframes joey-pulse-kf {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.joey-pulse {
  animation: joey-pulse-kf 2s ease-in-out infinite;
}

@keyframes joey-pin-pulse-kf {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.5); }
}
.joey-pin-pulse {
  transform-origin: center;
  transform-box: fill-box;
  animation: joey-pin-pulse-kf 2s ease-in-out infinite;
}
.joey-pin-pulse-delay {
  animation-delay: 0.5s;
}

@keyframes joey-arrow-draw-kf {
  from { stroke-dashoffset: 600; opacity: 0; }
  to { stroke-dashoffset: 0; opacity: 1; }
}
.joey-arrow-draw {
  stroke-dasharray: 6 4;
  animation: joey-arrow-draw-kf 1.5s ease-in-out forwards;
}

@keyframes joey-slide-up-kf {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
.joey-slide-up {
  animation: joey-slide-up-kf 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

@keyframes joey-fade-in-kf {
  from { opacity: 0; }
  to { opacity: 1; }
}
.joey-fade-in {
  animation: joey-fade-in-kf 0.25s ease-out forwards;
}

@keyframes joey-stage-in-kf {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes joey-skeleton-shimmer-kf {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
.joey-skeleton {
  background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 50%, #f1f5f9 100%);
  background-size: 800px 100%;
  animation: joey-skeleton-shimmer-kf 1.4s linear infinite;
  border-radius: 0.5rem;
}

@keyframes joey-thinking-dots-kf {
  0%, 20% { opacity: 0.3; }
  50% { opacity: 1; }
  80%, 100% { opacity: 0.3; }
}
.joey-thinking-dot {
  animation: joey-thinking-dots-kf 1.2s ease-in-out infinite;
}
.joey-thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.joey-thinking-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes joey-fade-out-kf {
  to { opacity: 0; visibility: hidden; }
}

.joey-stage-wrap { position: relative; }
.joey-stage-real { opacity: 0; animation: joey-stage-in-kf 0.5s ease-out forwards; }
.joey-stage-thinking { position: absolute; inset: 0; animation: joey-fade-out-kf 0.4s ease-out forwards; pointer-events: none; display: none; }

.joey-workflow-wrap { position: relative; }
.joey-workflow-wrap > .joey-workflow-real { display: none; }
.joey-workflow-wrap.joey-pause-done > .joey-workflow-real { display: block; }
.joey-workflow-pause {
  z-index: 5;
  animation: joey-fade-out-kf 0.4s ease-out 2.5s forwards;
  pointer-events: none;
}
.joey-workflow-wrap.joey-pause-done > .joey-workflow-pause { display: none; }

#workflow.joey-fast .joey-stage-real { animation-delay: 0s !important; }
#workflow.joey-fast .joey-workflow-pause { display: none !important; }

@keyframes joey-toast-in-kf {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
#toast > div {
  animation: joey-toast-in-kf 0.3s ease-out forwards;
}

body {
  background: #f8fafc;
  color: #0f172a;
  background-image:
    radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.04) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(14, 165, 233, 0.04) 0px, transparent 50%);
}

.keith-map {
  height: 480px;
  width: 100%;
  border-radius: 0.75rem;
  overflow: hidden;
  background: #e2e8f0;
}
.keith-map .leaflet-control-attribution {
  font-size: 9px;
  background: rgba(255,255,255,0.7);
}
.keith-pin {
  width: 18px;
  height: 18px;
  border-radius: 9999px;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(15, 23, 42, 0.15), 0 4px 10px rgba(15, 23, 42, 0.18);
}
.keith-pin-dublin { background: #16a34a; }
.keith-pin-cork { background: #f59e0b; }
.keith-pin-halo {
  position: absolute;
  inset: -10px;
  border-radius: 9999px;
  opacity: 0.35;
  animation: joey-pin-pulse-kf 2s ease-in-out infinite;
}
.keith-pin-halo-dublin { background: #16a34a; }
.keith-pin-halo-cork { background: #f59e0b; animation-delay: 0.5s; }
.keith-pin-wrap { position: relative; width: 18px; height: 18px; }

.keith-label {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 5px 10px;
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08);
}
.keith-label .keith-label-name { font-size: 14px; font-weight: 700; }
.keith-label .keith-label-emoji { margin: 0 5px; }
.keith-label .keith-label-price { color: #475569; font-weight: 500; }
.keith-label .keith-label-arrow {
  margin-left: 6px;
  font-size: 13px;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 4px;
  line-height: 1;
}
.keith-label .keith-label-arrow-up { color: #047857; background: #d1fae5; }
.keith-label .keith-label-arrow-down { color: #b91c1c; background: #fee2e2; }

.keith-arrow-label {
  background: #0f172a;
  color: white;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 9px;
  border-radius: 9999px;
  white-space: nowrap;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.25);
}

.leaflet-div-icon { background: transparent !important; border: none !important; }

.keith-store {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  border: 1.5px solid white;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.25);
  cursor: default;
}
.keith-store-warn { background: #16a34a; }
.keith-store-risk { background: #f59e0b; }
.keith-store-neutral { background: #94a3b8; }

.keith-lorry {
  font-size: 18px;
  line-height: 1;
  filter: drop-shadow(0 4px 6px rgba(15, 23, 42, 0.3));
  transform: translateY(-2px);
  pointer-events: none;
}

@keyframes joey-counter-bump-kf {
  0% { transform: scale(1); color: #0f172a; }
  30% { transform: scale(1.25); color: #059669; }
  100% { transform: scale(1); color: #0f172a; }
}
.joey-counter-bump {
  animation: joey-counter-bump-kf 0.6s ease-out;
  display: inline-block;
}
"""

DISMISS_TOAST_SCRIPT = """
document.body.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target.id === 'toast' && e.detail.target.children.length > 0) {
    setTimeout(() => {
      htmx.ajax('GET', '/toast/clear', { target: '#toast', swap: 'outerHTML' });
    }, 4000);
  }
});
"""

WORKFLOW_PAUSE_SCRIPT = """
function joeyArmWorkflowPause() {
  const wf = document.getElementById('workflow');
  if (!wf) return;
  if (wf.classList.contains('joey-fast') || !wf.classList.contains('joey-workflow-wrap')) return;
  if (wf.dataset.joeyPauseArmed === '1') return;
  wf.dataset.joeyPauseArmed = '1';
  setTimeout(() => {
    wf.classList.add('joey-pause-done');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    requestAnimationFrame(() => {
      window.dispatchEvent(new Event('resize'));
      (window.__joeyMaps || []).forEach((m) => { try { m.invalidateSize(); } catch (e) {} });
    });
  }, 2500);
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', joeyArmWorkflowPause);
} else {
  joeyArmWorkflowPause();
}
document.addEventListener('htmx:afterSwap', () => joeyArmWorkflowPause());
"""


app, rt = fast_app(
    pico=False,
    title="IDM — Retail Planning Assistant",
    hdrs=(
        Script(src="https://cdn.tailwindcss.com"),
        Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
        ),
        Link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            crossorigin="",
        ),
        Script(
            src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=",
            crossorigin="",
        ),
        Style("html { font-size: 120%; } html, body { font-family: 'Inter', sans-serif; }"),
        Style(HEAD_STYLES),
        Script(DISMISS_TOAST_SCRIPT),
        Script(WORKFLOW_PAUSE_SCRIPT),
    ),
)


def toast_node() -> Div:
    if state["toast"]:
        return Div(
            Div(
                Div(
                    Span("✓", cls="text-emerald-400 text-lg font-bold"),
                    cls="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center shrink-0",
                ),
                Div(
                    Span("Plan approved", cls="text-sm font-semibold text-white block"),
                    Span(state["toast"], cls="text-xs text-slate-300 block"),
                ),
                cls="flex items-center gap-3 bg-slate-900 px-4 py-3 rounded-xl shadow-2xl border border-slate-700 min-w-[320px]",
            ),
            cls="fixed bottom-6 right-6 z-50",
            id="toast",
        )
    return Div(id="toast")


@rt("/")
async def index(fast: int | None = None):
    scenario = await get_scenario()
    fast_mode = bool(fast)
    return Div(
        sidebar(),
        Div(
            app_topbar(scenario["monitoring_label"]),
            Main(
                Div(
                    Div(
                        Span(
                            "Insight detected",
                            cls="text-[10px] uppercase tracking-wider text-emerald-600 font-semibold",
                        ),
                        Span(
                            scenario["greeting"],
                            cls="text-2xl font-bold text-slate-900 block mt-1",
                        ),
                        Span(
                            scenario["subgreeting"],
                            cls="text-sm text-slate-500 block",
                        ),
                    ),
                    Div(
                        Div(
                            Span(
                                cls="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block joey-pulse"
                            ),
                            Span(
                                "4,812 SKUs · 142 stores",
                                cls="text-xs text-slate-600 ml-2",
                            ),
                            cls="flex items-center px-3 py-1.5 bg-white border border-slate-200 rounded-md",
                        ),
                        cls="flex items-center gap-3",
                    ),
                    cls="flex items-end justify-between mb-6",
                ),
                workflow(scenario, state["selected_id"], state["approved"], fast=fast_mode, actions=state["actions"]),
                cls="px-8 py-6 max-w-[1400px] mx-auto",
            ),
            why_drawer_closed(),
            toast_node(),
            cls="ml-52 min-h-screen",
        ),
        cls="bg-slate-50 min-h-screen",
    )


@rt("/select/{insight_id}")
async def select(insight_id: str):
    scenario = await get_scenario()
    state["selected_id"] = insight_id
    state["approved"] = False
    reset_actions()
    return workflow(scenario, state["selected_id"], state["approved"], fast=True, actions=state["actions"])


@rt("/action/{idx}/{decision}", methods=["POST"])
async def action(idx: int, decision: str):
    scenario = await get_scenario()
    if decision in {"approved", "escalated", "rejected", "pending"} and idx in state["actions"]:
        state["actions"][idx] = decision
    if all(v == "approved" for v in state["actions"].values()):
        state["approved"] = True
    return workflow(scenario, state["selected_id"], state["approved"], fast=True, actions=state["actions"])


@rt("/approve", methods=["POST"])
async def approve():
    scenario = await get_scenario()
    res = await approve_insight(state["selected_id"])
    state["approved"] = True
    for k in state["actions"]:
        if state["actions"][k] == "pending":
            state["actions"][k] = "approved"
    state["toast"] = res["message"]
    flow = workflow(scenario, state["selected_id"], state["approved"], fast=True, actions=state["actions"])
    return flow, Div(
        Div(
            Div(
                Span("✓", cls="text-emerald-400 text-lg font-bold"),
                cls="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center shrink-0",
            ),
            Div(
                Span("Plan approved", cls="text-sm font-semibold text-white block"),
                Span(res["message"], cls="text-xs text-slate-300 block"),
            ),
            cls="flex items-center gap-3 bg-slate-900 px-4 py-3 rounded-xl shadow-2xl border border-slate-700 min-w-[320px]",
        ),
        cls="fixed bottom-6 right-6 z-50",
        id="toast",
        hx_swap_oob="true",
    )


@rt("/toast/clear")
async def toast_clear():
    state["toast"] = None
    return Div(id="toast")


@rt("/why")
async def why(expand: int | None = None):
    scenario = await get_scenario()
    return why_drawer_open(scenario["bbq"]["why"], expand)


@rt("/why/close")
async def why_close():
    return why_drawer_closed()


if __name__ == "__main__":
    serve(host="0.0.0.0", port=3000)
