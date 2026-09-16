# Usage and storage

Run commands from the repository directory. Put a multiword title in quotes so
your terminal passes it as one argument.

## Commands

```bash
python3 todo.py add "Read chapter 3"
python3 todo.py list
python3 todo.py done 1
python3 todo.py remove 1
```

`add` saves a task and reports its number. `list` shows that number, the completion
marker and the title. `[ ]` means unfinished; `[x]` means complete. `done` marks
the selected task complete. Repeating `done` is harmless. `remove` deletes the
selected task from this local list, not from GitHub.

Task IDs are increasing numbers. Deleting task 2 does not change task 3's ID, and
a new task does not reuse a deleted ID. A nonexistent ID produces an error and
leaves the task file unchanged.

## Separate data files

The default path is `data/todos.json`, relative to the directory where you run the
command. Use `--file` before the command when you want another list:

```bash
python3 todo.py --file data/demo.json add "Prepare the demo"
python3 todo.py --file data/demo.json list
```

Use the same file for every command in that session. If the file does not exist,
`list` shows `No tasks yet.` without creating it. `add` creates the directory and
file on the first successful write. Files under `data/` are not committed.
An explicit path outside `data/` is your responsibility to keep out of Git.

## JSON structure

After adding one task, the file contains:

```json
{
  "next_id": 2,
  "tasks": [
    {"id": 1, "title": "Read chapter 3", "done": false}
  ]
}
```

`next_id` is the number for the next task. `tasks` is a list of task records. Each
record contains an ID, a title and a boolean completion status. JSON uses `true`
and `false` for boolean values. There are no AWS credentials or GitHub tokens in
this file, and the application makes no network calls.

## Input and errors

The application trims surrounding spaces and limits title length. Inspect
`MAX_TASK_LENGTH` in `todo.py` when investigating the current numeric limit.
An empty string is rejected. Spaces-only input is a known defect, reproduced in
[the demo scenarios](demo-scenarios.md).

Errors go to the terminal's error output with a nonzero exit status. Invalid JSON
or an invalid task structure is reported instead of silently replacing the file.
The tool is intended for one local command at a time. It does not coordinate
simultaneous writers or provide a production database or backup system.
