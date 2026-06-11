"""AI plan agent — an LLM iteratively rewrites the .plan file with visual
feedback until it is happy (or hits the iteration cap).

The sandbox is the whole point: the model controls ONLY the plan text.
Every proposal is parsed, validated (each device exactly once), realized
deterministically, routed, VERIFIED, and scored. A hallucinated plan is
rejected with a named error that is fed back to the model; a valid one
is written to the .plan file — which the live editor view re-renders,
so the human watches every iteration in real time.

API: OpenAI-compatible chat completions (api key via OPENAI_API_KEY or
the editor UI; base_url/model editable, so any compatible endpoint works).
"""
from __future__ import annotations

import base64
import json
import os
import re
import threading
import urllib.error
import urllib.request

SYSTEM = """You are an expert analog IC designer arranging a schematic.
You control a .plan file — a placement-intent language. You NEVER place
coordinates; you describe structure and narrative, and a deterministic
engine draws it. Syntax:

  plan NAME from NETLIST grid 1mm
  mirror NAME = DEV DEV ...                 # gate-tied mirror bank, L->R
  core5t NAME = pair(A B) tail(T) loads(L1 L2) diode(D)
  pair  NAME = pair(A B) tail(T)
  diode-link = DEV ...                      # diode-connected FETs
  lateral = DEV ...                         # drawn horizontal (switches)
  flow                                      # regions LEFT->RIGHT
    region "Title" ITEM ITEM ...            # ITEM = group name or [col]
                                            # [A B C] = column, TOP->BOTTOM
  orient DEV R90|MX|R0
  shift  DEV dx dy                          # grid units, small nudges only

Rules:
- every device must appear exactly once across groups-in-flow + columns
- columns read VDD side (top) to GND side (bottom)
- good schematics: signal flows left->right (bias first, outputs right),
  related structures grouped, few wire crossings, short wires, compact
- the engine reports score (wirelength/bends/crossings) and a VERIFIED
  flag; lower score numbers are better, VERIFIED must stay true

Each turn you receive the netlist, the current plan, the score, any
error, and a rendered IMAGE of the schematic. Respond with EITHER the
complete improved .plan file in a ```plan fenced block, OR exactly the
word DONE if the schematic is good and further edits won't help."""


def chat(base_url: str, api_key: str, model: str, messages: list) -> str:
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps({"model": model, "messages": messages}).encode(),
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        out = json.loads(r.read().decode("utf-8"))
    return out["choices"][0]["message"]["content"]


def _extract_plan(reply: str) -> str | None:
    m = re.search(r"```(?:plan)?\s*\n(.*?)```", reply, re.S)
    if m:
        return m.group(1).strip() + "\n"
    if reply.strip().lower().startswith("plan "):
        return reply.strip() + "\n"
    return None


class AgentRun(threading.Thread):
    def __init__(self, state, goal: str, model: str, base_url: str,
                 api_key: str, max_iters: int = 6):
        super().__init__(daemon=True)
        self.state = state
        self.goal = goal
        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1"
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.max_iters = max(1, min(12, max_iters))
        self.log: list[str] = []
        self.running = True
        self.stop_flag = False
        self.iter = 0

    def say(self, msg: str) -> None:
        self.log.append(msg)

    # ---------------------------------------------------------------
    def run(self) -> None:
        try:
            self._run()
        except Exception as exc:
            self.say(f"agent crashed: {type(exc).__name__}: {exc}")
        finally:
            self.running = False

    def _run(self) -> None:
        from .render_svg import render_sheet
        from .score import score
        from .snapshot import svg_to_png_bytes

        if not self.api_key:
            self.say("no API key — set OPENAI_API_KEY or paste one in the "
                     "agent panel")
            return
        with open(self.state.path, encoding="utf-8") as fh:
            netlist = fh.read()
        if len(netlist) > 20000:
            netlist = netlist[:20000] + "\n* (truncated)"

        feedback = ""
        for self.iter in range(1, self.max_iters + 1):
            if self.stop_flag:
                self.say("stopped by user")
                return
            # ---- current state of the plan, fully realized + scored
            plan_text = self.state.plan_text()
            try:
                sub, sheet, routing, verdict = self.state.build(None)
                sc = score(sheet, routing)
                status = (f"score: wirelength={sc.wirelength} "
                          f"bends={sc.bends} crossings={sc.crossings} | "
                          f"verified={verdict.ok}")
                svg = render_sheet(sheet, routing, verdict,
                                   {"path": "", "date": ""})
                png = svg_to_png_bytes(svg)
            except (ValueError, KeyError) as exc:
                status = f"PLAN INVALID: {exc}"
                png = None
            self.say(f"iter {self.iter}/{self.max_iters} — {status}")

            goal = self.goal or ("make this schematic as readable as a "
                                 "hand-drawn one")
            user_content = [{"type": "text", "text":
                             f"GOAL: {goal}\n\n"
                             f"NETLIST:\n{netlist}\n\n"
                             f"CURRENT PLAN:\n{plan_text}\n\n"
                             f"ENGINE STATUS: {status}\n{feedback}"}]
            if png is not None:
                user_content.append(
                    {"type": "image_url", "image_url": {"url":
                     "data:image/png;base64," +
                     base64.b64encode(png).decode()}})
            else:
                user_content[0]["text"] += \
                    "\n(no image available this round — use the score)"

            try:
                reply = chat(self.base_url, self.api_key, self.model,
                             [{"role": "system", "content": SYSTEM},
                              {"role": "user", "content": user_content}])
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", "replace")[:300]
                self.say(f"API error {exc.code}: {body}")
                return
            except (urllib.error.URLError, TimeoutError) as exc:
                self.say(f"API unreachable: {exc}")
                return

            if reply.strip().upper().startswith("DONE"):
                self.say(f"agent is happy after {self.iter - 1} edit(s) — DONE")
                return
            new_plan = _extract_plan(reply)
            if new_plan is None:
                feedback = ("FEEDBACK: your last reply was not a fenced "
                            "```plan block or DONE. Reply correctly.")
                self.say("reply had no plan block — asking again")
                continue

            # ---- sandbox: validate before letting it touch the file
            from .parser import parse_file
            from .classify import classify_design
            from .plan import parse_plan, realize_plan
            try:
                p = parse_plan(new_plan)
                fresh = parse_file(self.state.path)
                classify_design(fresh)
                realize_plan(fresh.subckts[p.name or self.state.subname], p)
            except (ValueError, KeyError) as exc:
                feedback = (f"FEEDBACK: your plan was REJECTED: {exc}. "
                            "Fix it — every device exactly once.")
                self.say(f"proposal rejected: {exc}")
                continue

            with open(self.state.plan_path, "w", encoding="utf-8") as fh:
                fh.write(new_plan)
            feedback = "FEEDBACK: plan applied. Improve further or say DONE."
            self.say("plan applied — editor view updated")
        self.say("iteration cap reached")
