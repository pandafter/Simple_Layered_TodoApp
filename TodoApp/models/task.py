from database.db import get_connection

class Task:
    def __init__(self, title, description, completed=False, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute("""
                    UPDATE tasks
                    SET title = ?, description = ?, completed = ?
                    WHERE id = ?
                """, (self.title, self.description, self.completed, self.id))
            else:
                cursor.execute("""
                    INSERT INTO tasks (title, description, completed)
                    VALUES (?, ?, ?)
                """, (self.title, self.description, self.completed))
            conn.commit()
        finally:
            conn.close()

    def mark_as_completed(self):
        self.completed = True
        self.save()

    def mark_as_pending(self):
        self.completed = False
        self.save()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Eliminar la tarea
            cursor.execute("DELETE FROM tasks WHERE id = ?", (self.id,))

            # Reorganizar los IDs
            cursor.execute("UPDATE tasks SET id = id - 1 WHERE id > ?", (self.id,))

            # Actualizar la secuencia de autoincremento
            cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM tasks) WHERE name = 'tasks'")

            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, description, completed FROM tasks")
            tasks = cursor.fetchall()
            return [Task(id=task[0], title=task[1], description=task[2], completed=task[3]) for task in tasks]
        finally:
            conn.close()

    def __str__(self):
        status = "Completada" if self.completed else "Pendiente"
        return f"{self.title} - {self.description} [{status}]"