"""Builds the Market Lab diagrams. Run: python3 gen.py, then export PNGs with rsvg-convert."""
from xml.sax.saxutils import escape as E

FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"
INK, SUB = "#0F172A", "#475569"


def svg(name, w, h, body):
    mk = ('<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
          'markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#64748B"/></marker>')
    with open(name, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}" font-family="{FONT}">\n<defs>{mk}</defs>\n'
                f'<rect width="{w}" height="{h}" rx="24" fill="#FFFFFF"/>\n' + "\n".join(body) + "\n</svg>\n")


def text(o, x, y, s, fs=18, fill=INK, bold=False, ital=False):
    extra = (' font-weight="700"' if bold else "") + (' font-style="italic"' if ital else "")
    o.append(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{fill}" text-anchor="middle"{extra}>{E(s)}</text>')


def box(o, x, y, w, h, title, sub, fill, stroke, dash=False):
    d = ' stroke-dasharray="8 6"' if dash else ""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>')
    text(o, x + w / 2, y + h / 2 - 4, title, 20, bold=True)
    text(o, x + w / 2, y + h / 2 + 22, sub, 15, SUB)


def arrow(o, x1, y1, x2, y2, dash=False):
    d = ' stroke-dasharray="6 6"' if dash else ""
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748B" stroke-width="2.5" marker-end="url(#a)"{d}/>')


BLUE = ("#EFF6FF", "#3B82F6")
GREEN = ("#ECFDF5", "#10B981")
AMBER = ("#FFFBEB", "#F59E0B")
GRAY = ("#F8FAFC", "#94A3B8")

# 1. Simple architecture: one capture session, left to right.
o = []
text(o, 600, 50, "Market Lab: how data moves", 26, bold=True)
box(o, 40, 120, 200, 110, "Market feed", "licensed data", *GRAY)
box(o, 300, 120, 200, 110, "Rate gate", "shared call limit", *AMBER)
box(o, 560, 120, 200, 110, "Capture", "scheduled scripts", *BLUE)
box(o, 820, 120, 200, 110, "Local storage", "private, dated", *GREEN)
arrow(o, 560, 160, 502, 160)
arrow(o, 300, 160, 242, 160)
arrow(o, 242, 192, 298, 192)
arrow(o, 502, 192, 558, 192)
arrow(o, 760, 175, 818, 175)
box(o, 560, 300, 200, 100, "Watchdog", "restarts capture", *AMBER)
arrow(o, 660, 300, 660, 232, dash=True)
box(o, 820, 300, 200, 100, "Rundowns", "summaries + charts", *BLUE)
arrow(o, 920, 230, 920, 298)
box(o, 1060, 300, 120, 100, "Me", "review", *GRAY)
arrow(o, 1020, 350, 1058, 350)
text(o, 600, 450, "Raw data stays local. Only summaries and charts leave.", 16, SUB, ital=True)
svg("market-lab-architecture-simple.svg", 1200, 480, o)

# 2. Current state vs future state: only storage moves.
o = []
text(o, 600, 50, "Market Lab: current vs future state", 26, bold=True)
text(o, 100, 140, "Today", 20, bold=True)
box(o, 180, 90, 240, 100, "Capture", "on my computer", *BLUE)
box(o, 480, 90, 240, 100, "Local storage", "dated folders", *GREEN)
box(o, 780, 90, 240, 100, "Rundowns", "summaries + charts", *BLUE)
arrow(o, 420, 140, 478, 140)
arrow(o, 720, 140, 778, 140)
text(o, 100, 300, "Planned", 20, bold=True)
box(o, 180, 250, 240, 100, "Capture", "unchanged", *BLUE)
box(o, 480, 250, 240, 100, "Cloud storage", "AWS, not final", *GREEN, dash=True)
box(o, 780, 250, 240, 100, "Rundowns", "unchanged", *BLUE)
arrow(o, 420, 300, 478, 300, dash=True)
arrow(o, 720, 300, 778, 300, dash=True)
text(o, 600, 400, "Only the storage layer moves. Capture and review stay the same.", 16, SUB, ital=True)
svg("market-lab-current-vs-future.svg", 1200, 430, o)

# 3. Placeholder photo.
o = ['<rect x="12" y="12" width="616" height="456" rx="20" fill="#F1F5F9" stroke="#94A3B8" stroke-width="3" stroke-dasharray="14 10"/>',
     '<polyline points="120,330 220,260 300,290 400,190 520,230" fill="none" stroke="#3B82F6" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>']
text(o, 320, 400, "Placeholder image", 28, SUB, bold=True)
svg("market-lab-placeholder.svg", 640, 480, o)
