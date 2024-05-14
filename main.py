import tkinter as tk
from tkinter import simpledialog

class Task:
    def __init__(self, description, deadline, status="не выполнено"):
        self.description = description
        self.deadline = deadline
        self.status = status

    def create_task(self):
        self.description = simpledialog.askstring("Создать задачу", "Введите описание новой задачи")
        self.deadline = simpledialog.askstring("Создать задачу", "Введите срок выполнения в формате ДДММГГГГ")
        incomplete_tasks.append(self)

    def mark_completed(self):
        self.status = "выполнено"

def save_tasks():
    with open("task_list.txt", "w") as f:
        for task in incomplete_tasks:
            f.write(f"{task.description},{task.deadline},{task.status}\n")

def load_tasks():
    try:
        with open("task_list.txt", "r") as f:
            for line in f:
                task_info = line.strip().split(",")
                task = Task(task_info[0], task_info[1], task_info[2])
                incomplete_tasks.append(task)
    except FileNotFoundError:
        pass

def show_all_tasks():
    listbox.delete(0, tk.END)
    for task in incomplete_tasks:
        listbox.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

def show_completed_tasks():
    listbox.delete(0, tk.END)
    for task in incomplete_tasks:
        if task.status == "выполнено":
            listbox.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

def show_incomplete_tasks():
    listbox.delete(0, tk.END)
    for task in incomplete_tasks:
        if task.status == "не выполнено":
            listbox.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

root = tk.Tk()
root.title("Менеджер задач")
root.geometry("600x400")

incomplete_tasks = []
load_tasks()

task_label = tk.Label(root, text="Список задач:")
task_label.pack()

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)

def add_task():
    new_task = Task("", "", "не выполнено")
    new_task.create_task()
    update_listbox()

def mark_task_completed():
    selected_task = listbox.curselection()
    if selected_task:
        task = incomplete_tasks[selected_task[0]]
        task.mark_completed()
        update_listbox()

def update_listbox():
    listbox.delete(0, tk.END)
    for task in incomplete_tasks:
        listbox.insert(tk.END, f"{task.description} - {task.deadline} - {task.status}")

add_task_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.pack()

complete_task_button = tk.Button(root, text="Отметить выполненную задачу", command=mark_task_completed)
complete_task_button.pack()

show_all_button = tk.Button(root, text="Все задачи", command=show_all_tasks)
show_all_button.pack()

show_completed_button = tk.Button(root, text="Выполненные задачи", command=show_completed_tasks)
show_completed_button.pack()

show_incomplete_button = tk.Button(root, text="Невыполненные задачи", command=show_incomplete_tasks)
show_incomplete_button.pack()

update_listbox()

root.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), root.destroy()])
root.mainloop()

