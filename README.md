# Small todo list

A local Python todo list used as a small repository-maintenance demo for CAB432.
Add a task, list your tasks, mark one complete or remove it. Tasks survive between
commands in a JSON file. The cloud custodian is a separate project.

## Run

Use Python 3.10 or newer. There are no third-party packages to install.
From the repository directory:

```bash
python3 todo.py add "Read chapter 3"
python3 todo.py add "Try the queue practical"
python3 todo.py list
python3 todo.py done 1
python3 todo.py list
python3 todo.py remove 2
```

After completing the first task, the list looks like this:

```text
1. [x] Read chapter 3
2. [ ] Try the queue practical
```

Use `python3 todo.py --help` for command help. Local data goes in
`data/todos.json`, which Git ignores. To use a separate demo file:

```bash
python3 todo.py --file data/presentation.json add "Prepare the demo"
python3 todo.py --file data/presentation.json list
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests use temporary files, not your task list. One expected failure records the
known whitespace-only input defect. It remains open for the maintenance demo.

## Limits

- A task title can contain up to 100 characters after trimming surrounding spaces.
- This is a single-user local tool, without login, due dates or concurrent writes.
- An empty string is rejected, but spaces alone currently create a blank task.

## Repository guide

- [Usage and storage](docs/usage.md): commands, task IDs and the JSON data model.
- [Demo scenarios](docs/demo-scenarios.md): controlled issues and documentation maintenance.
- `todo.py`: the application, including its input rules.
- `tests/test_todo.py`: CLI behavior and regression tests.
