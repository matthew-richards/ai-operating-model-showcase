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


def arrow(o, x1, y1, x2, y2, dash=False, color="#64748B"):
    d = ' stroke-dasharray="6 6"' if dash else ""
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" marker-end="url(#a)"{d}/>')


BLUE = ("#EFF6FF", "#3B82F6")
GREEN = ("#ECFDF5", "#10B981")
AMBER = ("#FFFBEB", "#F59E0B")
GRAY = ("#F8FAFC", "#94A3B8")

# 1. Simple architecture: one capture session.
# Solid arrows carry data one way, left to right. Dashed arrows are requests.
o = []
text(o, 650, 44, "Market Lab: how data moves", 26, bold=True)
Y, H, BW = 210, 100, 170
xs = [30, 240, 450, 660, 870, 1080]
box(o, xs[0], Y, BW, H, "Data provider", "any platform", *GRAY)
box(o, xs[1], Y, BW, H, "Provider adapter", "swap point", *GRAY)
box(o, xs[2], Y, BW, H, "Capture", "scheduled jobs", *BLUE)
box(o, xs[3], Y, BW, H, "Private storage", "dated folders", *GREEN)
box(o, xs[4], Y, BW, H, "Backtests", "lab + rundowns", *BLUE)
box(o, xs[5], Y, BW, H, "Me", "review", *GRAY)
box(o, 345, 70, 170, 80, "API budget gate", "shared limits", *AMBER)
arrow(o, 520, Y - 2, 480, 152, dash=True)
arrow(o, 380, 152, 340, Y - 2, dash=True)
arrow(o, xs[1], Y + 30, xs[0] + BW + 2, Y + 30, dash=True)
arrow(o, xs[0] + BW, Y + 70, xs[1] - 2, Y + 70)
arrow(o, xs[1] + BW, Y + 70, xs[2] - 2, Y + 70)
for i in (2, 3, 4):
    arrow(o, xs[i] + BW, Y + 50, xs[i + 1] - 2, Y + 50)
box(o, 450, 380, 170, 90, "Watchdog", "alerts me", *AMBER)
arrow(o, 535, Y + H, 535, 378)
text(o, 650, 520, "Solid: data, one way. Dashed: requests. Raw data stays private.", 16, SUB, ital=True)
svg("market-lab-architecture-simple.svg", 1300, 550, o)

# 2. Current state vs future state.
o = []
text(o, 600, 50, "Market Lab: current vs future state", 26, bold=True)
text(o, 100, 130, "Today", 20, bold=True)
text(o, 100, 156, "on hiatus", 15, SUB, ital=True)
box(o, 180, 90, 240, 100, "Capture", "my computer, stopped", *GRAY)
box(o, 480, 90, 240, 100, "Private storage", "my computer", *GREEN)
box(o, 780, 90, 240, 100, "Backtests", "lab + rundowns", *BLUE)
arrow(o, 420, 140, 478, 140, color="#CBD5E1")
arrow(o, 720, 140, 778, 140, color="#CBD5E1")
text(o, 100, 300, "Planned", 20, bold=True)
box(o, 180, 250, 240, 100, "Capture", "AWS virtual machine", *BLUE, dash=True)
box(o, 480, 250, 240, 100, "Data lake", "Parquet, private", *GREEN, dash=True)
box(o, 780, 250, 240, 100, "Backtests", "unchanged", *BLUE)
arrow(o, 420, 300, 478, 300, dash=True)
arrow(o, 720, 300, 778, 300, dash=True)
text(o, 600, 400, "Capture and storage move to AWS. Review stays the same.", 16, SUB, ital=True)
svg("market-lab-current-vs-future.svg", 1200, 430, o)

# 3. Data lake (planned): zones and how backtests read it.
o = []
text(o, 650, 44, "Market Lab data lake (planned)", 26, bold=True)
box(o, 30, 200, 190, 100, "Capture buffer", "today's session", *BLUE)
box(o, 270, 200, 190, 100, "Compact", "after each session", *AMBER)
o.append('<rect x="510" y="80" width="330" height="360" rx="20" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="8 6"/>')
text(o, 675, 112, "Private lake", 18, SUB, bold=True)
box(o, 540, 135, 270, 110, "Raw zone", "optional, compressed", *GREEN, dash=True)
box(o, 540, 290, 270, 110, "Curated zone", "Parquet, by date", *GREEN, dash=True)
box(o, 890, 200, 170, 100, "Catalog", "versioned schemas", *GRAY, dash=True)
box(o, 1110, 90, 170, 90, "Backtests", "lab engine", *BLUE)
box(o, 1110, 205, 170, 90, "SQL", "cross-day queries", *BLUE)
box(o, 1110, 320, 170, 90, "Local copy", "fast iteration", *BLUE)
arrow(o, 220, 250, 268, 250)
arrow(o, 460, 235, 538, 190, dash=True)
arrow(o, 460, 265, 538, 345, dash=True)
arrow(o, 810, 345, 888, 270, dash=True)
arrow(o, 1060, 230, 1108, 135, dash=True)
arrow(o, 1060, 250, 1108, 250, dash=True)
arrow(o, 1060, 270, 1108, 365, dash=True)
text(o, 650, 500, "Writers and readers use separate roles. Public access blocked. Encrypted at rest.", 16, SUB, ital=True)
svg("market-lab-data-lake.svg", 1310, 530, o)
