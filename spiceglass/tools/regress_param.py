""".param + expression-evaluation gate (E2).

  EP1 .param resolved (with SI suffixes): wb=2u -> 2e-6, mult=3.
  EP2 device expressions evaluated: w='2*wb' -> 4u, l={wb+1u} -> 3u.
  EP3 nested param refs: b='2*a' with a=2u -> 4u.
  EP4 unresolved expr left verbatim (no crash).
  EP5 plain numbers untouched: w=4u stays "4u".

    python tools/regress_param.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".."))

from glass.engine.parser import parse_text                 # noqa: E402

DECK = """* param eval gate
.param wb=2u
.param mult=3
.param a=2u
.param b='2*a'
.subckt blk d g s
M1 d g s s nmos w='2*wb' l={wb+1u} m=mult
M2 d g s s nmos w=4u l=0.5u
M3 d g s s nmos w='2*undefinedp' l=1u
MB d g s s nmos w='b' l=1u
.ends
"""


def main() -> int:
    d = parse_text(DECK)
    fails = []
    devs = {x.name: x for x in d.subckts["blk"].devices}

    def chk(dev, key, want, gate):
        got = devs[dev].params.get(key)
        if got != want:
            fails.append((gate, f"{dev}.{key} = {got!r}, want {want!r}"))

    # EP1 (params resolved) is exercised through EP2/EP3 device evals
    chk("M1", "w", "4u", "EP2")          # 2*2u
    chk("M1", "l", "3u", "EP2")          # 2u + 1u
    chk("M1", "m", "3", "EP1")           # mult=3
    chk("MB", "w", "4u", "EP3")          # b = 2*a = 2*2u
    chk("M2", "w", "4u", "EP5")          # plain, untouched
    chk("M2", "l", "0.5u", "EP5")
    # EP4 unresolved -> verbatim
    if devs["M3"].params.get("w") != "'2*undefinedp'":
        fails.append(("EP4", f"M3.w should stay verbatim, got "
                             f"{devs['M3'].params.get('w')!r}"))

    if fails:
        print(f"FAIL ({len(fails)}):")
        for g, m in fails:
            print(f"  [{g}] {m}")
        return 1
    print("PASS — EP1 params, EP2 device exprs (w=4u,l=3u), EP3 nested refs, "
          "EP4 unresolved verbatim, EP5 plain untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
