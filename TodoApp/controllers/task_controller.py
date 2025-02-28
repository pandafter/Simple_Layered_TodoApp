#Controlador de tasks

from models.task import Task

class TaskController:
    def __init__(self):
        self.tasks = Task.get_all()

    def add_task(self, title, description):
        task = Task(title, description)
        task.save()
        self.tasks = Task.get_all()

    def mark_task_as_completed(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.mark_as_completed()
            self.tasks = Task.get_all()

    def mark_task_as_pending(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.mark_as_pending()
            self.tasks = Task.get_all()

    def delete_task(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.delete()
            self.tasks = Task.get_all()

    def get_tasks(self):
        return Task.get_all()