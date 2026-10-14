"""Builds the SVG graphics for the FastPatch README.

Usage: python3 tools/build_assets.py <fonts-dir>
<fonts-dir> holds fontsource woff2 files for IBM Plex Sans and Cascadia Code.
Edit the data blocks below and re-run to update the graphics.
"""

import base64
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FILES = {
    ("plex", 400): "ibm-plex-sans-latin-400-normal.woff2",
    ("plex", 500): "ibm-plex-sans-latin-500-normal.woff2",
    ("plex", 600): "ibm-plex-sans-latin-600-normal.woff2",
    ("plex", 700): "ibm-plex-sans-latin-700-normal.woff2",
    ("mono", 400): "cascadia-code-latin-400-normal.woff2",
    ("mono", 700): "cascadia-code-latin-700-normal.woff2",
}
_fonts = {k: TTFont(FONTS / v) for k, v in FILES.items()}

# ---- palette ---------------------------------------------------------------
NIGHT = "#0B1730"
NIGHT2 = "#0F2245"
PANEL = "#0B1A35"
LINE = "#23406F"
ICE = "#EAF1FB"
SOFT = "#CFDBEE"
MIST = "#A9BBD8"
CYAN = "#38C8F0"
GREEN = "#3FD07A"
AMBER = "#F5C451"
CHIP = "#13284D"
CHIPLINE = "#2A4C80"

ICONS = {
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 .6-7.96A6 6 0 0 0 6.2 9.2 4.5 4.5 0 0 0 7 18z"/>',
    "server": '<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01M12 7h4M12 17h4"/>',
    "database": '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3.5 17.5l3 3 5.8-5.8a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "network": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M10.7 7.2l-4.4 9.6M13.3 7.2l4.4 9.6M7.5 19h9"/>',
    "candles": '<path d="M6 3.5v4M6 15v5.5M12 2.5v3M12 13v4.5M18 6v4.5M18 17v3.5"/><rect x="4.3" y="7.5" width="3.4" height="7.5" rx="0.6"/><rect x="10.3" y="5.5" width="3.4" height="7.5" rx="0.6"/><rect x="16.3" y="10.5" width="3.4" height="6.5" rx="0.6"/>',
    "cube": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "bolt": '<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M13 7.5l-3.5 5h3l-1 4 3.5-5h-3z"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "pin": '<path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M7 7l10 10M17 7L7 17"/>',
    "box": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "lines": '<path d="M5 6h14M5 12h14M5 18h9"/>',
    "retry": '<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 4v4h-4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "fork": '<circle cx="6" cy="5" r="2"/><circle cx="18" cy="5" r="2"/><circle cx="12" cy="19" r="2"/><path d="M6 7v2a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V7M12 12v5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4.5 20c1.2-3.8 4-5.5 7.5-5.5s6.3 1.7 7.5 5.5"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5l5 5"/>',
    "pulse": '<path d="M2.5 12.5h4.5l2.2-5.5 4.6 11 2.4-5.5h5.3"/>',
    "tag": '<path d="M3.5 12.6V4.5a1 1 0 0 1 1-1h8.1l8 8-9 9z"/><circle cx="8.2" cy="8.2" r="1.5"/>',
    "report": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h5"/>',
    "pause": '<circle cx="12" cy="12" r="9"/><path d="M10 9v6M14 9v6"/>',
    "apple": '<path d="M15.5 3.5c-1.2.1-2.6.9-3.2 2-.5.9-.7 1.9-.6 2.8 1.3.1 2.6-.7 3.3-1.8.5-.9.7-2 .5-3z"/><path d="M12 8.8c-1-.6-2.4-1-3.6-.8C6.2 8.4 4.8 10.5 5 13.4c.2 3.3 2.3 7 4.4 7.1.9 0 1.6-.5 2.6-.5s1.7.5 2.6.5c2.1-.1 4-3.6 4.4-6-1.9-.8-2.9-2.6-2.6-4.6.2-1 .8-1.9 1.6-2.4-1.7-1.5-4.1-1.3-6 .3z"/>',
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def measure(text, fam="plex", w=400, size=16):
    f = _fonts[(fam, w)]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    total = 0
    for ch in text:
        g = cmap.get(ord(ch))
        total += hmtx[g][0] if g else upm * 0.5
    return total / upm * size


def wrap(text, width, fam="plex", w=400, size=16):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if measure(trial, fam, w, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.body, self.css, self.defs = [], [], []
        self.used = {}

    def text(self, x, y, s, fam="plex", w=400, size=16, fill=ICE, anchor="start", extra="", cls=""):
        self.used.setdefault((fam, w), set()).update(s)
        family = ("P" if fam == "plex" else "M") + (f" {cls}" if cls else "")
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        self.body.append(
            f'<text x="{x:.1f}" y="{y:.1f}" class="{family}" font-weight="{w}" '
            f'font-size="{size}" fill="{fill}"{a} {extra}>{esc(s)}</text>'
        )

    def icon(self, name, x, y, size=24, stroke="#fff", sw=1.8):
        k = size / 24
        self.body.append(
            f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.3f})" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>'
        )

    def raw(self, s):
        self.body.append(s)

    def fontcss(self):
        out = []
        for (fam, w), chars in sorted(self.used.items()):
            f = TTFont(FONTS / FILES[(fam, w)])
            o = subset.Options()
            o.flavor = "woff2"
            o.layout_features = ["kern"]
            o.hinting = False
            sub = subset.Subsetter(o)
            sub.populate(text="".join(sorted(chars | {" "})))
            sub.subset(f)
            buf = io.BytesIO()
            f.flavor = "woff2"
            f.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            name = "PlexSub" if fam == "plex" else "CascadiaSub"
            out.append(
                f"@font-face{{font-family:'{name}';font-weight:{w};"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
            )
        return "".join(out)

    def save(self, name):
        css = (
            self.fontcss()
            + ".P{font-family:'PlexSub','IBM Plex Sans','Segoe UI',system-ui,-apple-system,sans-serif}"
            + ".M{font-family:'CascadiaSub','Cascadia Code',Consolas,'SFMono-Regular',Menlo,monospace;"
            "white-space:pre}"
            + "".join(self.css)
        )
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.title)}">'
            f"<title>{esc(self.title)}</title><style>{css}</style>"
            f"<defs>{''.join(self.defs)}</defs>{''.join(self.body)}</svg>"
        )
        (OUT / name).write_text(svg)
        return OUT / name


def card_bg(s, x, y, w, h, r=16, gid="cardg"):
    if not any(gid in d for d in s.defs):
        s.defs.append(
            f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{NIGHT2}"/><stop offset="1" stop-color="{NIGHT}"/></linearGradient>'
        )
    s.raw(
        f'<rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{h-1}" rx="{r}" '
        f'fill="url(#{gid})" stroke="{LINE}"/>'
    )


# =============================================================================
# 1. HERO
# =============================================================================
FP_STATS = [("600+", "machines patched"), ("99%", "success rate"), ("5", "checks per machine")]
FP_LOOP = [
    ("search", "Detect", "Failed and missing patches from Kaseya"),
    ("pulse", "Diagnose", "Five timestamped checks on the agent"),
    ("tag", "Classify", "One cause from a shared vocabulary"),
    ("wrench", "Remediate", "The approved fix, inside client policy"),
    ("shield", "Verify", "KB present after the reboot, not just a job"),
    ("report", "Report", "A ticket-ready line: cause plus action"),
]
# Illustrative run: hosts are made up; shows the shape of the output, not real data.
FP_RUN = [
    ("WS-0142", "component store", "DISM repair, retry", "ok"),
    ("SRV-FS01", "servicing stack", "stack update first", "ok"),
    ("WS-0388", "low disk on C:", "cleanup, retry", "ok"),
    ("WS-0517", "pending reboot", "held for the window", "hold"),
]
FP_GUARDS = [
    "Never forces a reboot",
    "Never rewrites update policy",
    "Fixes only inside client approvals",
    "Proves the KB landed, not the job",
    "Same flow on 10 machines or 100+",
]


def fastpatch_hero():
    W, H = 1000, 690
    s = Svg(W, H, "FastPatch: patch night, on autopilot. Self-healing Windows patch remediation "
                  "for Kaseya VSA fleets. 600+ machines patched at 99% success. Detect, diagnose, "
                  "classify, remediate, verify, report. Never forces a reboot, never rewrites update "
                  "policy. macOS support is next.")
    G1, G2 = "#3FD07A", "#16B3A0"
    s.defs.append(
        '<linearGradient id="fbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#08142B"/>'
        '<stop offset="1" stop-color="#0D2347"/></linearGradient>'
        f'<radialGradient id="fglow" cx="0.12" cy="0.08" r="0.55"><stop offset="0" stop-color="{G1}" '
        f'stop-opacity="0.20"/><stop offset="1" stop-color="{G1}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="fglow2" cx="0.92" cy="0.95" r="0.5"><stop offset="0" stop-color="{CYAN}" '
        f'stop-opacity="0.13"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        '<pattern id="fgrid" width="28" height="28" patternUnits="userSpaceOnUse">'
        '<path d="M28 0H0V28" fill="none" stroke="#FFFFFF" stroke-opacity="0.045"/></pattern>'
        f'<clipPath id="fframe"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
        f'<linearGradient id="flogo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{G1}"/>'
        f'<stop offset="1" stop-color="{G2}"/></linearGradient>'
        f'<linearGradient id="fhl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{G1}"/>'
        f'<stop offset="1" stop-color="{CYAN}"/></linearGradient>'
        f'<linearGradient id="fedge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{G1}" '
        f'stop-opacity="0.75"/><stop offset="1" stop-color="{LINE}"/></linearGradient>'
        f'<filter id="fblur" x="-50%" y="-50%" width="200%" height="200%">'
        f'<feGaussianBlur stdDeviation="6"/></filter>'
    )
    s.raw('<g clip-path="url(#fframe)">')
    for f in ("fbg", "fgrid", "fglow", "fglow2"):
        s.raw(f'<rect width="{W}" height="{H}" fill="url(#{f})"/>')
    s.raw("</g>")
    s.raw(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{LINE}"/>')

    css = s.css
    css.append(
        "@keyframes fpulse{0%,100%{opacity:.45}50%{opacity:1}}"
        "@keyframes fring{0%{r:4;opacity:.8}100%{r:12;opacity:0}}"
        "@keyframes fflow{to{stroke-dashoffset:-56}}"
    )

    # ---- header -------------------------------------------------------------
    X = 48
    s.raw(f'<rect x="{X+4}" y="46" width="60" height="60" rx="16" fill="{G1}" opacity="0.45" '
          f'filter="url(#fblur)"/>')
    s.raw(f'<rect x="{X}" y="40" width="68" height="68" rx="17" fill="url(#flogo)"/>')
    s.icon("bolt", X + 13, 53, 42, "#FFFFFF", 1.8)
    s.text(X + 88, 80, "FastPatch", "plex", 700, 40, ICE)

    px = X + 90
    pills = [("Live in production", GREEN, True), ("Built for Kaseya VSA", CYAN, False),
             ("macOS next", AMBER, False)]
    for lab, col, dot in pills:
        pw = measure(lab, "plex", 500, 13) + 24 + (14 if dot else 0)
        s.raw(f'<rect x="{px+0.5:.1f}" y="91.5" width="{pw:.1f}" height="24" rx="12" fill="{col}" '
              f'fill-opacity="0.10" stroke="{col}" stroke-opacity="0.65"/>')
        tx = px + 12
        if dot:
            s.raw(f'<circle cx="{px+15:.1f}" cy="103.5" r="4" fill="{col}"/>')
            s.raw(f'<circle class="fring" cx="{px+15:.1f}" cy="103.5" r="4" fill="none" stroke="{col}"/>')
            tx += 14
        s.text(tx, 108, lab, "plex", 500, 13, col)
        px += pw + 8

    s.text(X, 172, "Patch night,", "plex", 700, 38, ICE)
    s.text(X + measure("Patch night, ", "plex", 700, 38), 172, "on autopilot.", "plex", 700, 38,
           "url(#fhl)")
    sub = ("Finds every failed Windows update across the fleet, names the cause, applies the "
           "approved fix and proves it landed. All on the Kaseya agent you already run.")
    for i, ln in enumerate(wrap(sub, 540, "plex", 400, 17)):
        s.text(X, 206 + i * 25, ln, "plex", 400, 17, "#B9C8DF")

    # ---- stat tiles ---------------------------------------------------------
    TX, TY, TW_, TH, TG_ = 624, 40, 108, 120, 8
    for i, (big, lab) in enumerate(FP_STATS):
        x = TX + i * (TW_ + TG_)
        s.raw(f'<rect x="{x+0.5}" y="{TY+0.5}" width="{TW_-1}" height="{TH-1}" rx="14" '
              f'fill="{PANEL}" fill-opacity="0.85" stroke="url(#fedge)"/>')
        s.text(x + 16, TY + 54, big, "plex", 700, 36, G1 if i < 2 else ICE)
        for j, ln in enumerate(wrap(lab, TW_ - 30, "plex", 500, 13)):
            s.text(x + 16, TY + 80 + j * 17, ln, "plex", 500, 13, MIST)
    # roadmap tile
    ry = TY + TH + 10
    rw = 3 * TW_ + 2 * TG_
    s.raw(f'<rect x="{TX+0.5}" y="{ry+0.5}" width="{rw-1}" height="63" rx="14" fill="{AMBER}" '
          f'fill-opacity="0.07" stroke="{AMBER}" stroke-opacity="0.45"/>')
    s.icon("apple", TX + 16, ry + 18, 26, AMBER, 1.6)
    s.text(TX + 54, ry + 28, "Coming next: macOS", "plex", 600, 15.5, ICE)
    s.text(TX + 54, ry + 48, "Mac endpoints on the same loop", "plex", 400, 13.5, MIST)

    # ---- the loop -----------------------------------------------------------
    s.text(X, 298, "THE LOOP", "mono", 700, 12.5, G1, extra='letter-spacing="2.5"')
    s.text(X + 92, 298, "runs on every machine, every patch night", "plex", 400, 13.5, MIST)
    LX, LY, LW, LH = 32, 312, 936, 168
    s.raw(f'<rect x="{LX+0.5}" y="{LY+0.5}" width="{LW-1}" height="{LH-1}" rx="16" fill="{PANEL}" '
          f'fill-opacity="0.78" stroke="{LINE}"/>')
    n = len(FP_LOOP)
    slot = (LW - 32) / n
    cxs = [LX + 16 + slot * (i + 0.5) for i in range(n)]
    cy = LY + 50
    R = 25
    s.raw(f'<line x1="{cxs[0]:.1f}" y1="{cy}" x2="{cxs[-1]:.1f}" y2="{cy}" stroke="{LINE}" '
          f'stroke-width="2"/>')
    s.raw(f'<line class="fflow" x1="{cxs[0]:.1f}" y1="{cy}" x2="{cxs[-1]:.1f}" y2="{cy}" stroke="{G1}" '
          f'stroke-width="2" stroke-dasharray="6 8" stroke-opacity="0.75"/>')
    cyc = 7.2
    dist = cxs[-1] - cxs[0]
    css.append(
        f"@keyframes ftravel{{0%{{transform:translateX(0);opacity:0}}3%{{opacity:1}}"
        f"72%{{opacity:1}}75%{{transform:translateX({dist:.1f}px);opacity:0}}"
        f"100%{{transform:translateX({dist:.1f}px);opacity:0}}}}"
        "@keyframes flit{0%{opacity:0}4%{opacity:1}16%{opacity:1}30%{opacity:0}100%{opacity:0}}"
        "@media (prefers-reduced-motion:no-preference){"
        f".fdot{{animation:ftravel {cyc}s linear infinite}}"
        ".fflow{animation:fflow 2.4s linear infinite}"
        ".fring{animation:fring 2s ease-out infinite}"
        ".flive{animation:fpulse 2.4s ease-in-out infinite}"
        + "".join(f".flit{i}{{opacity:0;animation:flit {cyc}s linear {cyc*0.15*i:.2f}s infinite}}"
                  for i in range(n))
        + "}"
        "@media (prefers-reduced-motion:reduce){.fdot{display:none}}"
    )
    for i, (ic, name, cap) in enumerate(FP_LOOP):
        x = cxs[i]
        last = i >= 4
        col = G1 if last else CYAN
        s.raw(f'<circle class="flit{i}" cx="{x:.1f}" cy="{cy}" r="{R+8}" fill="{col}" fill-opacity="0.28" '
              f'filter="url(#fblur)"/>')
        s.raw(f'<circle cx="{x:.1f}" cy="{cy}" r="{R}" fill="{CHIP}" stroke="{col}" stroke-width="1.6"/>')
        s.icon(ic, x - 12, cy - 12, 24, col, 1.8)
        s.text(x, cy + 50, name, "plex", 600, 16, ICE, anchor="middle")
        for j, ln in enumerate(wrap(cap, slot - 20, "plex", 400, 13)):
            s.text(x, cy + 71 + j * 17, ln, "plex", 400, 13, MIST, anchor="middle")
    s.raw(f'<g class="fdot"><circle cx="{cxs[0]:.1f}" cy="{cy}" r="9" fill="{G1}" opacity="0.5" '
          f'filter="url(#fblur)"/><circle cx="{cxs[0]:.1f}" cy="{cy}" r="4.5" fill="#FFFFFF"/></g>')

    # ---- sample run terminal ------------------------------------------------
    BY, BH = 500, 172
    tx0, tw = 32, 560
    s.raw(f'<rect x="{tx0+0.5}" y="{BY+0.5}" width="{tw-1}" height="{BH-1}" rx="16" fill="#060F22" '
          f'stroke="{LINE}"/>')
    s.raw(f'<path d="M{tx0+0.5} {BY+36}H{tx0+tw-0.5}" stroke="{LINE}"/>')
    for k, c in enumerate(("#F2655B", AMBER, G1)):
        s.raw(f'<circle cx="{tx0+22+k*16}" cy="{BY+18.5}" r="5" fill="{c}" fill-opacity="0.85"/>')
    s.text(tx0 + 80, BY + 23, "fastpatch  ·  sample run", "mono", 400, 13, MIST)
    s.text(tx0 + tw - 18, BY + 23, "illustrative", "plex", 500, 12, "#6F86AB", anchor="end")
    FS = 13.5
    cols = [tx0 + 20, tx0 + 112, tx0 + 262, tx0 + 432]
    hy = BY + 60
    for cx_, lab in zip(cols, ("HOST", "CAUSE", "ACTION", "RESULT")):
        s.text(cx_, hy, lab, "mono", 400, 11.5, "#6F86AB", extra='letter-spacing="1.2"')
    m = len(FP_RUN)
    kfs = []
    for k, (host, cause, act, res) in enumerate(FP_RUN):
        y = hy + 25 + k * 23
        a = 6 + k * 11
        kfs.append(f"@keyframes frun{k}{{0%{{opacity:0}}{a}%{{opacity:0}}{a+3}%{{opacity:1}}"
                   f"88%{{opacity:1}}94%{{opacity:0}}100%{{opacity:0}}}}"
                   f"@media (prefers-reduced-motion:no-preference){{.frun{k}{{animation:frun{k} 9s infinite}}}}")
        s.raw(f'<g class="frun{k}">')
        s.text(cols[0], y, host, "mono", 400, FS, ICE)
        s.text(cols[1], y, cause, "mono", 400, FS, "#B9C8DF")
        s.text(cols[2], y, act, "mono", 400, FS, SOFT)
        if res == "ok":
            s.icon("check", cols[3] - 1, y - 13, 16, G1, 2.6)
            s.text(cols[3] + 20, y, "verified", "mono", 400, FS, G1)
        else:
            s.icon("pause", cols[3] - 1, y - 13, 16, AMBER, 2)
            s.text(cols[3] + 20, y, "held", "mono", 400, FS, AMBER)
        s.raw("</g>")
    css.extend(kfs)

    # ---- guardrails ---------------------------------------------------------
    gx, gw = tx0 + tw + 16, W - 32 - (tx0 + tw + 16)
    s.raw(f'<rect x="{gx+0.5}" y="{BY+0.5}" width="{gw-1}" height="{BH-1}" rx="16" fill="{PANEL}" '
          f'fill-opacity="0.8" stroke="{LINE}"/>')
    s.icon("shield", gx + 20, BY + 16, 22, G1, 1.8)
    s.text(gx + 50, BY + 33, "Guardrails, not hope", "plex", 600, 16.5, ICE)
    for k, g in enumerate(FP_GUARDS):
        y = BY + 66 + k * 22.5
        s.icon("check", gx + 22, y - 13, 16, G1, 2.6)
        s.text(gx + 46, y, g, "plex", 400, 14.5, "#C8D5EA")
    s.save("hero.svg")



# =============================================================================
# shared frame
# =============================================================================
G1, G2, RED, VIOLET = "#3FD07A", "#16B3A0", "#F2655B", "#A78BFA"


def frame(s, W, H, glow=G1, gx=0.1, gy=0.0):
    s.defs.append(
        '<linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#08142B"/>'
        '<stop offset="1" stop-color="#0D2347"/></linearGradient>'
        f'<radialGradient id="sglow" cx="{gx}" cy="{gy}" r="0.7"><stop offset="0" stop-color="{glow}" '
        f'stop-opacity="0.16"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>'
        '<pattern id="sgrid" width="28" height="28" patternUnits="userSpaceOnUse">'
        '<path d="M28 0H0V28" fill="none" stroke="#FFFFFF" stroke-opacity="0.04"/></pattern>'
        f'<clipPath id="sframe"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
        '<filter id="sblur" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="6"/></filter>'
    )
    s.raw('<g clip-path="url(#sframe)">')
    for f in ("sbg", "sgrid", "sglow"):
        s.raw(f'<rect width="{W}" height="{H}" fill="url(#{f})"/>')
    s.raw("</g>")
    s.raw(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{LINE}"/>')


def heading(s, x, y, kicker, title, col=G1):
    s.text(x, y, kicker, "mono", 700, 12.5, col, extra='letter-spacing="2.5"')
    s.text(x, y + 34, title, "plex", 700, 27, ICE)


# =============================================================================
# 2. FEATURES
# =============================================================================
FEATURES = [
    ("pulse", "Diagnoses before it fixes",
     "Five timestamped checks run on every machine before anything is touched."),
    ("tag", "Names the real cause",
     "One label from a shared vocabulary, so every engineer reads the same answer."),
    ("wrench", "Fixes inside your policy",
     "Only the approved path for that cause, rolled out one machine group at a time."),
    ("shield", "Proof, not job status",
     "Done means the update is installed after the restart, not that a job ran."),
    ("lines", "Ticket-ready output",
     "Status, cause and action on one line per machine. The NOC works exceptions only."),
    ("box", "Nothing new to install",
     "Runs inside the Kaseya VSA you already have, as a signed procedure per group."),
]


def features():
    W, COLS, GAP = 1000, 3, 16
    CW, CH = (W - 64 - GAP * (COLS - 1)) / COLS, 192
    rows = (len(FEATURES) + COLS - 1) // COLS
    H = 116 + rows * CH + (rows - 1) * GAP + 32
    s = Svg(W, H, "FastPatch features. " + " ".join(f"{t}: {d}" for _, t, d in FEATURES))
    frame(s, W, H, CYAN, 0.9, 0.0)
    heading(s, 40, 52, "FEATURES", "Everything patch night needs. Nothing it doesn't.")
    s.defs.append(f'<linearGradient id="ftile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" '
                  f'stop-color="{G1}"/><stop offset="1" stop-color="{G2}"/></linearGradient>')
    s.css.append("@keyframes fshine{0%,100%{opacity:.35}50%{opacity:.9}}"
                 "@media (prefers-reduced-motion:no-preference){"
                 + "".join(f".fs{i}{{animation:fshine 4.8s ease-in-out {i*0.8:.1f}s infinite}}"
                           for i in range(len(FEATURES))) + "}")
    for i, (ic, title, desc) in enumerate(FEATURES):
        r, c = divmod(i, COLS)
        x = 32 + c * (CW + GAP)
        y = 116 + r * (CH + GAP)
        s.raw(f'<rect x="{x+0.5:.1f}" y="{y+0.5}" width="{CW-1:.1f}" height="{CH-1}" rx="16" '
              f'fill="{PANEL}" fill-opacity="0.85" stroke="{LINE}"/>')
        s.raw(f'<path class="fs{i}" d="M{x+20:.1f} {y+0.8}H{x+CW-20:.1f}" stroke="{G1}" '
              f'stroke-width="1.6" stroke-linecap="round"/>')
        s.raw(f'<rect x="{x+22:.1f}" y="{y+24}" width="44" height="44" rx="12" fill="url(#ftile)"/>')
        s.icon(ic, x + 32, y + 34, 24, "#FFFFFF", 1.9)
        s.text(x + 22, y + 98, title, "plex", 600, 18, ICE)
        for j, ln in enumerate(wrap(desc, CW - 44, "plex", 400, 14.5)):
            s.text(x + 22, y + 124 + j * 21, ln, "plex", 400, 14.5, "#B9C8DF")
    s.save("features.svg")


# =============================================================================
# 3. RUN LOOP (orbit)
# =============================================================================
LOOP = [
    ("Schedule", "A signed procedure runs for one machine group at a time"),
    ("Run on the agent", "Five checks, then the approved fix"),
    ("Result line", "Status · cause · action per machine"),
    ("Branch and log", "Kaseya routes each result and keeps the logs"),
    ("Verify", "After your restart window: the update really landed"),
]


def loop():
    import math
    W, H = 1000, 460
    s = Svg(W, H, "How FastPatch runs inside Kaseya VSA: " +
            "; ".join(f"{i+1}. {t}: {d}" for i, (t, d) in enumerate(LOOP)))
    frame(s, W, H, G1, 0.5, 0.55)
    heading(s, 40, 52, "HOW IT RUNS", "One loop, inside the console")
    s.text(40, 110, "you already run.", "plex", 700, 27, ICE)
    cx, cy, R = 560, 250, 150
    s.defs.append(
        f'<radialGradient id="core" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#14365F"/>'
        f'<stop offset="1" stop-color="{PANEL}"/></radialGradient>'
        f'<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{G1}"/>'
        f'<stop offset="1" stop-color="{CYAN}"/></linearGradient>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="url(#ring)" stroke-width="10" '
          f'stroke-opacity="0.18" filter="url(#sblur)"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LINE}" stroke-width="2"/>')
    s.raw(f'<circle class="lflow" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="url(#ring)" '
          f'stroke-width="2" stroke-dasharray="5 9" stroke-opacity="0.8"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="72" fill="url(#core)" stroke="{CHIPLINE}"/>')
    s.text(cx, cy - 2, "Kaseya VSA", "plex", 700, 19, ICE, anchor="middle")
    s.text(cx, cy + 22, "YOUR CONSOLE", "mono", 400, 11, MIST, anchor="middle",
           extra='letter-spacing="1.8"')
    cyc = 10.0
    s.css.append(
        f"@keyframes lspin{{to{{transform:rotate(360deg)}}}}"
        "@keyframes lflow{to{stroke-dashoffset:-56}}"
        "@keyframes llit{0%{opacity:0}5%{opacity:1}14%{opacity:1}24%{opacity:0}100%{opacity:0}}"
        "@media (prefers-reduced-motion:no-preference){"
        f".lsat{{transform-origin:{cx}px {cy}px;animation:lspin {cyc}s linear infinite}}"
        ".lflow{animation:lflow 3s linear infinite}"
        + "".join(f".ll{i}{{opacity:0;animation:llit {cyc}s linear {cyc/5*i:.2f}s infinite}}"
                  for i in range(5)) + "}"
        "@media (prefers-reduced-motion:reduce){.lsat{display:none}}")
    for i, (t, d) in enumerate(LOOP):
        a = math.radians(-90 + 72 * i)
        nx, ny = cx + R * math.cos(a), cy + R * math.sin(a)
        col = G1 if i == 4 else CYAN
        s.raw(f'<circle class="ll{i}" cx="{nx:.1f}" cy="{ny:.1f}" r="34" fill="{col}" '
              f'fill-opacity="0.35" filter="url(#sblur)"/>')
        s.raw(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="24" fill="{CHIP}" stroke="{col}" stroke-width="1.8"/>')
        s.text(nx, ny + 5.5, f"0{i+1}", "mono", 700, 15, col, anchor="middle")
        right = math.cos(a) > -0.1
        lx = nx + (40 if right else -40)
        anc = "start" if right else "end"
        ly = ny - 4 if i else ny - 6
        s.text(lx, ly, t, "plex", 600, 17, ICE, anchor=anc)
        for j, ln in enumerate(wrap(d, 220, "plex", 400, 13.5)):
            s.text(lx, ly + 20 + j * 18, ln, "plex", 400, 13.5, MIST, anchor=anc)
    s.raw(f'<g class="lsat"><circle cx="{cx}" cy="{cy-R}" r="10" fill="{G1}" opacity="0.55" '
          f'filter="url(#sblur)"/><circle cx="{cx}" cy="{cy-R}" r="5" fill="#FFFFFF"/></g>')
    s.save("loop.svg")


# =============================================================================
# 4. GUARDRAILS
# =============================================================================
NEVERS = [
    ("Restart your machines", "Your maintenance window does that, on your schedule"),
    ("Change Windows Update settings", "It works with whoever manages updates today"),
    ("Delete Windows repair files", "It repairs. It never wipes."),
    ("Touch antivirus or security tools", "Your security stack stays exactly as it is"),
    ("Loop without a limit", "One search, one download, one install per run"),
    ("Say “success” without proof", "Done means installed after the restart"),
]


def guardrails():
    W, COLS, GAP = 1000, 2, 14
    CW, CH = (W - 64 - GAP) / COLS, 82
    rows = len(NEVERS) // COLS
    H = 118 + rows * CH + (rows - 1) * GAP + 32
    s = Svg(W, H, "Six things FastPatch will never do: " +
            "; ".join(f"{t} ({d})" for t, d in NEVERS))
    frame(s, W, H, RED, 0.08, 0.0)
    heading(s, 40, 52, "GUARDRAILS", "Six things FastPatch will never do.", RED)
    s.css.append("@keyframes gstrike{0%,12%{stroke-dashoffset:var(--l)}30%,100%{stroke-dashoffset:0}}"
                 "@media (prefers-reduced-motion:no-preference){"
                 + "".join(f".gs{i}{{animation:gstrike 7s ease-out {i*0.35:.2f}s infinite}}"
                           for i in range(len(NEVERS))) + "}")
    for i, (t, d) in enumerate(NEVERS):
        r, c = divmod(i, COLS)
        x = 32 + c * (CW + GAP)
        y = 118 + r * (CH + GAP)
        s.raw(f'<rect x="{x+0.5:.1f}" y="{y+0.5}" width="{CW-1:.1f}" height="{CH-1}" rx="14" '
              f'fill="{PANEL}" fill-opacity="0.85" stroke="{LINE}"/>')
        s.raw(f'<circle cx="{x+40:.1f}" cy="{y+CH/2}" r="18" fill="{RED}" fill-opacity="0.12" '
              f'stroke="{RED}" stroke-opacity="0.6"/>')
        s.icon("x", x + 30, y + CH / 2 - 10, 20, RED, 2.4)
        s.text(x + 72, y + 35, t, "plex", 600, 17, ICE)
        tw = measure(t, "plex", 600, 17)
        s.raw(f'<path class="gs{i}" style="--l:{tw:.0f}" d="M{x+72:.1f} {y+29.5}h{tw:.1f}" '
              f'stroke="{RED}" stroke-width="2" stroke-opacity="0.8" stroke-dasharray="{tw:.0f}"/>')
        s.text(x + 72, y + 59, d, "plex", 400, 14, MIST)
    s.save("guardrails.svg")


# =============================================================================
# 5. OUTCOMES
# =============================================================================
OUTCOMES = [
    ("check", "Fixed itself", "Patched and verified", G1),
    ("retry", "Try again later", "Safe to retry next run", CYAN),
    ("clock", "Waiting for a restart", "Lands after your window", AMBER),
    ("fork", "Needs a decision", "A policy or approval call", VIOLET),
    ("user", "Needs an engineer", "Comes with the cause", RED),
]


def outcomes():
    W, H = 1000, 250
    s = Svg(W, H, "Every machine ends with one of five answers: " +
            ", ".join(f"{t} ({d})" for _, t, d, _ in OUTCOMES))
    frame(s, W, H, VIOLET, 0.95, 0.0)
    heading(s, 40, 52, "OUTCOMES", "Every machine ends with a clear answer.", VIOLET)
    n, GAP = len(OUTCOMES), 12
    CW = (W - 64 - GAP * (n - 1)) / n
    y = 118
    for i, (ic, t, d, col) in enumerate(OUTCOMES):
        x = 32 + i * (CW + GAP)
        s.raw(f'<rect x="{x+0.5:.1f}" y="{y+0.5}" width="{CW-1:.1f}" height="99" rx="14" fill="{col}" '
              f'fill-opacity="0.07" stroke="{col}" stroke-opacity="0.55"/>')
        s.raw(f'<circle cx="{x+30:.1f}" cy="{y+30}" r="14" fill="{col}" fill-opacity="0.18"/>')
        s.icon(ic, x + 21, y + 21, 18, col, 2.2)
        s.text(x + 18, y + 68, t, "plex", 600, 15, ICE)
        s.text(x + 18, y + 88, d, "plex", 400, 12.5, MIST)
    s.save("outcomes.svg")


fastpatch_hero()
features()
loop()
guardrails()
outcomes()
for p in sorted(OUT.glob("*.svg")):
    print(f"{p.name:24s} {p.stat().st_size/1024:6.1f} KB")
