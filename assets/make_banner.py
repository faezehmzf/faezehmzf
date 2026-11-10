"""Build the animated profile banner (assets/banner.webp).

A synthetic social network is generated and laid out: communities grow by
preferential attachment, so each has a few hubs, and bridges join neighbouring
communities. Information cascades start from random accounts and spread along
edges, across communities, while the rest of the network stays dim. All motion
repeats every LOOP seconds, so the WebP loops without a jump.

Run:  python3 assets/make_banner.py            (writes assets/banner.webp)
      python3 assets/make_banner.py --frames-only 0 100   (PNG stills for checking)
Needs Pillow (with WebP) and NumPy; the font is macOS's SFNS.ttf (SF Pro).
"""
import argparse
import colorsys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).parent / "banner.webp"
W, H = 1280, 400
SS = 2                      # supersampling factor for smooth lines
FPS, LOOP = 25, 8.0
N_FRAMES = int(FPS * LOOP)
SEED = 7
RADIUS = 18                 # rounded corners

NAME = "Faezeh Mozaffari"
TAGLINE = "Network Science  ·  Graph ML  ·  Information Diffusion"
FONT = "/System/Library/Fonts/SFNS.ttf"
TEXT_X = 742                # left edge of the text block

BG_TOP, BG_BOTTOM = np.array([5, 9, 24]), np.array([10, 16, 40])
PALETTE = [(45, 212, 191), (56, 189, 248), (129, 140, 248), (167, 139, 250),
           (244, 114, 182), (251, 191, 36), (52, 211, 153), (96, 165, 250),
           (232, 121, 249), (45, 212, 191), (56, 189, 248), (129, 140, 248),
           (52, 211, 153), (244, 114, 182)]

rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------- network
def build_graph():
    """Communities placed over the banner; denser on the left, lighter under the text."""
    centres = [(85, 95), (95, 300), (230, 195), (335, 65), (370, 320), (480, 185),
               (585, 55), (625, 305), (700, 50), (800, 355), (905, 55), (1075, 350),
               (1200, 95), (1235, 260)]
    sizes = [70, 65, 85, 60, 65, 85, 55, 65, 40, 38, 36, 36, 42, 30]
    pos, comm, edges = [], [], []
    for c, ((cx, cy), n) in enumerate(zip(centres, sizes)):
        base = len(pos)
        spread = 10 + 2.6 * np.sqrt(n)
        for i in range(n):
            pos.append((cx + rng.standard_t(3) * spread, cy + rng.standard_t(3) * spread * 0.75))
            comm.append(c)
            if i == 0:
                continue
            # preferential attachment inside the community -> hubs
            deg = np.bincount(np.array([e for ed in edges for e in ed if e >= base], int) - base,
                              minlength=i)[:i] + 1.0
            m = min(i, 2 if rng.random() < 0.7 else 3)
            for t in rng.choice(i, size=m, replace=False, p=deg / deg.sum()):
                edges.append((base + i, base + int(t)))
    pos, comm = np.array(pos, float), np.array(comm)
    # bridges between nearby communities
    cen = np.array(centres, float)
    for a in range(len(centres)):
        d = np.hypot(*(cen - cen[a]).T)
        for b in np.argsort(d)[1:4]:
            if b < a and d[b] < 330:
                continue
            for _ in range(rng.integers(2, 5)):
                u = rng.choice(np.flatnonzero(comm == a)); v = rng.choice(np.flatnonzero(comm == b))
                edges.append((int(u), int(v)))
    edges = sorted({tuple(sorted(e)) for e in edges if e[0] != e[1]})
    pos = relax(pos, np.array(edges), comm)
    return pos, comm, np.array(edges)


def relax(pos, edges, comm, iters=160):
    """A short force-directed pass: springs on edges, repulsion between nodes."""
    anchor = pos.copy()
    for it in range(iters):
        step = 1.2 * (1 - it / iters) + 0.1
        d = pos[:, None, :] - pos[None, :, :]
        dist2 = (d ** 2).sum(-1) + 1e-3
        near = (dist2 < 30 ** 2)[..., None]          # push only close neighbours apart
        rep = np.clip((d / dist2[..., None] * near * 9.0).sum(1), -3, 3)
        spring = np.zeros_like(pos)
        delta = pos[edges[:, 1]] - pos[edges[:, 0]]
        length = np.linalg.norm(delta, axis=1, keepdims=True) + 1e-6
        same = (comm[edges[:, 0]] == comm[edges[:, 1]])[:, None]
        rest = np.where(same, 24.0, length)          # bridges keep their length
        f = delta / length * (length - rest) * 0.05
        np.add.at(spring, edges[:, 0], f)
        np.add.at(spring, edges[:, 1], -f)
        pos = pos + step * (rep + spring + 0.04 * (anchor - pos))
    pos[:, 0] = np.clip(pos[:, 0], 14, W - 14)
    pos[:, 1] = np.clip(pos[:, 1], 14, H - 14)
    return pos


# ---------------------------------------------------------------- cascades
def plan_cascades(n, edges, comm, count=16):
    """Independent-cascade spreads: (start time, list of (u, v, depth))."""
    nbrs = [[] for _ in range(n)]
    for u, v in edges:
        nbrs[u].append(v); nbrs[v].append(u)
    deg = np.array([len(x) for x in nbrs], float)
    out = []
    for k in range(count):
        seed = int(rng.choice(n, p=deg / deg.sum()))
        seen, frontier, steps = {seed}, [seed], []
        for depth in range(6):
            nxt = []
            for u in frontier:
                for v in nbrs[u]:
                    if v not in seen and rng.random() < 0.55:
                        seen.add(v); nxt.append(v); steps.append((u, v, depth))
            frontier = nxt[:14]
            if not frontier or len(steps) > 55:
                break
        out.append((k * LOOP / count + rng.uniform(0, 0.3), seed, steps))
    return out


# ---------------------------------------------------------------- drawing
def background():
    y = np.linspace(0, 1, H)[:, None, None]
    img = BG_TOP * (1 - y) + BG_BOTTOM * y
    img = np.repeat(img, W, axis=1)
    yy, xx = np.mgrid[0:H, 0:W]
    for cx, cy, r, col, a in [(300, 200, 420, (40, 70, 160), 0.28), (980, 220, 380, (90, 50, 160), 0.18)]:
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r / 2.5))
        img += g[..., None] * np.array(col) * a
    # faint dot grid
    grid = ((xx % 32 == 0) & (yy % 32 == 0))
    img[grid] += 14
    return img


def text_shade():
    """Darken the right side so the name stays readable over the network."""
    xx = np.linspace(0, 1, W)[None, :]
    yy = np.linspace(-1, 1, H)[:, None]
    s = np.clip((xx - 0.52) / 0.12, 0, 1) * np.clip(1.25 - 0.55 * yy ** 2, 0, 1)
    return 1 - 0.55 * s[..., None]


def node_radius(deg):
    return 1.1 + 0.55 * np.sqrt(deg)


def static_layer(pos, comm, edges, deg):
    """Edges and dim nodes, drawn once."""
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    p = pos * SS
    for u, v in edges:
        cu, cv = PALETTE[comm[u]], PALETTE[comm[v]]
        same = comm[u] == comm[v]
        col = cu if same else tuple((np.array(cu) + np.array(cv)) // 2)
        d.line([tuple(p[u]), tuple(p[v])], fill=col + ((62,) if same else (34,)), width=SS)
    for i in np.argsort(deg):
        r = node_radius(deg[i]) * SS
        col = PALETTE[comm[i]]
        x, y = p[i]
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (200,))
    return big.resize((W, H), Image.LANCZOS)


def text_layer():
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    name = ImageFont.truetype(FONT, 58); name.set_variation_by_axes([100, 58, 400, 700])
    tag = ImageFont.truetype(FONT, 17); tag.set_variation_by_axes([100, 17, 400, 500])
    kick = ImageFont.truetype(FONT, 13); kick.set_variation_by_axes([100, 13, 400, 600])
    d.text((TEXT_X, 152), "SOCIAL NETWORK ANALYSIS  ·  GRAPH LEARNING", font=kick,
           fill=(94, 234, 212, 235), anchor="ls")
    d.text((TEXT_X - 3, 222), NAME, font=name, fill=(243, 244, 248, 255), anchor="ls")
    d.text((TEXT_X, 276), TAGLINE, font=tag,
           fill=(170, 186, 218, 255), anchor="ls")
    return layer


def lighten(col, k):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in col))
    return tuple(int(c * 255) for c in colorsys.hls_to_rgb(h, min(1, l + k), s))


def dynamic_layer(t, pos, comm, deg, cascades, twinkle):
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    p = pos * SS
    hop = 0.32                                   # seconds per hop
    for start, seed, steps in cascades:
        tau = (t - start) % LOOP
        col = lighten(PALETTE[comm[seed]], 0.18)
        life = 6 * hop + 1.6
        if tau > life:
            continue
        fade = 1.0 if tau < life - 0.8 else (life - tau) / 0.8
        # seed ring
        ring = tau / 1.2
        if ring < 1:
            r = (4 + 22 * ring) * SS
            x, y = p[seed]
            d.ellipse([x - r, y - r, x + r, y + r], outline=col + (int(200 * (1 - ring)),), width=SS)
        lit = {seed: tau}
        for u, v, depth in steps:
            s0 = depth * hop
            prog = (tau - s0) / hop
            if prog <= 0:
                continue
            a, b = p[u], p[v]
            e = a + (b - a) * min(prog, 1)
            d.line([tuple(a), tuple(e)], fill=col + (int(150 * fade),), width=int(1.4 * SS))
            if prog < 1:
                r = 2.6 * SS
                d.ellipse([e[0] - r, e[1] - r, e[0] + r, e[1] + r], fill=(255, 255, 255, 255))
            else:
                lit[v] = tau - s0 - hop
        for i, age in lit.items():
            glow = max(0.2, 0.6 * np.exp(-age / 0.6)) * fade
            r = (node_radius(deg[i]) + 0.4 + 2.2 * np.exp(-age / 0.35)) * SS
            x, y = p[i]
            c = tuple(int(255 * glow + ch * (1 - glow)) for ch in col)
            d.ellipse([x - r, y - r, x + r, y + r], fill=c + (int(255 * min(1, glow + 0.45)),))
    # twinkling hubs
    for i, phase in twinkle:
        k = 0.5 + 0.5 * np.sin(2 * np.pi * (t / LOOP * 2) + phase)
        r = (node_radius(deg[i]) + 0.6) * SS
        x, y = p[i]
        c = lighten(PALETTE[comm[i]], 0.25)
        d.ellipse([x - r, y - r, x + r, y + r], fill=c + (int(220 * k),))
    return big.resize((W, H), Image.LANCZOS)


def rounded_mask():
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), RADIUS, fill=255)
    return m


def to_float(im):
    a = np.asarray(im).astype(float) / 255
    return a[..., :3], a[..., 3:4]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frames-only", type=int, nargs="*", help="save these frame numbers as PNG")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    pos, comm, edges = build_graph()
    deg = np.bincount(edges.ravel(), minlength=len(pos))
    cascades = plan_cascades(len(pos), edges, comm)
    hubs = np.argsort(deg)[-40:]
    twinkle = [(int(i), rng.uniform(0, 2 * np.pi)) for i in hubs]
    print(f"{len(pos)} nodes, {len(edges)} edges, {len(cascades)} cascades")

    bg = background() / 255
    stat_rgb, stat_a = to_float(static_layer(pos, comm, edges, deg))
    stat_glow = to_float(Image.fromarray((np.dstack([stat_rgb * stat_a, stat_a]) * 255).astype(np.uint8))
                         .filter(ImageFilter.GaussianBlur(5)))[0]
    base = bg * (1 - stat_a) + stat_rgb * stat_a + 0.6 * stat_glow
    shade = text_shade()
    txt_rgb, txt_a = to_float(text_layer())
    mask = rounded_mask()

    frames = []
    wanted = range(N_FRAMES) if args.frames_only is None else args.frames_only
    for f in wanted:
        t = f / FPS
        dyn = dynamic_layer(t, pos, comm, deg, cascades, twinkle)
        d_rgb, d_a = to_float(dyn)
        glow = to_float(dyn.filter(ImageFilter.GaussianBlur(6)))
        img = base + d_rgb * d_a + 0.9 * glow[0] * glow[1]
        img = img * shade
        img = img * (1 - txt_a) + txt_rgb * txt_a
        im = Image.fromarray((np.clip(img, 0, 1) * 255).round().astype(np.uint8))
        im = im.convert("RGBA"); im.putalpha(mask)
        if args.frames_only is not None:
            im.save(args.out.parent / f"frame_{f:03d}.png")
        frames.append(im)
    if args.frames_only is None:
        frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=round(1000 / FPS),
                       loop=0, quality=80, method=6, minimize_size=True)
        print(f"{len(frames)} frames -> {args.out} ({args.out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
