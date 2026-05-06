from fasthtml.common import NotStr


def mini_bar_chart(bars: list[dict]) -> NotStr:
    max_val = max(v for b in bars for v in (b["dublin"], b["cork"]))
    w, h = 280, 120
    pad_top, pad_bottom, pad_left, pad_right = 10, 24, 10, 10
    plot_h = h - pad_top - pad_bottom
    group_w = (w - pad_left - pad_right) / len(bars)
    bar_w = group_w * 0.3

    rects = []
    for i, b in enumerate(bars):
        gx = pad_left + i * group_w + group_w * 0.15
        d_h = (b["dublin"] / max_val) * plot_h * 0.9
        c_h = (b["cork"] / max_val) * plot_h * 0.9
        rects.append(
            f'<g>'
            f'<rect x="{gx}" y="{pad_top + plot_h - d_h}" width="{bar_w}" height="{d_h}" rx="2" fill="#16a34a" opacity="0.85" />'
            f'<rect x="{gx + bar_w + 2}" y="{pad_top + plot_h - c_h}" width="{bar_w}" height="{c_h}" rx="2" fill="#f59e0b" opacity="0.85" />'
            f'<text x="{gx + bar_w}" y="{h - 6}" text-anchor="middle" class="text-[10px] fill-neutral-500">{b["label"]}</text>'
            f'</g>'
        )

    svg = (
        f'<svg viewBox="0 0 {w} {h}" class="w-full max-w-[280px]">'
        + "".join(rects)
        + "</svg>"
    )
    return NotStr(svg)


def mini_line_chart(points: list[int]) -> NotStr:
    w, h = 280, 80
    pad_top, pad_bottom, pad_left, pad_right = 12, 12, 16, 16
    plot_w = w - pad_left - pad_right
    plot_h = h - pad_top - pad_bottom
    mn = min(points) - 5
    mx = max(points) + 5

    coords = [
        (
            pad_left + (i / (len(points) - 1)) * plot_w,
            pad_top + plot_h - ((p - mn) / (mx - mn)) * plot_h,
        )
        for i, p in enumerate(points)
    ]

    polyline = " ".join(f"{x},{y}" for x, y in coords)
    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="3.5" fill="#16a34a" />' for x, y in coords
    )
    labels = "".join(
        f'<text x="{x}" y="{y - 8}" text-anchor="middle" class="text-[10px] fill-neutral-600">{points[i]}%</text>'
        for i, (x, y) in enumerate(coords)
    )

    svg = (
        f'<svg viewBox="0 0 {w} {h}" class="w-full max-w-[280px]">'
        f'<polyline points="{polyline}" fill="none" stroke="#16a34a" stroke-width="2" stroke-linejoin="round" />'
        f'{circles}{labels}'
        f'</svg>'
    )
    return NotStr(svg)
