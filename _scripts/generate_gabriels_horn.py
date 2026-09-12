"""Generate the deterministic SVG used by the Gabriel's horn post.

The horn is the surface of revolution r = 1/x, x >= 1.  The drawing uses a
finite window only for display; the annotations show the limiting integrals.
"""
from math import cos, log, pi, sin
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets/images/20260912-gabriels-horn.svg"
W, H = 1200, 680
BLUE = "#0969da"
INK = "#24292f"
MUTED = "#57606a"
GRID = "#d0d7de"
PALE = "#ddf4ff"
ORANGE = "#bf8700"


def esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, value, size=16, fill=INK, weight="400", anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(value)}</text>'


def path(points, stroke, width=1.5, fill="none", opacity=1):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" stroke-linejoin="round"/>'


svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
    '<title id="title">Gabriel’s horn: a 1/x surface with finite volume and infinite area</title>',
    '<desc id="desc">A blue wireframe horn narrows as x increases. A companion cutoff chart shows the volume approaching pi while the surface area keeps growing like 2 pi log R.</desc>',
    '<rect width="1200" height="680" fill="white"/>',
    '<rect x="24" y="24" width="1152" height="632" rx="12" fill="white" stroke="#d8dee4"/>',
    text(56, 68, "Gabriel's horn", 25, INK, "700"),
    text(56, 94, "The surface of revolution r = 1/x, shown only over a finite viewing window", 15, MUTED),
    '<line x1="56" y1="114" x2="1144" y2="114" stroke="#d8dee4"/>',
    '<rect x="56" y="140" width="570" height="470" rx="8" fill="#f6f8fa"/>',
    '<rect x="650" y="140" width="494" height="470" rx="8" fill="#f6f8fa"/>',
    text(80, 176, "The horn", 18, INK, "700"),
    text(674, 176, "What changes as the cutoff R moves right?", 18, INK, "700"),
]

# Left panel: a clean perspective rendering of the surface as a blue shaded strip.
left, right, base, scale = 100, 574, 390, 390
xs = [1 + 7 * i / 80 for i in range(81)]
def project(x, radius, theta):
    # A deliberately simple oblique projection: x is the axis, y is vertical,
    # and the circular cross-section is flattened to make the surface legible.
    px = left + (x - 1) / 7 * (right - left)
    py = base - radius * scale * (0.58 * sin(theta) + 0.16 * cos(theta))
    return px, py

# A subtle filled surface silhouette emphasizes that this is a surface, not a 2D graph.
top = [project(x, 1 / x, pi / 2)[0:2] for x in xs]
bottom = [project(x, 1 / x, 3 * pi / 2)[0:2] for x in reversed(xs)]
svg.append(path(top + bottom + [top[0]], BLUE, 1, PALE, 0.78))
# Rings and generators make the 3D surface explicit.
for i, x in enumerate(xs[::5]):
    r = 1 / x
    ring = [project(x, r, 2 * pi * j / 32) for j in range(33)]
    svg.append(path(ring, BLUE, 1.1, "none", 0.52 if i % 2 else 0.72))
for theta in [0, pi / 4, pi / 2, 3 * pi / 4, pi, 5 * pi / 4, 3 * pi / 2, 7 * pi / 4]:
    svg.append(path([project(x, 1 / x, theta) for x in xs], BLUE, 1.2, "none", 0.68))
# Axis and annotations.
svg += [
    '<line x1="100" y1="390" x2="574" y2="390" stroke="#8c959f" stroke-width="1.2"/>',
    '<line x1="100" y1="390" x2="100" y2="228" stroke="#8c959f" stroke-width="1.2"/>',
    text(100, 421, "x = 1", 13, MUTED), text(555, 421, "x = 8", 13, MUTED, anchor="end"),
    text(338, 452, "radius shrinks as 1/x", 15, BLUE, "700", "middle"),
    text(338, 478, "rings continue getting thinner", 14, MUTED, "400", "middle"),
    '<circle cx="132" cy="246" r="4" fill="#0969da"/>',
    text(145, 249, "wide mouth", 13, MUTED),
    '<circle cx="542" cy="374" r="4" fill="#0969da"/>',
    text(530, 366, "narrow tail", 13, MUTED, "400", "end"),
    text(80, 550, "A finite picture cannot display the whole infinite horn.", 14, MUTED),
    text(80, 574, "It shows the rule, not a physical object at infinity.", 14, MUTED),
]

# Right panel: normalized comparison of exact cutoff formulae.
plot_x, plot_y, plot_w, plot_h = 704, 224, 406, 270
svg += [
    f'<line x1="{plot_x}" y1="{plot_y + plot_h}" x2="{plot_x + plot_w}" y2="{plot_y + plot_h}" stroke="{GRID}"/>',
    f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" y2="{plot_y + plot_h}" stroke="{GRID}"/>',
    text(plot_x - 10, plot_y + 5, "scaled", 12, MUTED, anchor="end"),
]
for frac in [0, .25, .5, .75, 1]:
    y = plot_y + plot_h * (1 - frac)
    svg.append(f'<line x1="{plot_x}" y1="{y:.1f}" x2="{plot_x + plot_w}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="2 5"/>')
    svg.append(text(plot_x - 10, y + 4, f"{frac:.2f}", 11, MUTED, anchor="end"))

cutoffs = [2, 4, 8, 16, 32]
# Volume fraction V_R / pi = 1 - 1/R; area is shown against its value at R=32
vol = [1 - 1 / r for r in cutoffs]
area = [log(r) / log(32) for r in cutoffs]
def chart_points(values):
    return [(plot_x + i * plot_w / (len(values) - 1), plot_y + plot_h * (1 - v)) for i, v in enumerate(values)]
svg.append(path(chart_points(vol), BLUE, 3))
svg.append(path(chart_points(area), ORANGE, 3))
for points, color in [(chart_points(vol), BLUE), (chart_points(area), ORANGE)]:
    for x, y in points:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="white" stroke="{color}" stroke-width="2.5"/>')
for i, r in enumerate(cutoffs):
    svg.append(text(plot_x + i * plot_w / 4, plot_y + plot_h + 25, f"{r}", 12, MUTED, anchor="middle"))
svg += [
    text(plot_x + plot_w / 2, plot_y + plot_h + 48, "cutoff R", 12, MUTED, anchor="middle"),
    text(674, 206, "cutoff values", 12, MUTED),
    f'<line x1="1000" y1="201" x2="1024" y2="201" stroke="{BLUE}" stroke-width="3"/>',
    text(1032, 206, "volume / π", 12, BLUE),
    f'<line x1="1000" y1="221" x2="1024" y2="221" stroke="{ORANGE}" stroke-width="3"/>',
    text(1032, 226, "area / area at 32", 12, ORANGE),
    text(674, 548, "V(R) = π(1 − 1/R)  →  π", 16, BLUE, "700"),
    text(674, 574, "A(R) = 2π log R  →  ∞", 16, ORANGE, "700"),
    text(674, 596, "The comparison is mathematical, not physical.", 13, MUTED),
]
svg.append('</svg>')
OUT.write_text("\n".join(svg) + "\n", encoding="utf-8")
print(f"wrote {OUT}")
