#!/usr/bin/env python3
"""
task_manager.py - A simple command-line task manager.

Tasks are stored in a local JSON file (tasks.json) so they persist
between runs of the script.

Usage:
    python task_manager.py add "Buy groceries" --priority high
    python task_manager.py list
    python task_manager.py complete 1
    python task_manager.py delete 1
"""

import argparse   # Used to parse command-line arguments (add, list, complete, delete)
import json       # Used to read/write our tasks as JSON
import os         # Used to check if the tasks file already exists

# The name of the file where we store our tasks.
# Because we don't give a full path, this file will be created in
# whatever folder you run the script from.
TASKS_FILE = "tasks.json"

# The priority levels a task can have, in highest-to-lowest order.
# We use this list both to validate --priority input and to sort tasks
# (its index doubles as the sort rank, so "high" sorts before "medium").
PRIORITY_LEVELS = ["high", "medium", "low"]


def load_tasks():
    """
    Read tasks.json from disk and return the list of tasks.

    If the file doesn't exist yet (e.g. first time running the app),
    we just return an empty list instead of crashing.
    """
    if not os.path.exists(TASKS_FILE):
        return []

    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        # json.load() reads the file and converts JSON text into
        # Python objects (in our case, a list of dictionaries).
        return json.load(file)


def save_tasks(tasks):
    """
    Write the given list of tasks back to tasks.json.

    We call this every time the task list changes (add/complete/delete)
    so the file on disk always matches what's in memory.
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        # indent=4 just makes the JSON file human-readable if you open it.
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    """
    Figure out the next available task ID.

    We look at the highest ID currently in use and add 1 to it.
    If there are no tasks yet, we start at 1.
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(description, priority="medium"):
    """Add a new task with the given description and priority.

    priority defaults to "medium" if the caller doesn't specify one.
    """
    tasks = load_tasks()

    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "done": False,
        "priority": priority,
    }

    tasks.append(new_task)
    save_tasks(tasks)

    print(f"Added task {new_task['id']}: {description} (priority: {priority})")


def list_tasks():
    """Print out every task, showing whether it's done or not.

    Tasks are sorted so higher-priority tasks are shown first.
    """
    tasks = load_tasks()

    if not tasks:
        print("No tasks yet. Add one with: python task_manager.py add \"Your task\"")
        return

    # Sort by the task's position in PRIORITY_LEVELS, so "high" (index 0)
    # comes before "medium" (index 1) and "low" (index 2). Older tasks use
    # .get("priority", "medium") as a fallback in case they were saved
    # before priorities existed.
    sorted_tasks = sorted(
        tasks,
        key=lambda task: PRIORITY_LEVELS.index(task.get("priority", "medium")),
    )

    for task in sorted_tasks:
        # A simple checkbox-style marker: [x] for done, [ ] for not done.
        status = "[x]" if task["done"] else "[ ]"
        priority = task.get("priority", "medium")
        print(f"{task['id']}. {status} {task['description']} (priority: {priority})")


def find_task(tasks, task_id):
    """
    Helper function to find a task by its ID inside a list of tasks.

    Returns the matching task dictionary, or None if not found.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def complete_task(task_id):
    """Mark the task with the given ID as done."""
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"No task found with id {task_id}")
        return

    task["done"] = True
    save_tasks(tasks)
    print(f"Marked task {task_id} as done: {task['description']}")


def delete_task(task_id):
    """Remove the task with the given ID from the list."""
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"No task found with id {task_id}")
        return

    # Rebuild the list without the task we want to delete.
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"Deleted task {task_id}: {task['description']}")


def main():
    # argparse handles reading the command and arguments you type
    # after "python task_manager.py", e.g. "add", "list", "1", etc.
    parser = argparse.ArgumentParser(description="A simple CLI task manager.")

    # "subparsers" let us define separate commands (add/list/complete/delete),
    # each with its own set of expected arguments.
    subparsers = parser.add_subparsers(dest="command", required=True)

    # "add" command: requires a description of the task, plus an optional
    # --priority flag. choices=PRIORITY_LEVELS makes argparse reject
    # anything that isn't "high", "medium", or "low".
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Description of the task")
    add_parser.add_argument(
        "--priority",
        choices=PRIORITY_LEVELS,
        default="medium",
        help="Priority of the task (default: medium)",
    )

    # "list" command: no extra arguments needed.
    subparsers.add_parser("list", help="List all tasks")

    # "complete" command: requires the ID of the task to mark as done.
    complete_parser = subparsers.add_parser("complete", help="Mark a task as done")
    complete_parser.add_argument("id", type=int, help="ID of the task to complete")

    # "delete" command: requires the ID of the task to remove.
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")

    args = parser.parse_args()

    # Based on which command was used, call the matching function.
    if args.command == "add":
        add_task(args.description, args.priority)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)


# This makes sure main() only runs when the script is executed directly
# (not when it's imported as a module into another script).
if __name__ == "__main__":
    main()
