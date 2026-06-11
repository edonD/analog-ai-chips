# .asc test corpus — sources & licensing

The `asc/` folder holds third-party LTspice schematics used locally to
test the `.asc` reader/renderer. The files are **not committed**
(mixed/unclear licenses); re-fetch them with `fetch_corpus.ps1`.

| Source | License | Used for |
|---|---|---|
| [mick001/Circuits-LTSpice](https://github.com/mick001/Circuits-LTSpice) | none declared | ~131 educational circuits (amplifiers, rectifiers, power) |
| [jmfermun/XTR111-LTspice-Model](https://github.com/jmfermun/XTR111-LTspice-Model) | MIT | sheet + local .asy resolution test |
| [nunobrum/PyLTSpice](https://github.com/nunobrum/PyLTSpice) | GPL-3.0 | tool-generated test sheets, encoding variants |

Status (2026-06-11): **150/150 files parse and render without errors.**
Native LTspice symbols (res, cap, ind, diode, voltage, current,
npn/pnp, nmos/pmos, opamps) render via corpus-derived pin offsets
(`probe_pins.py` measured wire endpoints across all instances:
res (16,16)/(16,96) ×383, npn C(64,0) B(0,48) E(64,96) ×85, …).
Unknown symbols degrade to dashed boxes with named warnings.
