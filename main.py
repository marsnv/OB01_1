import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class Task:
    def __init__(self, description, deadline, status="не выполнено"):
        self.description = description
        self.deadline = deadline
        self.status = status

    def mark_as_done(self):
        self.status = "выполнено"

    def __str__(self):
        return f"{self.description},{self.deadline},{self.status}"

    @staticmethod
    def from_string(task_str):
        description, deadline, status = task_str.split(',')
        return Task(description, deadline, status)

tasks = []

if os.path.exists("tasks.txt"):
    with open("tasks.txt", "r") as file:
        for line in file:
            tasks.append(Task.from_string(line.strip()))

def add_task():
    description = entry_description.get()
    deadline = entry_deadline.get()
    if not description or not deadline:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
        return
    try:
        datetime.strptime(deadline, "%d%m%Y")
    except ValueError:
        messagebox.showwarning("Ошибка", "Неправильный формат даты")
        return
    tasks.append(Task(description, deadline))
    entry_description.delete(0, tk.END)
    entry_deadline.delete(0, tk.END)
    show_all_tasks()

def mark_task_as_done():
    selected_task = listbox_tasks.curselection()
    if not selected_task:
        messagebox.showwarning("Ошибка", "Выберите задачу")
        return
    task = tasks[selected_task[0]]
    task.mark_as_done()
    show_all_tasks()

def show_all_tasks():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

def show_done_tasks():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        if task.status == "выполнено":
            listbox_tasks.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

def show_undone_tasks():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        if task.status == "не выполнено":
            listbox_tasks.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

def on_closing():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(str(task) + '\n')
    root.destroy()

root = tk.Tk()
root.title("Task Manager")
root.geometry("600x400")

label_description = tk.Label(root, text="Описание задачи:")
label_description.pack()

entry_description = tk.Entry(root, width=50)
entry_description.pack()

label_deadline = tk.Label(root, text="Срок выполнения (ДДММГГГГ):")
label_deadline.pack()

entry_deadline = tk.Entry(root, width=50)
entry_deadline.pack()

frame_buttons_top = tk.Frame(root)
frame_buttons_top.pack()

button_add = tk.Button(frame_buttons_top, text="Добавить задачу", command=add_task)
button_add.pack(side=tk.LEFT)

button_mark_done = tk.Button(frame_buttons_top, text="Отметить выполненной", command=mark_task_as_done)
button_mark_done.pack(side=tk.LEFT)

frame_buttons = tk.Frame(root)
frame_buttons.pack()

button_show_all = tk.Button(frame_buttons, text="Все задачи", command=show_all_tasks)
button_show_all.pack(side=tk.LEFT)

button_show_done = tk.Button(frame_buttons, text="Выполненные задачи", command=show_done_tasks)
button_show_done.pack(side=tk.LEFT)

button_show_undone = tk.Button(frame_buttons, text="Невыполненные задачи", command=show_undone_tasks)
button_show_undone.pack(side=tk.LEFT)

listbox_tasks = tk.Listbox(root, width=80, height=15)
listbox_tasks.pack()

show_all_tasks()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
