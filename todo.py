"""A small local todo list with JSON storage."""

import argparse
import json
from pathlib import Path


MAX_TASK_LENGTH = 100


def load_state(path):
    if not path.exists():
        return {"next_id": 1, "tasks": []}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("Invalid task file: invalid JSON.") from error
    if (
        not isinstance(state, dict)
        or type(state.get("next_id")) is not int
        or state["next_id"] < 1
        or not isinstance(state.get("tasks"), list)
    ):
        raise ValueError("Invalid task file: expected next_id and tasks.")
    ids = []
    for task in state["tasks"]:
        if (
            not isinstance(task, dict)
            or type(task.get("id")) is not int
            or task["id"] < 1
            or not isinstance(task.get("title"), str)
            or type(task.get("done")) is not bool
        ):
            raise ValueError("Invalid task file: malformed task.")
        ids.append(task["id"])
    if len(ids) != len(set(ids)) or state["next_id"] <= max(ids, default=0):
        raise ValueError("Invalid task file: inconsistent task IDs.")
    return state


def save_state(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def add_task(state, title):
    # Known demo issue: whitespace-only input passes this empty check.
    if title == "":
        raise ValueError("Title cannot be empty.")
    title = title.strip()
    if len(title) > MAX_TASK_LENGTH:
        raise ValueError(f"Title must be at most {MAX_TASK_LENGTH} characters.")
    task = {"id": state["next_id"], "title": title, "done": False}
    state["tasks"].append(task)
    state["next_id"] += 1
    return task


def find_task(state, task_id):
    for task in state["tasks"]:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task {task_id} not found.")


def main():
    parser = argparse.ArgumentParser(description="Manage a local todo list.")
    parser.add_argument("--file", type=Path, default=Path("data/todos.json"),
                        help="task file (default: data/todos.json)")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="add a task")
    add.add_argument("title", help="put a multiword title in quotes")
    commands.add_parser("list", help="show all tasks")
    for name, help_text in (("done", "mark a task complete"),
                            ("remove", "delete a task")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("id", type=int, help="task ID shown by list")
    args = parser.parse_args()

    try:
        state = load_state(args.file)
        if args.command == "list":
            if not state["tasks"]:
                print("No tasks yet.")
            for task in state["tasks"]:
                marker = "x" if task["done"] else " "
                print(f"{task['id']}. [{marker}] {task['title']}")
            return
        if args.command == "add":
            task = add_task(state, args.title)
            message = f"Added task {task['id']}: {task['title']}"
        else:
            task = find_task(state, args.id)
            if args.command == "done":
                task["done"] = True
                message = f"Completed task {args.id}."
            else:
                state["tasks"].remove(task)
                message = f"Removed task {args.id}."
        save_state(args.file, state)
        print(message)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
