import tkinter as tk
from tkinter import font
import math

# ─── Color Theme ───────────────────────────────────────────────
BG        = "#1e1e2e"
BTN_NUM   = "#313244"
BTN_OP    = "#89b4fa"
BTN_EQ    = "#a6e3a1"
BTN_CLR   = "#f38ba8"
BTN_SPEC  = "#cba6f7"
TEXT_MAIN = "#cdd6f4"
TEXT_DIM  = "#6c7086"
HOVER_NUM = "#45475a"
HOVER_OP  = "#74c7ec"
HOVER_EQ  = "#81c8a0"
HOVER_CLR = "#e57575"
HOVER_SPEC= "#b4a0e8"

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.expression = ""
        self.result_shown = False
        self.history = []

        self._build_ui()

    # ── UI Builder ──────────────────────────────────────────────
    def _build_ui(self):
        main = tk.Frame(self.root, bg=BG, padx=16, pady=16)
        main.pack()

        # Title
        tk.Label(main, text="Calculator", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 11)).pack(anchor="w")

        # History label
        self.history_var = tk.StringVar(value="")
        tk.Label(main, textvariable=self.history_var, bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10), anchor="e", width=28).pack(fill="x")

        # Expression display
        self.expr_var = tk.StringVar(value="")
        tk.Label(main, textvariable=self.expr_var, bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 13), anchor="e", width=28).pack(fill="x")

        # Main display
        self.display_var = tk.StringVar(value="0")
        tk.Label(main, textvariable=self.display_var, bg=BG, fg=TEXT_MAIN,
                 font=("Segoe UI", 36, "bold"), anchor="e",
                 width=14).pack(fill="x", pady=(0, 12))

        # Separator
        tk.Frame(main, bg=TEXT_DIM, height=1).pack(fill="x", pady=(0, 12))

        # Button grid
        grid = tk.Frame(main, bg=BG)
        grid.pack()

        buttons = [
            # (label, row, col, colspan, bg, hover, cmd)
            ("C",    0, 0, 1, BTN_CLR,  HOVER_CLR,  lambda: self.clear()),
            ("⌫",   0, 1, 1, BTN_SPEC, HOVER_SPEC, lambda: self.backspace()),
            ("%",    0, 2, 1, BTN_SPEC, HOVER_SPEC, lambda: self.append("%")),
            ("÷",    0, 3, 1, BTN_OP,   HOVER_OP,   lambda: self.append("/")),

            ("7",    1, 0, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("7")),
            ("8",    1, 1, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("8")),
            ("9",    1, 2, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("9")),
            ("×",    1, 3, 1, BTN_OP,   HOVER_OP,   lambda: self.append("*")),

            ("4",    2, 0, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("4")),
            ("5",    2, 1, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("5")),
            ("6",    2, 2, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("6")),
            ("−",    2, 3, 1, BTN_OP,   HOVER_OP,   lambda: self.append("-")),

            ("1",    3, 0, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("1")),
            ("2",    3, 1, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("2")),
            ("3",    3, 2, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("3")),
            ("+",    3, 3, 1, BTN_OP,   HOVER_OP,   lambda: self.append("+")),

            ("√",    4, 0, 1, BTN_SPEC, HOVER_SPEC, lambda: self.sqrt()),
            ("0",    4, 1, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append("0")),
            (".",    4, 2, 1, BTN_NUM,  HOVER_NUM,  lambda: self.append(".")),
            ("=",    4, 3, 1, BTN_EQ,   HOVER_EQ,   lambda: self.calculate()),
        ]

        for (label, row, col, span, bg, hover, cmd) in buttons:
            self._make_button(grid, label, row, col, span, bg, hover, cmd)

        # History panel
        hist_frame = tk.Frame(main, bg=BG)
        hist_frame.pack(fill="x", pady=(14, 0))
        tk.Label(hist_frame, text="History", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10)).pack(anchor="w")
        self.hist_box = tk.Text(hist_frame, bg=BTN_NUM, fg=TEXT_MAIN,
                                font=("Segoe UI", 10), height=4, width=28,
                                relief="flat", state="disabled", padx=8, pady=6)
        self.hist_box.pack(fill="x")

        # Keyboard bindings
        self.root.bind("<Key>", self._key_press)

    def _make_button(self, parent, label, row, col, span, bg, hover, cmd):
        btn = tk.Label(parent, text=label, bg=bg, fg=BG if bg in (BTN_EQ, BTN_OP, BTN_CLR, BTN_SPEC) else TEXT_MAIN,
                       font=("Segoe UI", 15, "bold"),
                       width=4, height=2, cursor="hand2",
                       relief="flat")
        btn.grid(row=row, column=col, columnspan=span,
                 padx=5, pady=5, sticky="nsew")
        btn.bind("<Button-1>", lambda e: cmd())
        btn.bind("<Enter>",    lambda e, b=btn, h=hover: b.config(bg=h))
        btn.bind("<Leave>",    lambda e, b=btn, bg_=bg: b.config(bg=bg_))

    # ── Logic ───────────────────────────────────────────────────
    def append(self, char):
        if self.result_shown and char not in "+-*/":
            self.expression = ""
        self.result_shown = False

        # Prevent double operators
        if char in "+-*/" and self.expression and self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1]

        self.expression += char
        self._update_display(self.expression)
        self.expr_var.set(self._pretty(self.expression))

    def clear(self):
        self.expression = ""
        self.result_shown = False
        self.display_var.set("0")
        self.expr_var.set("")
        self.history_var.set("")

    def backspace(self):
        if self.result_shown:
            self.clear()
            return
        self.expression = self.expression[:-1]
        self._update_display(self.expression or "0")
        self.expr_var.set(self._pretty(self.expression))

    def sqrt(self):
        try:
            val = float(self.expression or "0")
            if val < 0:
                self.display_var.set("Error")
                self.expression = ""
                return
            result = math.sqrt(val)
            self._finish(f"√({self._pretty(self.expression)})", result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def calculate(self):
        if not self.expression:
            return
        try:
            expr = self.expression.replace("%", "/100")
            result = eval(expr)
            self._finish(self._pretty(self.expression) + " =", result)
        except ZeroDivisionError:
            self.display_var.set("÷ 0 Error")
            self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def _finish(self, label, result):
        # Format nicely
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        result_str = str(result)

        self.history_var.set(label)
        self._add_history(f"{label} {result_str}")
        self.expression = result_str
        self.display_var.set(result_str)
        self.expr_var.set("")
        self.result_shown = True

    def _update_display(self, text):
        self.display_var.set(text if text else "0")

    def _pretty(self, expr):
        return expr.replace("*", "×").replace("/", "÷").replace("-", "−")

    def _add_history(self, entry):
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()
        self.hist_box.config(state="normal")
        self.hist_box.delete("1.0", "end")
        for h in self.history[:4]:
            self.hist_box.insert("end", h + "\n")
        self.hist_box.config(state="disabled")

    def _key_press(self, event):
        key = event.char
        if key in "0123456789.+-*/":
            self.append(key)
        elif key in ("\r", "="):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()

# ── Run ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
