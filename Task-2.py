import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Calculator")
        self.master.geometry("400x500")
        self.master.configure(bg="#1e1e2f")

        self.current_input = ""
        self.total = 0
        self.operator = ""
        self.new_num = True

        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self.create_display()
        self.create_buttons()

    def create_display(self):
        display_frame = tk.Frame(self.master, bg="#2a2a40", padx=10, pady=10)
        display_frame.pack(fill=tk.X)

        self.result_display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, 'bold'),
            justify='right',
            state='readonly',
            bg="#2a2a40",
            fg="#161313",
            relief='sunken',
            bd=10,
            insertwidth=2,
            width=14,
            borderwidth=4
        )
        self.result_display.pack(expand=True, fill=tk.BOTH)

    def create_buttons(self):
        button_frame = tk.Frame(self.master, bg="#1e1e2f", padx=10, pady=10)
        button_frame.pack(fill=tk.BOTH, expand=True)

        button_styles = {
            'font': ('Arial', 18, 'bold'),
            'bd': 5,
            'relief': 'raised',
            'activebackground': '#44475a',
            'padx': 10,
            'pady': 10
        }

        num_buttons = {**button_styles, 'bg': "#8cb4b3", 'fg': 'black'}
        op_buttons = {**button_styles, 'bg': "#a38b69", 'fg': 'black'}
        special_buttons = {**button_styles, 'bg': "#8c5856", 'fg': 'white'}

        buttons = [
            
            ('AC', 0, 0, special_buttons, self.clear),
            ('⌫', 0, 1, special_buttons, self.backspace),
            ('%', 0, 2, special_buttons, self.percentage),
            ('√', 0, 3, special_buttons, self.square_root),

            ('7', 1, 0, num_buttons, lambda: self.append_number('7')),
            ('8', 1, 1, num_buttons, lambda: self.append_number('8')),
            ('9', 1, 2, num_buttons, lambda: self.append_number('9')),
            ('/', 1, 3, op_buttons, lambda: self.set_operator('/')),

            ('4', 2, 0, num_buttons, lambda: self.append_number('4')),
            ('5', 2, 1, num_buttons, lambda: self.append_number('5')),
            ('6', 2, 2, num_buttons, lambda: self.append_number('6')),
            ('*', 2, 3, op_buttons, lambda: self.set_operator('*')),

            ('1', 3, 0, num_buttons, lambda: self.append_number('1')),
            ('2', 3, 1, num_buttons, lambda: self.append_number('2')),
            ('3', 3, 2, num_buttons, lambda: self.append_number('3')),
            ('-', 3, 3, op_buttons, lambda: self.set_operator('-')),

            ('0', 4, 0, num_buttons, lambda: self.append_number('0')),
            ('.', 4, 1, num_buttons, self.append_decimal),
            ('+', 4, 2, op_buttons, lambda: self.set_operator('+')),
            ('=', 4, 3, {**op_buttons, 'bg': '#1f75fe', 'fg': 'white'}, self.calculate_result),
        ]

        for text, row, col, style, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, **style)
            btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)

        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

    def append_number(self, num):
        if self.new_num:
            self.current_input = num
            self.new_num = False
        else:
            self.current_input += num
        self.display_var.set(self.current_input)

    def append_decimal(self):
        if '.' not in self.current_input:
            if self.new_num or self.current_input == '':
                self.current_input = '0.'
            else:
                self.current_input += '.'
            self.new_num = False
            self.display_var.set(self.current_input)

    def set_operator(self, op):
        if self.current_input:
            try:
                self.total = float(self.current_input)
            except ValueError:
                self.total = 0
        self.operator = op
        self.new_num = True

    def calculate_result(self):
        try:
            if not self.current_input:
                return
            current = float(self.current_input)
            result = 0
            if self.operator == '+':
                result = self.total + current
            elif self.operator == '-':
                result = self.total - current
            elif self.operator == '*':
                result = self.total * current
            elif self.operator == '/':
                if current == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    return
                result = self.total / current
            else:
                return

            if result == int(result):
                result = int(result)

            self.display_var.set(str(result))
            self.current_input = str(result)
            self.total = result
            self.operator = ""
            self.new_num = True
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")

    def clear(self):
        self.current_input = ""
        self.total = 0
        self.operator = ""
        self.new_num = True
        self.display_var.set("0")

    def backspace(self):
        if not self.new_num and self.current_input:
            self.current_input = self.current_input[:-1]
            self.display_var.set(self.current_input if self.current_input else "0")

    def percentage(self):
        try:
            value = float(self.current_input)
            value = value / 100
            self.current_input = str(value)
            self.display_var.set(self.current_input)
        except ValueError:
            pass

    def square_root(self):
        try:
            value = float(self.current_input)
            if value < 0:
                messagebox.showerror("Error", "Cannot take square root of negative number!")
                return
            result = math.sqrt(value)
            self.current_input = str(int(result) if result == int(result) else result)
            self.display_var.set(self.current_input)
        except ValueError:
            pass

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.eval('tk::PlaceWindow . center')

    def on_key(event):
        key = event.char
        if key.isdigit():
            app.append_number(key)
        elif key in '+-*/':
            app.set_operator(key)
        elif key == '.':
            app.append_decimal()
        elif key in ['\r', '\n', '=']:
            app.calculate_result()
        elif key in ['\x08', '\x7f']:
            app.backspace()

    root.bind('<KeyPress>', on_key)
    root.focus_set()
    root.mainloop()

if __name__ == "__main__":
    main()
