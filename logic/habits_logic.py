from storage.habits_store import load_habits, save_habits

def get_habits():
    return load_habits()

def add_habit(habit):
    habits = load_habits()
    habits.append(habit)
    save_habits(habits)

def delete_habit(index):
    habits = load_habits()
    if 0 <= index < len(habits):
        habits.pop(index)
        save_habits(habits)
