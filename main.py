import tkinter as tk
from tkinter import ttk
from ui.habits_ui import HabitsUI
from ui.finance_ui import FinanceUI

def main():
    root = tk.Tk()
    root.title("Life Assistant")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    habits_tab = tk.Frame(notebook)
    finance_tab = tk.Frame(notebook)

    notebook.add(habits_tab, text="Habits")
    notebook.add(finance_tab, text="Finance")

    HabitsUI(habits_tab)
    FinanceUI(finance_tab)

    root.mainloop()

if __name__ == "__main__":
    main()
