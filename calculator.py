import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        
        self.entry = tk.Entry(master, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        self.create_buttons()
        self.f_num = 0
        self.math = ""

    def button_click(self, number):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(current) + str(number))

    def button_clear(self):
        self.entry.delete(0, tk.END)

    def button_add(self):
        first_number = self.entry.get()
        self.math = "addition"
        self.f_num = float(first_number) if first_number else 0
        self.entry.delete(0, tk.END)

    def button_subtract(self):
        first_number = self.entry.get()
        self.math = "subtraction"
        self.f_num = float(first_number) if first_number else 0
        self.entry.delete(0, tk.END)

    def button_multiply(self):
        first_number = self.entry.get()
        self.math = "multiplication"
        self.f_num = float(first_number) if first_number else 0
        self.entry.delete(0, tk.END)

    def button_divide(self):
        first_number = self.entry.get()
        self.math = "division"
        self.f_num = float(first_number) if first_number else 0
        self.entry.delete(0, tk.END)

    def button_equal(self):
        second_number = self.entry.get()
        self.entry.delete(0, tk.END)
        
        if not second_number:
            second_number = 0
            
        if self.math == "addition":
            self.entry.insert(0, self.f_num + float(second_number))
        elif self.math == "subtraction":
            self.entry.insert(0, self.f_num - float(second_number))
        elif self.math == "multiplication":
            self.entry.insert(0, self.f_num * float(second_number))
        elif self.math == "division":
            if float(second_number) == 0:
                self.entry.insert(0, "Error! Div by zero")
            else:
                self.entry.insert(0, self.f_num / float(second_number))

    def create_buttons(self):
        # Define buttons
        button_1 = tk.Button(self.master, text="1", padx=40, pady=20, command=lambda: self.button_click(1))
        button_2 = tk.Button(self.master, text="2", padx=40, pady=20, command=lambda: self.button_click(2))
        button_3 = tk.Button(self.master, text="3", padx=40, pady=20, command=lambda: self.button_click(3))
        button_4 = tk.Button(self.master, text="4", padx=40, pady=20, command=lambda: self.button_click(4))
        button_5 = tk.Button(self.master, text="5", padx=40, pady=20, command=lambda: self.button_click(5))
        button_6 = tk.Button(self.master, text="6", padx=40, pady=20, command=lambda: self.button_click(6))
        button_7 = tk.Button(self.master, text="7", padx=40, pady=20, command=lambda: self.button_click(7))
        button_8 = tk.Button(self.master, text="8", padx=40, pady=20, command=lambda: self.button_click(8))
        button_9 = tk.Button(self.master, text="9", padx=40, pady=20, command=lambda: self.button_click(9))
        button_0 = tk.Button(self.master, text="0", padx=40, pady=20, command=lambda: self.button_click(0))
        
        button_add = tk.Button(self.master, text="+", padx=39, pady=20, command=self.button_add)
        button_subtract = tk.Button(self.master, text="-", padx=41, pady=20, command=self.button_subtract)
        button_multiply = tk.Button(self.master, text="*", padx=40, pady=20, command=self.button_multiply)
        button_divide = tk.Button(self.master, text="/", padx=41, pady=20, command=self.button_divide)
        
        button_equal = tk.Button(self.master, text="=", padx=91, pady=20, command=self.button_equal)
        button_clear = tk.Button(self.master, text="Clear", padx=79, pady=20, command=self.button_clear)
        
        # Put the buttons on the screen
        button_1.grid(row=3, column=0)
        button_2.grid(row=3, column=1)
        button_3.grid(row=3, column=2)
        
        button_4.grid(row=2, column=0)
        button_5.grid(row=2, column=1)
        button_6.grid(row=2, column=2)
        
        button_7.grid(row=1, column=0)
        button_8.grid(row=1, column=1)
        button_9.grid(row=1, column=2)
        
        button_0.grid(row=4, column=0)
        button_clear.grid(row=4, column=1, columnspan=2)
        
        button_add.grid(row=5, column=0)
        button_equal.grid(row=5, column=1, columnspan=2)
        
        button_subtract.grid(row=6, column=0)
        button_multiply.grid(row=6, column=1)
        button_divide.grid(row=6, column=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
