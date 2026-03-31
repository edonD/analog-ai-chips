"""Shared library for generating xschem .sch files with SKY130 PDK symbols.
Follows the exact format of mode_control_2_comparators.sch."""

PDK = "/home/ubuntu/.volare/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.tech/xschem/sky130_fd_pr"
XLIB = "/usr/share/xschem/xschem_library/devices"

class Schematic:
    def __init__(self):
        self.lines = []
        self._pc = 0  # pin counter
        self._lc = 0  # label counter

    def _pn(self):
        self._pc += 1; return f"p{self._pc}"
    def _ln(self):
        self._lc += 1; return f"lb{self._lc}"

    # -- primitives --
    def T(self, text, x, y, rot=0, flip=0, xm=0.4, ym=0.4, attrs=""):
        self.lines.append(f'T {{{text}}} {x} {y} {rot} {flip} {xm} {ym} {{{attrs}}}')

    def N(self, x1, y1, x2, y2, lab=""):
        a = f"lab={lab}" if lab else ""
        self.lines.append(f'N {x1} {y1} {x2} {y2} {{{a}}}')

    def C(self, sym, x, y, rot=0, flip=0, attrs=""):
        self.lines.append(f'C {{{sym}}} {x} {y} {rot} {flip} {{{attrs}}}')

    def L(self, layer, x1, y1, x2, y2, attrs=""):
        self.lines.append(f'L {layer} {x1} {y1} {x2} {y2} {{{attrs}}}')

    def comment(self, text):
        self.lines.append(f"* {text}")

    def blank(self):
        self.lines.append("")

    # -- lab_pin: label a wire endpoint --
    def lab(self, x, y, rot, name):
        self.C(f"{XLIB}/lab_pin.sym", x, y, rot, 0,
               f"name={self._ln()} sig_type=std_logic lab={name}")

    # -- header --
    def header(self, title, subtitle, info, author):
        self.lines.append("v {xschem version=3.4.6 file_version=1.2}")
        self.lines.append("G {}")
        self.lines.append('K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}')
        self.lines.append("V {}")
        self.lines.append("S {}")
        self.lines.append("E {}")
        self.blank()
        self.T(title, -300, -1200, xm=0.85, ym=0.85, attrs="layer=4")
        self.T(subtitle, -300, -1130, xm=0.45, ym=0.45, attrs="layer=8")
        self.T("PVDD 5.0V LDO Regulator  |  SkyWater SKY130A", -300, -1095, xm=0.3, ym=0.3)
        self.T(info, -300, -1065, xm=0.28, ym=0.28, attrs="layer=13")
        self.C(f"{XLIB}/title.sym", -300, 600, 0, 0,
               f'name=l1 author="{author}"')
        self.blank()

    # -- port pins --
    def ipin(self, x, y, name):
        self.C(f"{XLIB}/ipin.sym", x, y, 0, 0, f"name={self._pn()} lab={name}")
    def opin(self, x, y, name):
        self.C(f"{XLIB}/opin.sym", x, y, 0, 0, f"name={self._pn()} lab={name}")
    def iopin(self, x, y, name):
        self.C(f"{XLIB}/iopin.sym", x, y, 0, 0, f"name={self._pn()} lab={name}")

    # -- dashed rect --
    def rect_dash(self, x1, y1, x2, y2, layer=8):
        for a in [(x1,y1,x2,y1),(x2,y1,x2,y2),(x2,y2,x1,y2),(x1,y2,x1,y1)]:
            self.L(layer, *a, "dash=5")

    # ================================================================
    # MOSFET placement — matches mode_control_2_comparators.sch exactly
    # cx,cy = position for C element (symbol placed at cx, cy)
    # Pin offsets from (cx, cy):
    #   gate:   (cx-20, cy)   — extends left
    #   bulk:   (cx+20, cy)   — extends right
    #   top:    (cx+20, cy-30) — PFET=source, NFET=drain
    #   bottom: (cx+20, cy+30) — PFET=drain, NFET=source
    # ================================================================
    def _sym_path(self, kind):
        return {
            "ph": f"{PDK}/pfet_g5v0d10v5.sym",
            "nh": f"{PDK}/nfet_g5v0d10v5.sym",
            "p18": f"{PDK}/pfet_01v8.sym",
            "n18": f"{PDK}/nfet_01v8.sym",
        }[kind]

    def _model(self, kind):
        return {"ph":"pfet_g5v0d10v5","nh":"nfet_g5v0d10v5",
                "p18":"pfet_01v8","n18":"nfet_01v8"}[kind]

    def fet(self, name, kind, cx, cy, d, g, s, b, w, l, m=1):
        """Place a MOSFET with full wiring, labels, and annotation.
        For PFET: top=S, bottom=D. For NFET: top=D, bottom=S."""
        is_p = kind in ("ph", "p18")
        sym = self._sym_path(kind)
        model = self._model(kind)
        mult = f" mult={m}" if m > 1 else " mult=1"

        # Symbol
        self.C(sym, cx, cy, 0, 0,
               f"name={name} L={l} W={w} nf=1{mult} model={model} spiceprefix=X")

        # Annotation
        ptype = "P" if is_p else "N"
        wl = f"{ptype}: W={w} L={l}" + (f" m={m}" if m > 1 else "")
        self.T(name, cx - 25, cy - 50, xm=0.22, ym=0.22, attrs="layer=13")
        self.T(wl, cx - 25, cy - 35, xm=0.18, ym=0.18, attrs="layer=5")

        top_net = s if is_p else d
        bot_net = d if is_p else s

        # Gate — wire left, label
        self.N(cx - 20, cy, cx - 60, cy, lab=g)
        self.lab(cx - 60, cy, 0, g)

        # Bulk — wire right, label
        self.N(cx + 20, cy, cx + 50, cy, lab=b)
        self.lab(cx + 50, cy, 2, b)

        # Top — wire up, label
        self.N(cx + 20, cy - 30, cx + 20, cy - 70, lab=top_net)
        self.lab(cx + 20, cy - 70, 2, top_net)

        # Bottom — wire down, label
        self.N(cx + 20, cy + 30, cx + 20, cy + 70, lab=bot_net)
        self.lab(cx + 20, cy + 70, 2, bot_net)

    def fet_stacked(self, name, kind, cx, cy, d, g, s, b, w, l, m=1,
                    wire_top=None, wire_bot=None, wire_gate=None,
                    top_len=70, bot_len=70, gate_len=60):
        """Place FET with optional explicit wire targets instead of lab_pin.
        wire_top/bot/gate: if (x,y) tuple, draw wire to there; else use lab_pin."""
        is_p = kind in ("ph", "p18")
        sym = self._sym_path(kind)
        model = self._model(kind)
        mult = f" mult={m}" if m > 1 else " mult=1"
        self.C(sym, cx, cy, 0, 0,
               f"name={name} L={l} W={w} nf=1{mult} model={model} spiceprefix=X")

        ptype = "P" if is_p else "N"
        wl = f"{ptype}: W={w} L={l}" + (f" m={m}" if m > 1 else "")
        self.T(name, cx - 25, cy - 50, xm=0.22, ym=0.22, attrs="layer=13")
        self.T(wl, cx - 25, cy - 35, xm=0.18, ym=0.18, attrs="layer=5")

        top_net = s if is_p else d
        bot_net = d if is_p else s

        # Gate
        if wire_gate:
            self.N(cx - 20, cy, wire_gate[0], wire_gate[1], lab=g)
        else:
            self.N(cx - 20, cy, cx - gate_len, cy, lab=g)
            self.lab(cx - gate_len, cy, 0, g)

        # Bulk
        self.N(cx + 20, cy, cx + 50, cy, lab=b)
        self.lab(cx + 50, cy, 2, b)

        # Top
        if wire_top:
            self.N(cx + 20, cy - 30, wire_top[0], wire_top[1], lab=top_net)
        else:
            self.N(cx + 20, cy - 30, cx + 20, cy - top_len, lab=top_net)
            self.lab(cx + 20, cy - top_len, 2, top_net)

        # Bottom
        if wire_bot:
            self.N(cx + 20, cy + 30, wire_bot[0], wire_bot[1], lab=bot_net)
        else:
            self.N(cx + 20, cy + 30, cx + 20, cy + bot_len, lab=bot_net)
            self.lab(cx + 20, cy + bot_len, 2, bot_net)

    # ================================================================
    # PDK Resistor (res_xhigh_po) — 3 pins: P(top), M(bottom), B(body)
    # ================================================================
    def rxh(self, name, cx, cy, p, m_net, b, w, l):
        self.C(f"{PDK}/res_xhigh_po.sym", cx, cy, 0, 0,
               f"name={name} W={w} L={l} model=res_xhigh_po spiceprefix=X")
        self.T(name, cx + 20, cy - 25, xm=0.2, ym=0.2, attrs="layer=13")
        self.T(f"W={w} L={l}", cx + 20, cy + 10, xm=0.17, ym=0.17, attrs="layer=5")
        self.N(cx, cy - 30, cx, cy - 65, lab=p)
        self.lab(cx, cy - 65, 2, p)
        self.N(cx, cy + 30, cx, cy + 65, lab=m_net)
        self.lab(cx, cy + 65, 2, m_net)
        self.N(cx - 20, cy, cx - 45, cy, lab=b)
        self.lab(cx - 45, cy, 0, b)

    # ================================================================
    # MIM Cap (cap_mim_m3_1) — 2 pins: c0(top), c1(bottom)
    # ================================================================
    def mim(self, name, cx, cy, c0, c1, w, l, mf=1):
        self.C(f"{PDK}/cap_mim_m3_1.sym", cx, cy, 0, 0,
               f"name={name} W={w} L={l} MF={mf} model=cap_mim_m3_1 spiceprefix=X")
        self.T(name, cx + 20, cy - 25, xm=0.2, ym=0.2, attrs="layer=13")
        self.T(f"{w}x{l}", cx + 20, cy + 10, xm=0.17, ym=0.17, attrs="layer=5")
        self.N(cx, cy - 30, cx, cy - 65, lab=c0)
        self.lab(cx, cy - 65, 2, c0)
        self.N(cx, cy + 30, cx, cy + 65, lab=c1)
        self.lab(cx, cy + 65, 2, c1)

    # ================================================================
    # Bare R / C (ideal SPICE elements)
    # ================================================================
    def bare_R(self, name, cx, cy, n1, n2, val):
        self.C(f"{XLIB}/res.sym", cx, cy, 0, 0, f"name={name} value={val}")
        self.T(name, cx + 20, cy - 20, xm=0.2, ym=0.2, attrs="layer=13")
        self.T(val, cx + 20, cy + 8, xm=0.18, ym=0.18, attrs="layer=5")
        self.N(cx, cy - 30, cx, cy - 65, lab=n1)
        self.lab(cx, cy - 65, 2, n1)
        self.N(cx, cy + 30, cx, cy + 65, lab=n2)
        self.lab(cx, cy + 65, 2, n2)

    def bare_C(self, name, cx, cy, n1, n2, val):
        self.C(f"{XLIB}/capa.sym", cx, cy, 0, 0, f"name={name} value={val}")
        self.T(name, cx + 20, cy - 20, xm=0.2, ym=0.2, attrs="layer=13")
        self.T(val, cx + 20, cy + 8, xm=0.18, ym=0.18, attrs="layer=5")
        self.N(cx, cy - 30, cx, cy - 65, lab=n1)
        self.lab(cx, cy - 65, 2, n1)
        self.N(cx, cy + 30, cx, cy + 65, lab=n2)
        self.lab(cx, cy + 65, 2, n2)

    # -- net label on a wire (no pin, just text) --
    def net_text(self, name, x, y, layer=8):
        self.T(name, x, y, xm=0.28, ym=0.28, attrs=f"layer={layer}")

    # -- section header inside a schematic --
    def section(self, title, x, y, layer=4):
        self.comment("=" * 60)
        self.comment(title)
        self.comment("=" * 60)
        self.T(title, x, y, xm=0.35, ym=0.35, attrs=f"layer={layer}")

    # -- write to file --
    def write(self, path):
        with open(path, "w") as f:
            f.write("\n".join(self.lines) + "\n")
        print(f"  Written {path} ({len(self.lines)} lines)")
