"""Generate the profile banner (dark and light SVG).

The graph on the right is a small synthetic network with three communities.
Node size is the node's PageRank, and the moving dot is a random surfer
walking along the edges.

Run:  python3 assets/make_banner.py
"""

import math
import random
from pathlib import Path

W, H = 1280, 320
OUT = Path(__file__).parent
SEED = 11

THEMES = {
    "dark": {
        "bg0": "#0b1020", "bg1": "#151b34",
        "title": "#f3f4f8", "sub": "#a9b1d6", "mono": "#7dd3fc",
        "edge": "#3b4472", "walker": "#fde68a",
        "groups": ["#a78bfa", "#2dd4bf", "#fb923c"],
    },
    "light": {
        "bg0": "#f8fafc", "bg1": "#eef2ff",
        "title": "#111827", "sub": "#4b5563", "mono": "#0369a1",
        "edge": "#c7cde3", "walker": "#d97706",
        "groups": ["#7c3aed", "#0d9488", "#ea580c"],
    },
}

TAGLINE = "NLP  ·  Information Retrieval  ·  Network Science"
LINES = [
    "text   →  tokens    →  vectors",
    "query  →  retrieve  →  rank",
    "graph  →  communities  →  influence",
]


def build_graph(rng):
    centers = [(790, 120, 0), (1010, 95, 1), (960, 235, 2), (1170, 205, 1)]
    sizes = [8, 7, 8, 5]
    nodes = []  # (x, y, group)
    for (cx, cy, g), n in zip(centers, sizes):
        placed = 0
        while placed < n:
            x = rng.gauss(cx, 55)
            y = rng.gauss(cy, 38)
            if not (660 < x < 1240 and 28 < y < 292):
                continue
            if any(math.hypot(x - a, y - b) < 34 for a, b, _ in nodes):
                continue
            nodes.append((x, y, g))
            placed += 1

    edges = set()
    for i, (x, y, g) in enumerate(nodes):
        same = sorted(
            (math.hypot(x - a, y - b), j)
            for j, (a, b, h) in enumerate(nodes)
            if j != i and h == g
        )
        for _, j in same[:2]:
            edges.add((i, j) if rng.random() < 0.5 else (j, i))
    # a few bridges between communities
    for _ in range(5):
        i, j = rng.sample(range(len(nodes)), 2)
        if nodes[i][2] != nodes[j][2]:
            edges.add((i, j))
    return nodes, sorted(edges)


def pagerank(n, edges, alpha=0.15, iters=100):
    out = [[] for _ in range(n)]
    for i, j in edges:
        out[i].append(j)
    pr = [1 / n] * n
    for _ in range(iters):
        new = [alpha / n] * n
        for i in range(n):
            targets = out[i] or range(n)  # dangling node: spread evenly
            share = (1 - alpha) * pr[i] / len(targets)
            for j in targets:
                new[j] += share
        pr = new
    return pr


def random_walk(rng, n, edges, steps=14):
    nbrs = [set() for _ in range(n)]
    for i, j in edges:
        nbrs[i].add(j)
        nbrs[j].add(i)
    cur = max(range(n), key=lambda k: len(nbrs[k]))
    path = [cur]
    for _ in range(steps):
        options = sorted(nbrs[cur] - {path[-2]} if len(path) > 1 else nbrs[cur])
        cur = rng.choice(options or sorted(nbrs[cur]))
        path.append(cur)
    return path


def svg(theme, nodes, edges, pr, walk):
    t = THEMES[theme]
    lo, hi = min(pr), max(pr)
    radius = [5 + 11 * (p - lo) / (hi - lo) for p in pr]
    top = max(range(len(pr)), key=pr.__getitem__)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Faezeh Mozaffari. {TAGLINE}">',
        "<defs>",
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg0"]}"/>'
        f'<stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>',
        f'<marker id="arrow" viewBox="0 0 6 6" refX="5" refY="3" '
        f'markerWidth="5" markerHeight="5" orient="auto">'
        f'<path d="M0,0 L6,3 L0,6 z" fill="{t["edge"]}"/></marker>',
        "</defs>",
        "<style>",
        ".title{font:700 52px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}",
        ".sub{font:500 21px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}",
        ".mono{font:500 18px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
        "white-space:pre}",
        ".cycle{opacity:0;animation:cycle 9s infinite}",
        ".c1{animation-delay:3s}.c2{animation-delay:6s}",
        "@keyframes cycle{0%{opacity:0}4%{opacity:1}30%{opacity:1}"
        "34%{opacity:0}100%{opacity:0}}",
        ".node{transform-box:fill-box;transform-origin:center;"
        "animation:pulse 4s ease-in-out infinite}",
        "@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}",
        "@media (prefers-reduced-motion:reduce){.cycle,.node{animation:none}"
        ".c0{opacity:1}.walker{display:none}}",
        "</style>",
        f'<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>',
        f'<text x="64" y="138" class="title" fill="{t["title"]}">Faezeh Mozaffari</text>',
        f'<text x="66" y="180" class="sub" fill="{t["sub"]}">{TAGLINE}</text>',
    ]
    for k, line in enumerate(LINES):
        parts.append(
            f'<text x="66" y="236" class="mono cycle c{k}" fill="{t["mono"]}">'
            f"›  {line}</text>"
        )

    # edges, shortened so the arrow head stops at the node border
    for i, j in edges:
        (x1, y1, _), (x2, y2, _) = nodes[i], nodes[j]
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        sx, sy = x1 + ux * radius[i], y1 + uy * radius[i]
        ex, ey = x2 - ux * (radius[j] + 3), y2 - uy * (radius[j] + 3)
        parts.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{t["edge"]}" stroke-width="1.4" marker-end="url(#arrow)"/>'
        )

    for k, ((x, y, g), r) in enumerate(zip(nodes, radius)):
        color = t["groups"][g]
        delay = (k * 0.37) % 4
        parts.append(
            f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" '
            f'fill="{color}" fill-opacity="0.9" style="animation-delay:{delay:.2f}s"/>'
        )
        if k == top:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 6:.1f}" fill="none" '
                f'stroke="{color}" stroke-width="1.5" stroke-dasharray="3 4"/>'
            )

    path = " ".join(
        f'{"M" if n == 0 else "L"}{nodes[v][0]:.1f},{nodes[v][1]:.1f}'
        for n, v in enumerate(walk)
    )
    parts.append(
        f'<circle class="walker" r="4.5" fill="{t["walker"]}">'
        f'<animateMotion dur="14s" repeatCount="indefinite" path="{path}"/></circle>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    rng = random.Random(SEED)
    nodes, edges = build_graph(rng)
    pr = pagerank(len(nodes), edges)
    walk = random_walk(rng, len(nodes), edges)
    for theme in THEMES:
        (OUT / f"banner-{theme}.svg").write_text(svg(theme, nodes, edges, pr, walk))
    print(f"{len(nodes)} nodes, {len(edges)} edges -> banner-dark.svg, banner-light.svg")


if __name__ == "__main__":
    main()
