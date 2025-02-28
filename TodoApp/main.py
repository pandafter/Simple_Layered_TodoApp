#Punto de entrada principal de la aplicacion
from views.task_views import TaskView
from controllers.task_controller import TaskController
from database.db import create_database

def main():
    # Crear la base de datos
    create_database()

    # Inicializar la aplicación
    app = TaskView()
    controller = TaskController()
    app.set_controller(controller)

    # Mostrar las tareas iniciales
    app.refresh_tasks()

    # Iniciar el bucle de la aplicación
    app.mainloop()

if __name__ == "__main__":
    main()