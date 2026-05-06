from fasthtml.common import Div, Span


def forecast_strip(forecast: list[dict]) -> Div:
    children = [Div()]
    for f in forecast:
        children.append(Div(f["day"], cls="text-center font-medium text-neutral-500"))

    children.append(Div("DUB", cls="text-xs font-medium text-neutral-400 self-center"))
    for f in forecast:
        children.append(
            Div(
                Span(f["dublin"]["emoji"], cls="text-base"),
                Span(f"{f['dublin']['temp_c']}°", cls="ml-1 text-neutral-700"),
                cls="text-center bg-green-50 rounded-lg py-1",
            )
        )

    children.append(Div("COR", cls="text-xs font-medium text-neutral-400 self-center"))
    for f in forecast:
        children.append(
            Div(
                Span(f["cork"]["emoji"], cls="text-base"),
                Span(f"{f['cork']['temp_c']}°", cls="ml-1 text-neutral-700"),
                cls="text-center bg-amber-50 rounded-lg py-1",
            )
        )

    return Div(
        Div(
            *children,
            cls="grid grid-cols-[auto_repeat(3,1fr)] gap-x-3 gap-y-1 text-sm",
        ),
        cls="mt-4",
    )
