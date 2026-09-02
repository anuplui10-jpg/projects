import tkinter as tk

# ---------- Functions ----------
def click(value):
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current + str(value))

def clear():
    display.delete(0, tk.END)

def calculate():
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")

# ---------- Window setup ----------
window = tk.Tk()
window.title("Calculator")
window.geometry("300x400")

display = tk.Entry(window, font=("Arial", 24), justify="right")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)

# ---------- Button layout ----------
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(window, text=text, font=("Arial", 18), command=calculate)
    else:
        button = tk.Button(window, text=text, font=("Arial", 18), command=lambda t=text: click(t))
    button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

clear_button = tk.Button(window, text="C", font=("Arial", 18), command=clear)
clear_button.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

# Make columns/rows resize evenly
for i in range(4):
    window.grid_columnconfigure(i, weight=1)
for i in range(6):
    window.grid_rowconfigure(i, weight=1)

window.mainloop()