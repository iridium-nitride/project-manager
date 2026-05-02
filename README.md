# Project Manager

A simple CLI project/task management program I developed to learn Python (and programming in general).

## Usage

The program manages a list of projects, each containing their own list of tasks.

Both projects and tasks have metadata, including descriptions, a 'completed' value (for tasks), and a priority value (also for tasks).

The program data is saved to a JSON file in the project directory.

The program is command-based, with these commands:

- `:: PROJECTS/P`: Lists projects.
- `:: TASKS/T`: Lists tasks in currently open project.
- `:: OPEN/O [project name]`: Opens specified project.
- `:: NEW_PROJECT/NP`: Creates new project.
- `:: NEW_TASK/NEW/NT/N`: Creates new task in currently open project.
- `:: COMPLETE/C`: Marks specified task as completed (or vice versa).
- `:: CLOSE/X`: Closes currently open project.
- `:: SAVE/S`: Saves changes to JSON.
- `:: HELP/H`: Opens help menu.
- `:: EXIT/QUIT/Q`: Exits the program while auto-saving changes.
- `:: FORCE_QUIT/FQ`: Exits the program without saving changes.

These commands are not case-sensitive.