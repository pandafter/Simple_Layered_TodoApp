# views/task_view.py
import tkinter as tk
from tkinter import ttk
import tksheet

class TaskView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Tareas")
        self.geometry("520x630")

        self.resizable(False, False)

        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabla de tareas (usando tksheet)
        self.sheet = tksheet.Sheet(self.main_frame)
        self.sheet.enable_bindings()  # Habilitar interacciones
        self.sheet.pack(fill="both", expand=True)

        # Configurar columnas
        self.sheet.headers(["ID", "Título", "Descripción", "Estado"])
        self.sheet.column_width(0, 200)  # Ancho de la columna Título
        self.sheet.column_width(1, 200)  # Ancho de la columna Título
        self.sheet.column_width(2, 300)  # Ancho de la columna Descripción
        self.sheet.column_width(3, 100)  # Ancho de la columna Estado

        # Entradas para nueva tarea
        self.title_label = ttk.Label(self.main_frame, text="Titulo Tarea")
        self.title_label.pack(pady=5)
        self.title_entry = ttk.Entry(self.main_frame, width=50)
        self.title_entry.pack(pady=5)

        self.description_label = ttk.Label(self.main_frame, text="Descripción Tarea")
        self.description_label.pack(pady=5)
        self.description_entry = ttk.Entry(self.main_frame, width=50)
        self.description_entry.pack(pady=5)

        # Botones
        self.add_button = ttk.Button(self.main_frame, text="Añadir Tarea", command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = ttk.Button(self.main_frame, text="Marcar como Completada", command=self.mark_as_completed)
        self.complete_button.pack(pady=5)

        self.complete_button = ttk.Button(self.main_frame, text="Marcar como Pendiente", command=self.mark_as_pending)
        self.complete_button.pack(pady=5)

        self.delete_button = ttk.Button(self.main_frame, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.refresh_button = ttk.Button(self.main_frame, text="Actualizar Lista", command=self.refresh_tasks)
        self.refresh_button.pack(pady=5)

        # Índice de la tarea seleccionada
        self.selected_index = None

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            self.controller.add_task(title, description)
            self.refresh_tasks()
            self.title_entry.delete(0, "end")
            self.description_entry.delete(0, "end")

    def mark_as_completed(self):
        selected_row = self.sheet.get_currently_selected()
        if selected_row:
            task_id = self.tasks[selected_row.row].id
            self.controller.mark_task_as_completed(task_id)
            self.refresh_tasks()

    def mark_as_pending(self):
        selected_row = self.sheet.get_currently_selected()
        if selected_row:
            task_id = self.tasks[selected_row.row].id
            self.controller.mark_task_as_pending(task_id)
            self.refresh_tasks()

    def delete_task(self):
        selected_row = self.sheet.get_currently_selected()
        if selected_row:
            task_id = self.tasks[selected_row.row].id
            self.controller.delete_task(task_id)
            self.refresh_tasks()

    def refresh_tasks(self):
        self.tasks = self.controller.get_tasks()
        data = []
        for task in self.tasks:
            status = "Completada" if task.completed else "Pendiente"
            data.append([task.id, task.title, task.description, status])
        self.sheet.set_sheet_data(data)

    def set_controller(self, controller):
        self.controller = controller