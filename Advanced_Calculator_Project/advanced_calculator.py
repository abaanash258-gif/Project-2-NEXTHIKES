import ast
import math
import operator
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False


class Calculator:
    # Choose a preset from the theme selector at the top of the window.
    THEMES = {
        "Midnight": {
            "bg": "#151923", "panel": "#202838", "field": "#101722",
            "text": "#F3F6FC", "muted": "#AAB6C8", "accent": "#4F8CFF",
            "button": "#303D52", "button_text": "#FFFFFF",
            "operator": "#365F9D", "success": "#42D6A4",
            "plot": "#202838", "grid": "#64748B"
        },
        "Ocean": {
            "bg": "#DCEFF5", "panel": "#F2FAFC", "field": "#FFFFFF",
            "text": "#123447", "muted": "#527386", "accent": "#087EAA",
            "button": "#C7E3ED", "button_text": "#123447",
            "operator": "#087EAA", "success": "#087F68",
            "plot": "#F2FAFC", "grid": "#A8C9D5"
        },
        "Forest": {
            "bg": "#17251F", "panel": "#22372D", "field": "#142019",
            "text": "#F0F7F1", "muted": "#B1C8B7", "accent": "#4EAD78",
            "button": "#345343", "button_text": "#FFFFFF",
            "operator": "#397D59", "success": "#8BE0A9",
            "plot": "#22372D", "grid": "#718D7A"
        },
        "Sunset": {
            "bg": "#2B2028", "panel": "#3B2B35", "field": "#211921",
            "text": "#FFF4EE", "muted": "#D7BDB5", "accent": "#F08A62",
            "button": "#59404A", "button_text": "#FFF4EE",
            "operator": "#A65350", "success": "#F5B66B",
            "plot": "#3B2B35", "grid": "#987A80"
        },
        "Light": {
            "bg": "#E9EDF3", "panel": "#FFFFFF", "field": "#FFFFFF",
            "text": "#202938", "muted": "#657286", "accent": "#4169C8",
            "button": "#E2E8F0", "button_text": "#202938",
            "operator": "#C9D8F8", "success": "#16856B",
            "plot": "#FFFFFF", "grid": "#CBD5E1"
        },
        "Rose": {
            "bg": "#F7E8EF", "panel": "#FFF5F8", "field": "#FFFFFF",
            "text": "#49283A", "muted": "#8A6076", "accent": "#C64F83",
            "button": "#F1D3E1", "button_text": "#49283A",
            "operator": "#D77AA1", "success": "#39866C",
            "plot": "#FFF5F8", "grid": "#E4BFD0"
        }
    }

    def __init__(self, root):
        self.root = root
        root.title("Advanced Calculator")
        root.geometry("960x720")
        root.minsize(800, 620)

        self.mode = tk.StringVar(value="DEG")
        self.status = tk.StringVar(value="Ready")
        self.theme_name = tk.StringVar(value="Midnight")
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.build_layout()
        self.apply_theme("Midnight")

    def build_layout(self):
        self.toolbar = ttk.Frame(self.root, padding=(14, 10))
        self.toolbar.pack(fill="x")

        self.heading = ttk.Label(
            self.toolbar, text="ADVANCED CALCULATOR",
            style="Heading.TLabel"
        )
        self.heading.pack(side="left")

        self.theme_label = ttk.Label(self.toolbar, text="Color theme:")
        self.theme_label.pack(side="right", padx=(8, 5))

        self.theme_box = ttk.Combobox(
            self.toolbar, textvariable=self.theme_name,
            values=list(self.THEMES.keys()), state="readonly", width=13
        )
        self.theme_box.pack(side="right")
        self.theme_box.bind("<<ComboboxSelected>>", self.change_theme)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=(2, 8))

        self.basic = ttk.Frame(self.tabs, padding=12)
        self.advanced = ttk.Frame(self.tabs, padding=12)
        self.units = ttk.Frame(self.tabs, padding=12)
        self.graph = ttk.Frame(self.tabs, padding=12)

        for frame, name in [
            (self.basic, "Basic"),
            (self.advanced, "Scientific"),
            (self.units, "Unit Conversion"),
            (self.graph, "Graph Plotter")
        ]:
            self.tabs.add(frame, text=name)

        self.make_calc(self.basic, False)
        self.make_calc(self.advanced, True)
        self.make_units()
        self.make_graph()

        self.status_label = ttk.Label(
            self.root, textvariable=self.status,
            style="Status.TLabel", anchor="w", padding=(14, 7)
        )
        self.status_label.pack(fill="x", side="bottom")

    def change_theme(self, event=None):
        self.apply_theme(self.theme_name.get())

    def apply_theme(self, name):
        colors = self.THEMES.get(name, self.THEMES["Midnight"])
        self.colors = colors
        self.root.configure(background=colors["bg"])

        self.style.configure(
            ".", background=colors["panel"], foreground=colors["text"],
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "TFrame", background=colors["panel"]
        )
        self.style.configure(
            "TLabel", background=colors["panel"], foreground=colors["text"]
        )
        self.style.configure(
            "Heading.TLabel", background=colors["bg"],
            foreground=colors["accent"], font=("Segoe UI", 16, "bold")
        )
        self.style.configure(
            "Status.TLabel", background=colors["bg"],
            foreground=colors["muted"], font=("Segoe UI", 9)
        )
        self.style.configure(
            "TButton", background=colors["button"],
            foreground=colors["button_text"], padding=(8, 7),
            borderwidth=0, font=("Segoe UI", 10, "bold")
        )
        self.style.map(
            "TButton",
            background=[("active", colors["accent"]), ("pressed", colors["operator"])],
            foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")]
        )
        self.style.configure(
            "TEntry", fieldbackground=colors["field"],
            foreground=colors["text"], insertcolor=colors["text"],
            padding=8
        )
        self.style.configure(
            "TCombobox", fieldbackground=colors["field"],
            background=colors["button"], foreground=colors["text"],
            arrowcolor=colors["text"], padding=5
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", colors["field"])],
            foreground=[("readonly", colors["text"])]
        )
        self.style.configure(
            "TNotebook", background=colors["bg"], borderwidth=0
        )
        self.style.configure(
            "TNotebook.Tab", background=colors["button"],
            foreground=colors["button_text"], padding=(18, 10),
            font=("Segoe UI", 10, "bold")
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", colors["accent"])],
            foreground=[("selected", "#FFFFFF")]
        )
        self.style.configure(
            "Result.TLabel", background=colors["panel"],
            foreground=colors["success"], font=("Segoe UI", 11, "bold")
        )
        self.style.configure(
            "Section.TLabel", background=colors["panel"],
            foreground=colors["accent"], font=("Segoe UI", 15, "bold")
        )

        # Update the graph too if a chart is currently displayed.
        if getattr(self, "canvas", None) is not None:
            self.draw()

    def evaluate(self, text):
        text = (text.replace("×", "*").replace("÷", "/")
                    .replace("−", "-").replace("^", "**")
                    .replace("π", "pi"))
        if not text.strip():
            raise ValueError("Enter a mathematical expression")

        rad = self.mode.get() == "RAD"
        cv = lambda x: math.radians(x) if not rad else x
        back = lambda x: math.degrees(x) if not rad else x

        funcs = {
            "sin": lambda x: math.sin(cv(x)),
            "cos": lambda x: math.cos(cv(x)),
            "tan": lambda x: math.tan(cv(x)),
            "asin": lambda x: back(math.asin(x)),
            "acos": lambda x: back(math.acos(x)),
            "atan": lambda x: back(math.atan(x)),
            "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
            "abs": abs, "factorial": math.factorial,
            "floor": math.floor, "ceil": math.ceil, "exp": math.exp
        }
        const = {"pi": math.pi, "e": math.e}
        binops = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.Pow: operator.pow, ast.Mod: operator.mod
        }
        unops = {ast.UAdd: operator.pos, ast.USub: operator.neg}
        tree = ast.parse(text, mode="eval")

        def walk(node):
            if isinstance(node, ast.Expression):
                return walk(node.body)
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value
            if isinstance(node, ast.Name):
                if node.id in const:
                    return const[node.id]
                raise ValueError("Unknown name: " + node.id)
            if isinstance(node, ast.BinOp) and type(node.op) in binops:
                a, b = walk(node.left), walk(node.right)
                if isinstance(node.op, ast.Pow) and abs(b) > 1000:
                    raise ValueError("Exponent too large")
                return binops[type(node.op)](a, b)
            if isinstance(node, ast.UnaryOp) and type(node.op) in unops:
                return unops[type(node.op)](walk(node.operand))
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in funcs and len(node.args) == 1
                    and not node.keywords):
                return funcs[node.func.id](walk(node.args[0]))
            raise ValueError("Invalid mathematical expression")

        result = walk(tree)
        if isinstance(result, complex) or not math.isfinite(float(result)):
            raise ValueError("Invalid result")
        return result

    def make_calc(self, parent, scientific):
        title = "Scientific Calculator" if scientific else "Basic Calculator"
        ttk.Label(parent, text=title, style="Section.TLabel").pack(
            anchor="w", pady=(0, 8)
        )

        var = tk.StringVar()
        entry = ttk.Entry(
            parent, textvariable=var, justify="right",
            font=("Consolas", 23)
        )
        entry.pack(fill="x", pady=5, ipady=10)

        result = ttk.Label(parent, text="", style="Result.TLabel")
        result.pack(anchor="w", pady=5)

        def calc(event=None):
            try:
                value = self.evaluate(var.get())
                if isinstance(value, float) and value.is_integer():
                    shown = str(int(value))
                elif isinstance(value, float):
                    shown = f"{value:.12g}"
                else:
                    shown = str(value)
                var.set(shown)
                result.config(text="Result: " + shown)
                self.status.set("Calculation completed")
            except Exception as error:
                result.config(text="Error: " + str(error))
                self.status.set("Invalid expression")
            return "break"

        def clear(event=None):
            var.set("")
            result.config(text="")
            self.status.set("Cleared")
            return "break"

        entry.bind("<Return>", calc)
        entry.bind("<KP_Enter>", calc)
        entry.bind("<Escape>", clear)
        entry.bind("<BackSpace>", lambda event: (var.set(var.get()[:-1]), "break"))

        rows = (
            [["sin(", "cos(", "tan(", "sqrt(", "log("],
             ["asin(", "acos(", "atan(", "ln(", "factorial("]]
            if scientific else []
        )
        rows += [
            ["C", "⌫", "(", ")", "÷"],
            ["7", "8", "9", "×", "−"],
            ["4", "5", "6", "+", "%"],
            ["1", "2", "3", "^", "π"],
            ["0", ".", "e", "=", "DEG/RAD"]
        ]

        pad = ttk.Frame(parent)
        pad.pack(fill="both", expand=True)

        for row_index, row in enumerate(rows):
            for col_index, label in enumerate(row):
                def action(item=label):
                    if item == "C":
                        clear()
                    elif item == "⌫":
                        var.set(var.get()[:-1])
                    elif item == "=":
                        calc()
                    elif item == "DEG/RAD":
                        self.mode.set("RAD" if self.mode.get() == "DEG" else "DEG")
                        self.status.set("Angle mode: " + self.mode.get())
                    else:
                        replacements = {"÷": "/", "×": "*", "−": "-", "π": "pi"}
                        var.set(var.get() + replacements.get(item, item))
                    entry.focus_set()

                ttk.Button(pad, text=label, command=action).grid(
                    row=row_index, column=col_index, sticky="nsew",
                    padx=4, pady=4, ipady=8
                )
            pad.grid_rowconfigure(row_index, weight=1)

        for col in range(5):
            pad.grid_columnconfigure(col, weight=1)

    def make_units(self):
        frame = self.units
        ttk.Label(
            frame, text="Unit Conversion", style="Section.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=10)

        self.cat = tk.StringVar(value="Length")
        self.val = tk.StringVar(value="1")
        self.src = tk.StringVar()
        self.dst = tk.StringVar()
        self.unit_out = tk.StringVar(value="Result will appear here")

        ttk.Label(frame, text="Category").grid(row=1, column=0, sticky="w", pady=6)
        category_box = ttk.Combobox(
            frame, textvariable=self.cat, state="readonly",
            values=["Length", "Mass", "Temperature", "Time"]
        )
        category_box.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Value").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=self.val).grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text="From").grid(row=3, column=0, sticky="w", pady=6)
        self.srcbox = ttk.Combobox(frame, textvariable=self.src, state="readonly")
        self.srcbox.grid(row=3, column=1, sticky="ew")

        ttk.Label(frame, text="To").grid(row=4, column=0, sticky="w", pady=6)
        self.dstbox = ttk.Combobox(frame, textvariable=self.dst, state="readonly")
        self.dstbox.grid(row=4, column=1, sticky="ew")

        ttk.Button(frame, text="Convert", command=self.convert).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=12
        )
        ttk.Label(
            frame, textvariable=self.unit_out, style="Result.TLabel"
        ).grid(row=6, column=0, columnspan=2, sticky="w")

        frame.grid_columnconfigure(1, weight=1)
        category_box.bind("<<ComboboxSelected>>", lambda event: self.units_changed())
        self.units_changed()

    def units_changed(self):
        self.unitsets = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Foot", "Inch"],
            "Mass": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour", "Day"]
        }
        options = self.unitsets[self.cat.get()]
        self.srcbox["values"] = options
        self.dstbox["values"] = options
        self.src.set(options[0])
        self.dst.set(options[1])

    def convert(self):
        try:
            value = float(self.val.get())
            source, target, category = self.src.get(), self.dst.get(), self.cat.get()
            if category == "Temperature":
                to_celsius = {
                    "Celsius": lambda v: v,
                    "Fahrenheit": lambda v: (v - 32) * 5 / 9,
                    "Kelvin": lambda v: v - 273.15
                }
                from_celsius = {
                    "Celsius": lambda v: v,
                    "Fahrenheit": lambda v: v * 9 / 5 + 32,
                    "Kelvin": lambda v: v + 273.15
                }
                answer = from_celsius[target](to_celsius[source](value))
            else:
                factors = {
                    "Length": {
                        "Meter": 1, "Kilometer": 1000, "Centimeter": 0.01,
                        "Millimeter": 0.001, "Mile": 1609.344,
                        "Foot": 0.3048, "Inch": 0.0254
                    },
                    "Mass": {
                        "Kilogram": 1, "Gram": 0.001, "Milligram": 0.000001,
                        "Pound": 0.45359237, "Ounce": 0.028349523125
                    },
                    "Time": {"Second": 1, "Minute": 60, "Hour": 3600, "Day": 86400}
                }
                answer = value * factors[category][source] / factors[category][target]

            self.unit_out.set(f"{value:g} {source} = {answer:.10g} {target}")
            self.status.set("Conversion completed")
        except Exception as error:
            self.unit_out.set("Error: " + str(error))

    def make_graph(self):
        frame = self.graph
        ttk.Label(frame, text="Graph Plotter", style="Section.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=8
        )

        self.x = tk.StringVar(value="10,20,30,40")
        self.y = tk.StringVar(value="25,46,60,46")
        self.kind = tk.StringVar(value="Horizontal Bar")

        ttk.Label(frame, text="X values (comma-separated):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        ttk.Entry(frame, textvariable=self.x).grid(
            row=1, column=1, columnspan=3, sticky="ew"
        )
        ttk.Label(frame, text="Y values (comma-separated):").grid(
            row=2, column=0, sticky="w", pady=5
        )
        ttk.Entry(frame, textvariable=self.y).grid(
            row=2, column=1, columnspan=3, sticky="ew"
        )
        ttk.Label(frame, text="Chart type:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Combobox(
            frame, textvariable=self.kind, state="readonly",
            values=["Horizontal Bar", "Vertical Bar", "Line", "Scatter", "Pie"]
        ).grid(row=3, column=1, sticky="ew")

        ttk.Button(frame, text="Draw Chart", command=self.draw).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=8
        )
        ttk.Button(frame, text="Clear", command=self.clear_graph).grid(
            row=4, column=2, columnspan=2, sticky="ew", pady=8
        )

        self.plot = ttk.Frame(frame)
        self.plot.grid(row=5, column=0, columnspan=4, sticky="nsew")
        for col in range(1, 4):
            frame.grid_columnconfigure(col, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        self.canvas = None

        if not HAS_PLOT:
            ttk.Label(
                self.plot,
                text="Install Matplotlib: python -m pip install matplotlib"
            ).pack(pady=20)

    def clear_graph(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        for widget in self.plot.winfo_children():
            widget.destroy()
        self.status.set("Graph cleared")

    def draw(self):
        if not HAS_PLOT:
            messagebox.showerror(
                "Missing library",
                "Install Matplotlib using: python -m pip install matplotlib"
            )
            return

        try:
            xs = [float(value.strip()) for value in self.x.get().split(",") if value.strip()]
            ys = [float(value.strip()) for value in self.y.get().split(",") if value.strip()]
            kind = self.kind.get()

            if not xs or not ys:
                raise ValueError("Enter X and Y values")
            if kind != "Pie" and len(xs) != len(ys):
                raise ValueError("X and Y must have equal numbers of values")
            if kind == "Pie" and any(value < 0 for value in ys):
                raise ValueError("Pie chart values cannot be negative")

            # Remove the previous chart without changing the status message.
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
                self.canvas = None
            for widget in self.plot.winfo_children():
                widget.destroy()

            colors = self.colors
            fig = Figure(figsize=(7, 3.2), dpi=100)
            fig.patch.set_facecolor(colors["plot"])
            ax = fig.add_subplot(111)
            ax.set_facecolor(colors["plot"])
            ax.tick_params(colors=colors["text"])
            for spine in ax.spines.values():
                spine.set_color(colors["muted"])

            if kind == "Horizontal Bar":
                ax.barh(xs, ys, color=colors["accent"])
                ax.set_xlabel("Y values", color=colors["text"])
                ax.set_ylabel("X values", color=colors["text"])
            elif kind == "Vertical Bar":
                ax.bar(xs, ys, color=colors["accent"])
                ax.set_xlabel("X values", color=colors["text"])
                ax.set_ylabel("Y values", color=colors["text"])
            elif kind == "Line":
                ax.plot(xs, ys, marker="o", color=colors["accent"])
                ax.set_xlabel("X values", color=colors["text"])
                ax.set_ylabel("Y values", color=colors["text"])
            elif kind == "Scatter":
                ax.scatter(xs, ys, color=colors["accent"])
                ax.set_xlabel("X values", color=colors["text"])
                ax.set_ylabel("Y values", color=colors["text"])
            else:
                ax.pie(
                    ys, labels=[str(value) for value in xs],
                    autopct="%1.1f%%"
                )

            ax.set_title(kind + " Chart", color=colors["text"])
            if kind != "Pie":
                ax.grid(True, alpha=0.25, color=colors["grid"])
            fig.tight_layout()

            self.canvas = FigureCanvasTkAgg(fig, master=self.plot)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.status.set(kind + " chart drawn")
        except Exception as error:
            messagebox.showerror("Graph input error", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
