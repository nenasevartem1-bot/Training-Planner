import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        # Поля ввода
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Метки и поля ввода
        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(self.root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица тренировок
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтрация
        ttk.Label(self.root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Entry(self.root)
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, columnspan=2, pady=10)

    def add_training(self):
        date = self.date_entry.get()
        tr_type = self.type_entry.get()
        duration = self.duration_entry.get()

        # Проверка корректности ввода
        try:
            datetime.strptime(date, "%Y-%m-%d")
            duration = float(duration)
            if duration <= 0:
                raise ValueError("Длительность должна быть положительным числом.")
            if not tr_type:
                raise ValueError("Тип тренировки не может быть пустым.")

            self.data.append({"date": date, "type": tr_type, "duration": duration})
            self.update_table()
            self.save_data()
            self.clear_entries()

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.data:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def apply_filter(self):
        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get()

        filtered = self.data
        if f_type:
            filtered = [x for x in filtered if f_type in x["type"].lower()]
        if f_date:
            filtered = [x for x in filtered if x["date"] == f_date]

        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in filtered:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def save_data(self):
        with open("trainings.json", "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        try:
            with open("trainings.json", "r") as f:
                self.data = json.load(f)
                self.update_table()
        except FileNotFoundError:
            pass

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
