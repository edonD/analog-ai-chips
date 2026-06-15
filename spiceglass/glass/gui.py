"""SpiceGlass launcher GUI (Tkinter, stdlib only).

    python -m glass gui        (or double-click SpiceGlass.bat)

Pick a netlist (.cir/.spice) or a .plan, Start — the editor server runs
as a child process with its log shown here; buttons open the editor,
the algorithm view and the symbol designer in the browser.
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from tkinter import filedialog, ttk

PKG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.normpath(os.path.join(PKG_DIR, ".."))


def port_busy(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def discover() -> list[str]:
    """Plans, design netlists and .asc sheets worth one click."""
    out: list[str] = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if not d.startswith((".", "__"))
                   and d != "node_modules"]
        for f in files:
            if f.endswith((".plan", ".asc")) or \
               (f.endswith((".cir", ".spice")) and f.startswith("design")):
                out.append(os.path.relpath(os.path.join(root, f), REPO))
    return sorted(out, key=lambda p: (not p.endswith(".plan"),
                                      p.endswith(".asc"), p))


class Launcher:
    def __init__(self) -> None:
        self.proc: subprocess.Popen | None = None
        self.root = tk.Tk()
        self.root.title("SpiceGlass Launcher")
        self.root.geometry("760x560")
        self.root.configure(bg="#23262b")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".", background="#23262b", foreground="#dde1e8",
                        fieldbackground="#16181c")
        style.configure("TButton", background="#3d434d", padding=6)
        style.map("TButton", background=[("active", "#4a515d")])

        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=10, pady=8)
        ttk.Label(top, text="File (.cir / .spice / .plan):").pack(side="left")
        self.file_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.file_var, width=58)\
            .pack(side="left", padx=6, fill="x", expand=True)
        ttk.Button(top, text="Browse…", command=self.browse)\
            .pack(side="left")
        ttk.Label(top, text="  port").pack(side="left")
        self.port_var = tk.StringVar(value="8137")
        ttk.Entry(top, textvariable=self.port_var, width=6)\
            .pack(side="left")

        mid = ttk.Frame(self.root)
        mid.pack(fill="both", expand=False, padx=10)
        ttk.Label(mid, text="Discovered (double-click: .plan/.cir = select "
                            "for server, .asc = open live editor):")\
            .pack(anchor="w")
        self.listbox = tk.Listbox(mid, height=8, bg="#16181c", fg="#d8dee7",
                                  selectbackground="#3d5a86",
                                  font=("Consolas", 9))
        self.listbox.pack(fill="x")
        for item in discover():
            self.listbox.insert("end", item)
        self.listbox.bind("<Double-Button-1>", self.pick)

        btns = ttk.Frame(self.root)
        btns.pack(fill="x", padx=10, pady=8)
        self.start_btn = ttk.Button(btns, text="▶ Start server",
                                    command=self.start)
        self.start_btn.pack(side="left")
        ttk.Button(btns, text="■ Stop", command=self.stop)\
            .pack(side="left", padx=4)
        ttk.Button(btns, text="Open Editor",
                   command=lambda: self.open("/")).pack(side="left", padx=12)
        ttk.Button(btns, text="Algorithm view",
                   command=lambda: self.open("/algo")).pack(side="left")
        ttk.Button(btns, text="Symbol designer",
                   command=lambda: self.open("/symbols"))\
            .pack(side="left", padx=4)
        self.status = ttk.Label(btns, text="idle")
        self.status.pack(side="right")

        ttk.Label(self.root, text="Server log:").pack(anchor="w", padx=10)
        self.log = tk.Text(self.root, bg="#16181c", fg="#9fb6a3",
                           font=("Consolas", 9), state="disabled")
        self.log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ------------------------------------------------------------ actions
    def browse(self) -> None:
        f = filedialog.askopenfilename(
            initialdir=REPO,
            filetypes=[("netlists, plans & schematics",
                        "*.cir *.spice *.sp *.plan *.asc"),
                       ("all files", "*.*")])
        if f:
            self.file_var.set(f)
            if f.lower().endswith(".asc"):
                self.open_asc(f)

    def pick(self, _ev) -> None:
        sel = self.listbox.curselection()
        if not sel:
            return
        f = os.path.join(REPO, self.listbox.get(sel[0]))
        self.file_var.set(f)
        if f.lower().endswith(".asc"):
            self.open_asc(f)            # double-click .asc -> live editor

    def open_asc(self, file: str) -> None:
        """Launch the live .asc editor server and open it in the browser.

        Interchangeable text + graphics: edit either, both stay in sync."""
        port = int(self.port_var.get() or 8137)
        if self.proc is not None and self.proc.poll() is None:
            self.stop()
        if port_busy(port):
            self.say(f"port {port} busy — opening browser\n")
            self.open("/")
            return
        self.proc = subprocess.Popen(
            [sys.executable, "-m", "glass", "edit", file,
             "--port", str(port), "--no-browser"],
            cwd=PKG_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, creationflags=getattr(subprocess,
                                             "CREATE_NO_WINDOW", 0))
        threading.Thread(target=self._pump, daemon=True).start()
        self.status.configure(text=f"running :{port} (.asc)")
        self.root.after(1200, lambda: self.open("/"))

    def say(self, msg: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", msg)
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self) -> None:
        file = self.file_var.get().strip()
        port = int(self.port_var.get() or 8137)
        if not file:
            self.say("pick a file first\n")
            return
        if not os.path.exists(file):
            self.say(f"not found: {file}\n")
            return
        if file.lower().endswith(".asc"):
            self.open_asc(file)         # .asc -> live editor server
            return
        if self.proc is not None and self.proc.poll() is None:
            self.say("already running — Stop first\n")
            return
        if port_busy(port):
            self.say(f"port {port} already serving — opening browser\n")
            self.open("/")
            return
        self.proc = subprocess.Popen(
            [sys.executable, "-m", "glass", "edit", file,
             "--port", str(port), "--no-browser"],
            cwd=PKG_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, creationflags=getattr(subprocess,
                                             "CREATE_NO_WINDOW", 0))
        threading.Thread(target=self._pump, daemon=True).start()
        mode = "PLAN MODE" if file.lower().endswith(".plan") else "auto"
        self.status.configure(text=f"running :{port} ({mode})")
        self.root.after(1200, lambda: self.open("/"))

    def _pump(self) -> None:
        assert self.proc is not None and self.proc.stdout is not None
        for line in self.proc.stdout:
            self.root.after(0, self.say, line)
        self.root.after(0, self.say, "[server exited]\n")
        self.root.after(0, self.status.configure, {"text": "idle"})

    def stop(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            self.proc.terminate()
            self.say("stopped\n")
        self.status.configure(text="idle")

    def open(self, path: str) -> None:
        webbrowser.open(f"http://127.0.0.1:{int(self.port_var.get())}{path}")

    def close(self) -> None:
        self.stop()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    Launcher().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
