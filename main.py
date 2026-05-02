import json

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
    print("NEW PROJECT")
    print("-----------")

    while True:
        name = input("NAME (Will be converted to THIS_FORMAT): ").strip().upper().replace(" ", "_")
        if not name: continue

        if any(project.name == name for project in existing_projects):
            print("Project with that name already exists.")
            continue

        break

    while True:
        description = input("DESCRIPTION: ").strip()
        if description: break

    return Project(name=name, description=description, tasks=[])

def query_new_task(existing_tasks: list[Task]) -> Task:
    print("NEW TASK")
    print("--------")

    while True:
        name = input("NAME (Will be converted to THIS_FORMAT): ").strip().upper().replace(" ", "_")
        if not name: continue

        if any(task.name == name for task in existing_tasks):
            print("Task with that name already exists.")
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
                print("Priority must be between 1 and 5.")
        except ValueError:
            print("Please enter a number.")

    return Task(name=name, description=description, priority=priority, completed=False)

def print_projects(projects: list[Project]) -> None:
    if not projects:
        print("No projects found.")

    for i, project in enumerate(projects):
        print(f"{project.name}")
        print(f"-- DESCRIPTION: {project.description}")
        print(f"-- TASKS REMAINING: {len([task for task in project.tasks if not task.completed])}")
        print(f"-- TOTAL TASKS: {len(project.tasks)}")

        if i < len(projects) - 1:
            print()

def print_tasks(project: Project) -> None:
    if not project.tasks:
        print("No tasks found.")

    for i, task in enumerate(project.tasks):
        print(f"{task.name}")
        print(f"-- DESCRIPTION: {task.description}")
        print(f"-- PRIORITY: {task.priority}")
        print(f"-- COMPLETED: {task.completed}")

        if i < len(project.tasks) - 1:
            print()

def print_help() -> None:
    print("""\
Project Manager v1.0

Commands are not case sensitive.

PROJECTS, P:
    Lists projects.

TASKS, T:
    Lists tasks.

OPEN, O:
    Opens new project; requires project name as argument (e.g. 'OPEN MY_PROJECT').

NEW_PROJECT, NP:
    Creates new project.

NEW_TASK, NEW, NT, N:
    Creates new task in open project.

COMPLETE, C:
    Marks specified task as completed (or vice versa).

CLOSE, X:
    Closes currently open project.

SAVE, S:
    Saves changes to JSON.

HELP, H:
    Opens this help menu.

EXIT, QUIT, Q:
    Exits the program while auto-saving changes.

FORCE_QUIT, FQ:
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
        print("Cancelled.")
    else:
        save_changes(projects)
        quit()

def force_quit_program() -> None:
    if input("Are you sure you want to exit without saving changes? [y/N] ").strip().upper().startswith("Y"):
        quit()
    else:
        print("Cancelled.")

def main():
    projects = load_json()
    selected_project = None

    print("Welcome to Project Manager v1.0!")
    print("Type 'HELP' for a list of commands.")
    print()

    while True:
        tokens: list[str] = input(
            f"{selected_project.name if selected_project else ""}{" " if selected_project else ""}:: ").upper().strip().split()

        if tokens == [""]:
            print("Please enter a command. Try 'HELP' for a list of commands.")
            continue

        cmd: str = tokens[0]
        arg: str = tokens[1] if len(tokens) > 1 else ""

        match cmd:
            case "PROJECTS" | "P":
                print_projects(projects)

            case "TASKS" | "T":
                if not selected_project:
                    print("No project selected.")
                    continue
                print_tasks(selected_project)

            case "OPEN" | "O":
                if not arg:
                    print("Expecting argument (to specify project) but none found. Try 'OPEN MY_PROJECT'")
                    continue

                selected_project = next(
                    (project for project in projects if project.name == arg),
                    None
                )

                if not selected_project:
                    print("Project not found.")

            case "NEW_PROJECT" | "NP":
                new_project: Project = query_new_project(projects)
                projects.append(new_project)
                selected_project = new_project

            case "NEW_TASK" | "NEW" | "NT" | "N":
                if not selected_project:
                    print("No project selected.")
                    continue

                new_task: Task = query_new_task(selected_project.tasks)
                selected_project.tasks.append(new_task)

            case "COMPLETE" | "C":
                if not selected_project:
                    print("No project selected.")
                    continue

                if not arg:
                    print("No task provided.")
                    continue

                selected_task = next(
                    (task for task in selected_project.tasks if task.name == arg),
                    None
                )

                if not selected_task:
                    print("Task not found.")
                    continue

                selected_task.completed = not selected_task.completed

            case "DELETE" | "D":
                if not arg:
                    print("You must specify the task or project to delete.")
                    continue

                if selected_project:
                    deleted_task = next(
                        (task for task in selected_project.tasks if task.name == arg),
                        None
                    )

                    if not deleted_task:
                        print("Task not found.")
                        continue

                    confirm = input(f"Are you sure you want to delete task {deleted_task.name}? [y/N] ").strip().upper()

                    if confirm == "Y":
                        selected_project.tasks.remove(deleted_task)
                    else:
                        print("Cancelled.")
                else:
                    deleted_project = next(
                        (project for project in projects if project.name == arg),
                        None
                    )

                    if not deleted_project:
                        print("Project not found.")
                        continue

                    confirm = input(f"Are you sure you want to delete project {deleted_project.name}? [y/N] ").strip().upper()

                    if confirm == "Y":
                        projects.remove(deleted_project)
                    else:
                        print("Cancelled.")

            case "CLOSE" | "X":
                selected_project = None

            case "SAVE" | "S":
                save_changes(projects)
                print("Changes saved.")

            case "HELP" | "H":
                print_help()

            case "EXIT" | "QUIT" | "Q":
                quit_program(projects)

            case "FORCE_QUIT" | "FQ":
                force_quit_program()

            case _:
                print("Command not found. Try 'HELP' for a list of commands.")

        print()

if __name__ == "__main__":
    main()