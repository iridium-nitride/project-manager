import json
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.rule import Rule

theme = Theme({
    "error": "red",
    "warning": "yellow"
})

console = Console(theme=theme)

FILEPATH: str = "data.json"

class Project:
    def __init__(self, name: str, description: str, tasks: list["Task"]):
        self.name = name
        self.description = description
        self.tasks = tasks

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tasks": [task.to_dict() for task in self.tasks]
        }


class Task:
    def __init__(self, name: str, description: str, priority: int, completed: bool):
        self.name = name
        self.description = description
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed
        }

def query_new_project(existing_projects: list[Project]) -> Project:
    console.print(Rule("NEW PROJECT"))

    while True:
        name = input("NAME (Will be converted to THIS_FORMAT): ").strip().upper().replace(" ", "_")
        if not name: continue

        if any(project.name == name for project in existing_projects):
            console.print("Project with that name already exists.", style="warning")
            continue

        break

    while True:
        description = input("DESCRIPTION: ").strip()
        if description: break

    return Project(name=name, description=description, tasks=[])

def query_new_task(existing_tasks: list[Task]) -> Task:
    console.print(Rule("NEW TASK"))

    while True:
        name = input("NAME (Will be converted to THIS_FORMAT): ").strip().upper().replace(" ", "_")
        if not name: continue

        if any(task.name == name for task in existing_tasks):
            console.print("Task with that name already exists.", style="warning")
            continue

        break

    while True:
        description = input("DESCRIPTION: ").strip()
        if description: break

    while True:
        try:
            priority = int(input("PRIORITY (1-5): ").strip())

            if 1 <= priority <= 5:
                break
            else:
                console.print("Priority must be between 1 and 5.", style="warning")
        except ValueError:
            console.print("Please enter a number.", style="warning")

    return Task(name=name, description=description, priority=priority, completed=False)

def print_projects(projects: list[Project]) -> None:
    if not projects:
        console.print("No projects found.", style="warning")
        return

    table = Table(title="Projects")

    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("Remaining Tasks", justify="right")
    table.add_column("Total Tasks", justify="right")

    for project in projects:
        table.add_row(
            project.name,
            project.description,
            str(sum(not task.completed for task in project.tasks)),
            str(len(project.tasks))
        )

    console.print(table)

def print_tasks(project: Project) -> None:
    if not project.tasks:
        console.print("No tasks found.", style="warning")
        return

    table = Table(title=f"{project.name}: Tasks")

    table.add_column("Name", style="bold")
    table.add_column("Completed", style="bold")
    table.add_column("Priority", justify="right")
    table.add_column("Description")

    for task in project.tasks:
        table.add_row(
            task.name,
            "Yes" if task.completed else "No",
            str(task.priority),
            task.description
        )

    console.print(table)

def print_help() -> None:
    console.print("""\
Project Manager v1.0

A simple CLI project/task management program.
Commands are used to create, view, and manage projects and tasks.
Commands are not case sensitive.
All data is stored in a 'data.json' file; do not remove or rename this file.

:: PROJECTS/P:
    Lists projects.
    
:: TASKS/T:
    Lists tasks in currently open project.
    
:: OPEN/O [project name]:
    Opens specified project.
    
:: NEW_PROJECT/NP:
    Creates new project.
    
:: NEW_TASK/NEW/NT/N:
    Creates new task in currently open project.
    
:: COMPLETE/C:
    Marks specified task as completed (or vice versa).
    
:: DELETE/D:
    Deletes specified project or task (if project is selected).
    
:: CLOSE/X:
    Closes currently open project.
    
:: SAVE/S:
    Saves changes to JSON.
    
:: HELP/H:
    Opens help menu.
    
:: EXIT/QUIT/Q:
    Exits the program while auto-saving changes.
    
:: FORCE_QUIT/FQ:
    Exits the program without saving changes.
""")

def save_changes(projects: list[Project], filepath: str = FILEPATH) -> None:
    data = [project.to_dict() for project in projects]

    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)

def load_json(filepath: str = FILEPATH) -> list[Project]:
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    projects = []

    for project in data:
        tasks = [
            Task(
                name=task["name"],
                description=task["description"],
                priority=task["priority"],
                completed=task["completed"]
            ) for task in project.get("tasks", [])
        ]

        projects.append(
            Project(
                name=project["name"],
                description=project["description"],
                tasks=tasks
            )
        )

    return projects

def quit_program(projects: list[Project]) -> None:
    if input("Are you sure you want to exit? (Changes you made will be automatically saved) [Y/n] ").strip().upper().startswith("N"):
        console.print("Cancelled.")
    else:
        save_changes(projects)
        quit()

def force_quit_program() -> None:
    if input("Are you sure you want to exit without saving changes? [y/N] ").strip().upper().startswith("Y"):
        quit()
    else:
        console.print("Cancelled.")

def main():
    projects = load_json()
    selected_project = None

    console.print("Welcome to Project Manager v1.0!")
    console.print("Type 'HELP' for a list of commands.")
    console.print()

    while True:
        tokens = input(f"{selected_project.name if selected_project else ""}{" " if selected_project else ""}:: ").upper().strip().split()

        if tokens == [""]:
            continue

        cmd = tokens[0]
        arg = tokens[1] if len(tokens) > 1 else ""

        match cmd:
            case "PROJECTS" | "P":
                print_projects(projects)

            case "TASKS" | "T":
                if not selected_project:
                    console.print("No project selected.", style="warning")
                    continue
                print_tasks(selected_project)

            case "OPEN" | "O":
                if not arg:
                    console.print("Expecting argument (to specify project) but none found. Try 'OPEN MY_PROJECT'", style="error")
                    continue

                selected_project = next(
                    (project for project in projects if project.name == arg),
                    None
                )

                if not selected_project:
                    console.print("Project not found.", style="warning")

            case "NEW_PROJECT" | "NP":
                new_project: Project = query_new_project(projects)
                projects.append(new_project)
                selected_project = new_project

            case "NEW_TASK" | "NEW" | "NT" | "N":
                if not selected_project:
                    console.print("No project selected.", style="warning")
                    continue

                new_task: Task = query_new_task(selected_project.tasks)
                selected_project.tasks.append(new_task)

            case "COMPLETE" | "C":
                if not selected_project:
                    console.print("No project selected.", style="warning")
                    continue

                if not arg:
                    console.print("No task provided.", style="warning")
                    continue

                selected_task = next(
                    (task for task in selected_project.tasks if task.name == arg),
                    None
                )

                if not selected_task:
                    console.print("Task not found.", style="warning")
                    continue

                selected_task.completed = not selected_task.completed

            case "DELETE" | "D":
                if not arg:
                    console.print("You must specify the task or project to delete.", style="warning")
                    continue

                if selected_project:
                    deleted_task = next(
                        (task for task in selected_project.tasks if task.name == arg),
                        None
                    )

                    if not deleted_task:
                        console.print("Task not found.", style="warning")
                        continue

                    if input(f"Are you sure you want to delete task {deleted_task.name}? [y/N] ").strip().upper().startswith("Y"):
                        selected_project.tasks.remove(deleted_task)
                    else:
                        console.print("Cancelled.")
                else:
                    deleted_project = next(
                        (project for project in projects if project.name == arg),
                        None
                    )

                    if not deleted_project:
                        console.print("Project not found.", style="warning")
                        continue

                    if input(f"Are you sure you want to delete project {deleted_project.name}? [y/N] ").strip().upper().startswith("Y"):
                        projects.remove(deleted_project)
                    else:
                        console.print("Cancelled.")

            case "CLOSE" | "X":
                selected_project = None

            case "SAVE" | "S":
                save_changes(projects)
                console.print("Changes saved.")

            case "HELP" | "H":
                print_help()

            case "EXIT" | "QUIT" | "Q":
                quit_program(projects)

            case "FORCE_QUIT" | "FQ":
                force_quit_program()

            case _:
                console.print("Command not found. Try 'HELP' for a list of commands.", style="warning")

        console.print()

if __name__ == "__main__":
    main()