import tkinter as tk
from tkinter import ttk, messagebox
from logic.habits_logic import get_habits, add_habit, delete_habit

class HabitsUI:
    def __init__(self, root):
        self.root = root

        # ===== MAIN CONTAINER =====
        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        # ===== HEADER =====
        header = ttk.Label(
            main,
            text="Habits Tracker",
            font=("Segoe UI", 16, "bold")
        )
        header.pack(anchor="w", pady=(0, 15))

        # ===== CONTENT AREA =====
        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        # LEFT: INPUTS
        input_frame = ttk.LabelFrame(content, text="Add New Habit", padding=15)
        input_frame.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(input_frame, text="Habit name:").pack(anchor="w")
        self.habit_entry = ttk.Entry(input_frame, width=25)
        self.habit_entry.pack(pady=5)

        self.add_button = ttk.Button(
            input_frame,
            text="Add Habit",
            command=self.add_habit
        )
        self.add_button.pack(pady=(10, 0), fill="x")

        # RIGHT: LIST
        list_frame = ttk.LabelFrame(content, text="Your Habits", padding=15)
        list_frame.pack(side="right", fill="both", expand=True)

        self.habit_list = tk.Listbox(list_frame, height=10)
        self.habit_list.pack(fill="both", expand=True)

        # ===== ACTION BAR =====
        actions = ttk.Frame(main)
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(actions, text="Mark Done", command=self.mark_done).pack(side="left")
        ttk.Button(actions, text="Delete", command=self.delete_habit).pack(side="left", padx=5)

        # ===== STATUS BAR =====
        self.status_label = ttk.Label(main, text="", foreground="green")
        self.status_label.pack(fill="x", pady=(10, 0))

        # ===== LOAD HABITS FROM STORAGE =====
        self.habits = get_habits()
        for habit in self.habits:
            self.habit_list.insert(tk.END, habit)

    def add_habit(self):
        habit = self.habit_entry.get().strip()
        if not habit:
            messagebox.showwarning("Input error", "Please enter a habit name.")
            return

        add_habit(habit)  # Save habit using logic layer
        self.habit_list.insert(tk.END, habit)
        self.habit_entry.delete(0, tk.END)
        self.show_status(f"Habit '{habit}' added!")

    def delete_habit(self):
        selected = self.habit_list.curselection()
        if not selected:
            messagebox.showwarning("Selection error", "Please select a habit to delete.")
            return

        index = selected[0]
        delete_habit(index)  # Remove habit from storage
        self.habit_list.delete(index)
        self.show_status("Habit deleted!")

    def mark_done(self):
        selected = self.habit_list.curselection()
        if not selected:
            messagebox.showwarning("Selection error", "Please select a habit to mark done.")
            return

        index = selected[0]
        habit = self.habits[index]
        if habit.startswith("✔ "):
            self.show_status(f"Habit '{habit[2:]}' is already marked done.")
            return

        self.habits[index] = f"✔ {habit}"
        # Update storage and UI
        self.habit_list.delete(index)
        self.habit_list.insert(index, self.habits[index])
        from logic.habits_logic import save_habits  # Save full list after update
        save_habits(self.habits)
        self.show_status(f"Habit '{habit}' marked done.")

    def show_status(self, message):
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text=""))  # Clear after 3 seconds
