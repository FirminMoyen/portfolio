"""Export the Claude Design artboards in scripts/diagrams/src/ to static SVGs (docs/architecture.md §11.6).

Each source is an artboard copied from the private Claude Design canvas: one
absolutely positioned root holding bands, cards, labels and arrow <svg>s.
For every `<name>.<lang>.dc.html` this writes `assets/diagrams/<name>.<lang>.light.svg`
and `.dark.svg`.

Usage: python3 scripts/diagrams/render.py
"""
import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "diagrams" / "src"
OUT = ROOT / "assets" / "diagrams"

FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

# Light colours used on the canvas, and their dark-theme counterpart.
DARK = {
    "#ffffff": "#1d1e20", "#1f2328": "#e6edf3", "#57606a": "#9da7b3", "#0969da": "#4493f8",
    "#8c959f": "#6e7681", "#f6f8fa": "#24272b", "#d0d7de": "#3d444d", "#eef4fb": "#1f2a37",
    "#b6d0ee": "#2f4a6b", "#0550ae": "#79b8ff",
}


def style_of(attrs):
    out = {}
    for part in (attrs.get("style") or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def px(value, default=0.0):
    m = re.match(r"(-?[\d.]+)", value or "")
    return float(m.group(1)) if m else default


class Artboard(HTMLParser):
    """Collects the root's direct children: divs (with their inner HTML) and svgs (raw)."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.depth = 0
        self.root = None
        self.items = []
        self.current = None
        self.raw = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        text = self.get_starttag_text()
        if self.root is None:
            if tag == "div" and "position: relative" in (attrs.get("style") or ""):
                self.root = style_of(attrs)
                self.depth = 1
            return
        if self.depth == 1 and tag in ("div", "svg"):
            self.current = {"tag": tag, "style": style_of(attrs), "attrs": attrs}
            self.raw = [text]
        elif self.current is not None:
            self.raw.append(text)
        if tag not in ("br", "path") or not text.endswith("/>"):
            if tag not in ("br",):
                self.depth += 1

    def handle_startendtag(self, tag, attrs):
        if self.current is not None:
            self.raw.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.root is None or self.depth == 0:
            return
        if tag == "br":
            return
        self.depth -= 1
        if self.current is not None:
            self.raw.append(f"</{tag}>")
            if self.depth == 1:
                self.current["raw"] = "".join(self.raw)
                self.items.append(self.current)
                self.current = None
        if self.depth == 0:
            self.root_closed = True

    def handle_data(self, data):
        if self.current is not None:
            self.raw.append(data)

    def handle_entityref(self, name):
        if self.current is not None:
            self.raw.append(f"&{name};")

    def handle_charref(self, name):
        if self.current is not None:
            self.raw.append(f"&#{name};")


def inner(raw):
    return raw[raw.index(">") + 1: raw.rindex("<")]


def lines_of(markup):
    """Split a card label into (text, bold) lines on <br>."""
    markup = re.sub(r"^\s*<span>|</span>\s*$", "", markup.strip())
    out = []
    for part in re.split(r"<br\s*/?>", markup):
        bold = "<b>" in part
        text = html.unescape(re.sub(r"<[^>]+>", "", part)).strip()
        out.append((text, bold))
    return out


def wrap(text, width, size, bold):
    """Greedy word wrap with an average glyph width; the canvas wraps the same way."""
    if not text:
        return [""]
    per = size * (0.55 if bold else 0.5)
    limit = max(1, int(width / per))
    words, rows, row = text.split(" "), [], ""
    for w in words:
        cand = f"{row} {w}".strip()
        if len(cand) > limit and row:
            rows.append(row)
            row = w
        else:
            row = cand
    rows.append(row)
    return rows


def esc(text):
    return html.escape(text, quote=False)


def colour(value, theme):
    value = (value or "").lower()
    return DARK.get(value, value) if theme == "dark" else value


def render(path, theme):
    board = Artboard()
    board.feed(path.read_text(encoding="utf-8"))
    w, h = px(board.root["width"]), px(board.root["height"])
    title = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8")).group(1)
    ink = colour(board.root.get("color", "#1f2328"), theme)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}" '
        f'role="img" aria-label="{html.escape(html.unescape(title))}" font-family="{FONT}">',
        f'<title>{esc(html.unescape(title))}</title>',
        f'<rect width="{w:g}" height="{h:g}" fill="{colour(board.root.get("background", "#ffffff"), theme)}"/>',
    ]
    for item in board.items:
        s = item["style"]
        x, y = px(s.get("left")), px(s.get("top"))
        if item["tag"] == "svg":
            raw = item["raw"]
            for light, dark in DARK.items():
                if theme == "dark":
                    raw = re.sub(re.escape(light), dark, raw, flags=re.I)
            raw = re.sub(r'\sstyle="[^"]*"', lambda m: _svg_style(m.group(0)), raw, count=1)
            raw = raw.replace("<svg ", f'<svg x="{x:g}" y="{y:g}" overflow="visible" ', 1)
            out.append(raw)
            continue
        body = inner(item["raw"]).strip()
        size = px(s.get("font-size"), 15)
        lh = px(s.get("line-height"), 20 if size == 15 else size * 1.25)
        fg = colour(s.get("color", ink), theme)
        weight = s.get("font-weight", "")
        if "height" in s:
            bw, bh = px(s.get("width")), px(s.get("height"))
            fill = s.get("background")
            border = s.get("border", "")
            radius = px(s.get("border-radius"))
            if fill or border:
                stroke_w = px(border.split(" ")[0], 1) if border else 0
                stroke_c = colour(border.split(" ")[-1], theme) if border else "none"
                dash = ' stroke-dasharray="6 4"' if "dashed" in border else ""
                out.append(f'<rect x="{x:g}" y="{y:g}" width="{bw:g}" height="{bh:g}" rx="{radius:g}" '
                           f'fill="{colour(fill, theme) if fill else "none"}" stroke="{stroke_c}" '
                           f'stroke-width="{stroke_w:g}"{dash}/>')
            if not body:
                continue
            pad = px(s.get("padding"), 8)
            rows = []
            for text, bold in lines_of(body):
                rows += [(r, bold) for r in wrap(text, bw - 2 * pad, size, bold)]
            first = y + bh / 2 - len(rows) * lh / 2 + (lh - size) / 2 + size * 0.8
            for i, (text, bold) in enumerate(rows):
                fw = ' font-weight="700"' if bold else ""
                out.append(f'<text x="{x + bw / 2:g}" y="{first + i * lh:.1f}" text-anchor="middle" '
                           f'font-size="{size:g}"{fw} fill="{fg}">{esc(text)}</text>')
            continue
        text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        bw = px(s.get("width")) if "width" in s else None
        centred = s.get("text-align") == "center" and bw
        rows = wrap(text, bw, size, bool(weight)) if bw else [text]
        anchor = ' text-anchor="middle"' if centred else ""
        tx = x + bw / 2 if centred else x
        fw = f' font-weight="{weight}"' if weight else ""
        base = y + (lh - size) / 2 + size * 0.8
        for i, row in enumerate(rows):
            out.append(f'<text x="{tx:g}" y="{base + i * lh:.1f}"{anchor} font-size="{size:g}"{fw} '
                       f'fill="{fg}">{esc(row)}</text>')
    out.append("</svg>\n")
    return "\n".join(out)


def _svg_style(attr):
    """Keep only the presentation properties of an arrow's style attribute."""
    keep = []
    for part in attr.split('"')[1].split(";"):
        if ":" not in part:
            continue
        k, v = (p.strip() for p in part.split(":", 1))
        if k in ("fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "stroke-dasharray"):
            keep.append(f"{k}: {v}")
    return f' style="{"; ".join(keep)}"'


if __name__ == "__main__":
    for src in sorted(SRC.glob("*.dc.html")):
        name = src.name[: -len(".dc.html")]
        for theme in ("light", "dark"):
            (OUT / f"{name}.{theme}.svg").write_text(render(src, theme), encoding="utf-8")
            print(f"assets/diagrams/{name}.{theme}.svg")
