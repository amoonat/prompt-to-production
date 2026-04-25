import tkinter as tk
from decimal import Decimal, InvalidOperation

class RetailCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Retail Calculator")
        self.master.geometry("400x650")
        self.master.configure(bg="#121212")
        self.master.minsize(350, 500)

        # Fonts - Using Inter, Outfit or system fallbacks
        self.large_font = ("Inter", 42, "bold")
        self.small_font = ("Inter", 18)
        self.btn_font = ("Inter", 22, "bold")

        # State
        self.current_expression = "0"
        self.history_expression = ""
        self.last_operator = None
        self.first_operand = None
        self.new_input_starting = True

        self.create_widgets()
        self.bind_keys()
        
        # Grid weight configuration for responsiveness
        self.master.grid_rowconfigure(0, weight=1)
        for i in range(1, 7):
            self.master.grid_rowconfigure(i, weight=2)
        for i in range(4):
            self.master.grid_columnconfigure(i, weight=1)

    def create_widgets(self):
        # Displays Frame
        display_frame = tk.Frame(self.master, bg="#121212")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=20, pady=20)
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        # Ghost history preview
        self.history_label = tk.Label(display_frame, text="", bg="#121212", fg="#888888", font=self.small_font, anchor="e")
        self.history_label.grid(row=0, column=0, sticky="ew")

        # Main large responsive output
        self.main_label = tk.Label(display_frame, text="0", bg="#121212", fg="#FFFFFF", font=self.large_font, anchor="e")
        self.main_label.grid(row=1, column=0, sticky="ew")

        # Deep Dark theme with pastel colors for buttons
        button_colors = {
            "numbers": {"bg": "#2C303A", "fg": "#FFFFFF", "active_bg": "#3A3F47"},
            "operators": {"bg": "#FFB347", "fg": "#121212", "active_bg": "#FFCC80"},
            "clear": {"bg": "#FFB3BA", "fg": "#121212", "active_bg": "#FFD1D6"},
            "equals": {"bg": "#AEC6CF", "fg": "#121212", "active_bg": "#C6D8E0"},
            "percent": {"bg": "#B39DDB", "fg": "#121212", "active_bg": "#D1C4E9"}
        }

        # Layout: AC, C, %, /
        #         7,  8, 9, *
        #         4,  5, 6, -
        #         1,  2, 3, +
        #         0,  ., =
        
        buttons = [
            ('AC', 1, 0, button_colors["clear"]), ('C', 1, 1, button_colors["clear"]), ('%', 1, 2, button_colors["percent"]), ('/', 1, 3, button_colors["operators"]),
            ('7', 2, 0, button_colors["numbers"]), ('8', 2, 1, button_colors["numbers"]), ('9', 2, 2, button_colors["numbers"]), ('*', 2, 3, button_colors["operators"]),
            ('4', 3, 0, button_colors["numbers"]), ('5', 3, 1, button_colors["numbers"]), ('6', 3, 2, button_colors["numbers"]), ('-', 3, 3, button_colors["operators"]),
            ('1', 4, 0, button_colors["numbers"]), ('2', 4, 1, button_colors["numbers"]), ('3', 4, 2, button_colors["numbers"]), ('+', 4, 3, button_colors["operators"]),
            ('0', 5, 0, button_colors["numbers"]), ('.', 5, 2, button_colors["numbers"]), ('=', 5, 3, button_colors["equals"])
        ]

        for btn in buttons:
            text, row, col, colors = btn
            colspan = 2 if text == '0' else 1
            action = lambda x=text: self.on_button_click(x)
            
            b = tk.Button(self.master, text=text, font=self.btn_font, 
                          bg=colors["bg"], fg=colors["fg"], 
                          activebackground=colors["active_bg"], activeforeground=colors["fg"],
                          relief="flat", borderwidth=0, command=action, cursor="hand2")
            # Padding for a modern spaced out look
            b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)

    def bind_keys(self):
        self.master.bind("<Key>", self.key_handler)
        self.master.bind("<Return>", lambda event: self.on_button_click("="))
        self.master.bind("<BackSpace>", lambda event: self.on_button_click("C"))
        self.master.bind("<Escape>", lambda event: self.on_button_click("AC"))

    def key_handler(self, event):
        char = event.char
        if char in "0123456789.+-*/%":
            self.on_button_click(char)
        elif char == "\r":
            self.on_button_click("=")

    def format_number(self, num_str):
        if not num_str:
            return "0"
        return num_str

    def update_displays(self):
        self.main_label.config(text=self.format_number(self.current_expression))
        self.history_label.config(text=self.history_expression)

    def calculate(self, op1, op2, operator):
        # Using Decimal prevents 0.1 + 0.2 = 0.30000000000000004
        try:
            d1 = Decimal(op1)
            d2 = Decimal(op2)
            if operator == "+":
                return self.format_result(d1 + d2)
            elif operator == "-":
                return self.format_result(d1 - d2)
            elif operator == "*":
                return self.format_result(d1 * d2)
            elif operator == "/":
                if d2 == 0:
                    return "Cannot divide by zero"
                return self.format_result(d1 / d2)
        except InvalidOperation:
            return "Error"
        return "0"

    def format_result(self, decimal_val):
        # Remove trailing zeros and integerize if possible
        s = str(decimal_val)
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s

    def on_button_click(self, char):
        if char == "AC":
            self.current_expression = "0"
            self.history_expression = ""
            self.first_operand = None
            self.last_operator = None
            self.new_input_starting = True
        
        elif char == "C":
            # Clear only current entry
            self.current_expression = "0"
            self.new_input_starting = True

        elif char in "0123456789":
            if self.new_input_starting:
                self.current_expression = char
                self.new_input_starting = False
            else:
                if self.current_expression == "0":
                    self.current_expression = char
                else:
                    self.current_expression += char

        elif char == ".":
            if self.new_input_starting:
                self.current_expression = "0."
                self.new_input_starting = False
            elif "." not in self.current_expression:
                self.current_expression += "."

        elif char in "+-*/":
            if self.current_expression in ("Error", "Cannot divide by zero"):
                return
            if not self.new_input_starting and self.first_operand is not None and self.last_operator is not None:
                # Chain calculations: e.g. 5 + 5 + 5
                res = self.calculate(self.first_operand, self.current_expression, self.last_operator)
                self.current_expression = res
                self.first_operand = res
            else:
                self.first_operand = self.current_expression if self.current_expression else "0"
            
            self.last_operator = char
            self.history_expression = f"{self.first_operand} {char}"
            self.new_input_starting = True

        elif char == "%":
            if self.current_expression and self.current_expression not in ("Error", "Cannot divide by zero"):
                try:
                    # Convert to percentage
                    val = Decimal(self.current_expression) / Decimal("100")
                    self.current_expression = self.format_result(val)
                    self.new_input_starting = True
                except InvalidOperation:
                    self.current_expression = "Error"

        elif char == "=":
            if self.first_operand is not None and self.last_operator is not None:
                res = self.calculate(self.first_operand, self.current_expression, self.last_operator)
                self.history_expression = f"{self.first_operand} {self.last_operator} {self.current_expression} ="
                self.current_expression = res
                self.first_operand = None
                self.last_operator = None
                self.new_input_starting = True

        self.update_displays()

if __name__ == "__main__":
    root = tk.Tk()
    app = RetailCalculator(root)
    root.mainloop()
