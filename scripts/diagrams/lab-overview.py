"""Export the lab-overview diagram validated in Claude Design to static SVGs (docs/architecture.md §11.6).

Usage: python3 scripts/diagrams/lab-overview.py assets/diagrams
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1])

THEMES = {
    "light": dict(bg="#ffffff", ink="#1f2328", muted="#57606a", accent="#0969da", planned="#8c959f",
                  lab="#f6f8fa", labline="#d0d7de", host="#eef4fb", hostline="#b6d0ee", hostlabel="#0550ae",
                  card="#ffffff", arrow="#57606a"),
    "dark": dict(bg="#1d1e20", ink="#e6edf3", muted="#9da7b3", accent="#4493f8", planned="#6e7681",
                 lab="#24272b", labline="#3d444d", host="#1f2a37", hostline="#2f4a6b", hostlabel="#79b8ff",
                 card="#1d1e20", arrow="#9da7b3"),
}

TEXT = {
    "fr": dict(
        title="Vue d'ensemble du lab", subtitle="Homelab reconstruit de zéro · état au 25 octobre 2026",
        lab="Lab · 10.42.0.0/16 · isolé du réseau domestique",
        host="Hermes (pve1) · Dell Latitude 7490 · Proxmox VE 9.2",
        devices=("Mes appareils", ["client VPN"]),
        tailscale=("Tailscale", ["subnet router", "plugin OPNsense"]),
        opnsense=("OPNsense (fw-01)", ["VM : pare-feu et routeur"]),
        switch=("sw-01", ["switch dédié au lab"]),
        atlas=("Atlas (pve2)", ["Dell XPS 15 · workloads", "prévu"]),
        zone0=("10.42.0.0/24", ["infrastructure physique"]),
        zones=("10.42.10.0/24, 10.42.20.0/24…", ["zones à venir · VLAN = 3ᵉ octet"]),
        home=("Réseau domestique", ["hors du lab, jamais", "accessible par le VPN"]),
        tunnel="tunnel chiffré", lan="LAN du lab", exposed="Rien n'est exposé sur Internet.",
        running="En service", planned="Prévu",
        desc="Schéma du lab : mes appareils rejoignent par un tunnel chiffré Tailscale, sur OPNsense dans Hermes ; "
             "OPNsense dessert le switch sw-01 et Atlas (prévu) ; réseau 10.42.0.0/16 isolé du réseau domestique.",
    ),
    "en": dict(
        title="Lab overview", subtitle="Homelab rebuilt from scratch · as of 25 October 2026",
        lab="Lab · 10.42.0.0/16 · isolated from the home network",
        host="Hermes (pve1) · Dell Latitude 7490 · Proxmox VE 9.2",
        devices=("My devices", ["VPN client"]),
        tailscale=("Tailscale", ["subnet router", "OPNsense plugin"]),
        opnsense=("OPNsense (fw-01)", ["VM: firewall and router"]),
        switch=("sw-01", ["switch dedicated to the lab"]),
        atlas=("Atlas (pve2)", ["Dell XPS 15 · workloads", "planned"]),
        zone0=("10.42.0.0/24", ["physical infrastructure"]),
        zones=("10.42.10.0/24, 10.42.20.0/24…", ["upcoming zones · VLAN = 3rd octet"]),
        home=("Home network", ["outside the lab, never", "reachable through the VPN"]),
        tunnel="encrypted tunnel", lan="lab LAN", exposed="Nothing is exposed to the internet.",
        running="In service", planned="Planned",
        desc="Lab diagram: my devices connect through an encrypted Tailscale tunnel to OPNsense on Hermes; "
             "OPNsense serves the sw-01 switch and Atlas (planned); the 10.42.0.0/16 network is isolated from the home network.",
    ),
}

FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def card(x, y, w, h, label, c, planned=False, home=False):
    title, lines = label
    if home:
        fill, stroke, dash, color, sw = c["lab"], c["labline"], "", c["muted"], 1
    elif planned:
        fill, stroke, dash, color, sw = c["card"], c["planned"], ' stroke-dasharray="6 4"', c["muted"], 1.5
    else:
        fill, stroke, dash, color, sw = c["card"], c["accent"], "", c["ink"], 1.5
    rows = [(title, True)] + [(l, False) for l in lines]
    top = y + h / 2 - (len(rows) * 20) / 2 + 15
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>']
    for i, (t, bold) in enumerate(rows):
        weight = ' font-weight="700"' if bold else ""
        fc = color if bold or home or planned else c["ink"]
        out.append(f'<text x="{x + w / 2}" y="{top + i * 20:.0f}" text-anchor="middle" font-size="15"{weight} fill="{fc}">{escape(t)}</text>')
    return "\n".join(out)


def arrow(x1, y1, x2, y2, color, dashed=False, mid="a"):
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" stroke-linecap="round"{dash} marker-end="url(#{mid})"/>')


def render(lang, theme):
    t, c = TEXT[lang], THEMES[theme]
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="760" viewBox="0 0 1280 760" role="img" aria-labelledby="t d" font-family="{FONT}">')
    p.append(f'<title id="t">{escape(t["title"])}</title><desc id="d">{escape(t["desc"])}</desc>')
    p.append("<defs>")
    for mid, col in (("a", c["arrow"]), ("p", c["planned"])):
        p.append(f'<marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" fill="{col}"/></marker>')
    p.append("</defs>")
    p.append(f'<rect width="1280" height="760" fill="{c["bg"]}"/>')
    p.append(f'<rect x="360" y="160" width="856" height="536" rx="16" fill="{c["lab"]}" stroke="{c["labline"]}"/>')
    p.append(f'<rect x="392" y="216" width="792" height="184" rx="12" fill="{c["host"]}" stroke="{c["hostline"]}"/>')
    p.append(arrow(280, 308, 419, 308, c["arrow"]))
    p.append(arrow(656, 308, 747, 308, c["arrow"]))
    p.append(arrow(868, 352, 868, 443, c["arrow"]))
    p.append(arrow(752, 492, 661, 492, c["planned"], dashed=True, mid="p"))
    p.append(f'<line x1="64" y1="632" x2="104" y2="632" stroke="{c["accent"]}" stroke-width="2"/>')
    p.append(f'<line x1="64" y1="664" x2="104" y2="664" stroke="{c["planned"]}" stroke-width="2" stroke-dasharray="6 6"/>')
    p.append(card(64, 264, 216, 88, t["devices"], c))
    p.append(card(424, 264, 232, 88, t["tailscale"], c))
    p.append(card(752, 264, 232, 88, t["opnsense"], c))
    p.append(card(752, 448, 232, 88, t["switch"], c))
    p.append(card(424, 448, 232, 88, t["atlas"], c, planned=True))
    p.append(card(424, 584, 344, 80, t["zone0"], c))
    p.append(card(800, 584, 384, 80, t["zones"], c, planned=True))
    p.append(card(64, 448, 216, 104, t["home"], c, home=True))
    p.append(f'<text x="64" y="84" font-size="30" font-weight="700" fill="{c["ink"]}">{escape(t["title"])}</text>')
    p.append(f'<text x="64" y="116" font-size="15" fill="{c["muted"]}">{escape(t["subtitle"])}</text>')
    p.append(f'<text x="384" y="192" font-size="14" font-weight="600" fill="{c["muted"]}">{escape(t["lab"])}</text>')
    p.append(f'<text x="416" y="244" font-size="14" font-weight="600" fill="{c["hostlabel"]}">{escape(t["host"])}</text>')
    p.append(f'<text x="352" y="292" text-anchor="middle" font-size="13" fill="{c["muted"]}">{escape(t["tunnel"])}</text>')
    p.append(f'<text x="880" y="404" font-size="13" fill="{c["muted"]}">{escape(t["lan"])}</text>')
    p.append(f'<text x="64" y="600" font-size="14" font-weight="600" fill="{c["ink"]}">{escape(t["exposed"])}</text>')
    p.append(f'<text x="116" y="636" font-size="13" fill="{c["muted"]}">{escape(t["running"])}</text>')
    p.append(f'<text x="116" y="668" font-size="13" fill="{c["muted"]}">{escape(t["planned"])}</text>')
    p.append("</svg>\n")
    return "\n".join(p)


for lang in TEXT:
    for theme in THEMES:
        (OUT / f"lab-overview.{lang}.{theme}.svg").write_text(render(lang, theme), encoding="utf-8")
