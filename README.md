# Task Manager

A simple command-line task manager written in Python. Tasks are stored
locally in a `tasks.json` file, so your list persists between runs.

## Requirements

- Python 3.7+ (no external packages needed — only the standard library)

## Installation

No installation step is required. Just make sure `task_manager.py` and
`README.md` are in the same folder, then run the script with Python:

```bash
python task_manager.py --help
```

The first time you add a task, a `tasks.json` file will be created
automatically in that same folder.

## Usage

The tool supports four commands: `add`, `list`, `complete`, and `delete`.

### Add a task

```bash
python task_manager.py add "Buy groceries"
```

```
Added task 1: Buy groceries (priority: medium)
```

You can also set a priority when adding a task (see
[Priority levels](#priority-levels) below):

```bash
python task_manager.py add "Fix production bug" --priority high
```

### List tasks

```bash
python task_manager.py list
```

```
1. [ ] Fix production bug (priority: high)
2. [ ] Buy groceries (priority: medium)
```

Each line shows the task's ID, a checkbox (`[x]` for done, `[ ]` for not
done), its description, and its priority. Tasks are sorted with the
highest priority first.

### Complete a task

Mark a task as done using its ID (shown by `list`):

```bash
python task_manager.py complete 1
```

```
Marked task 1 as done: Fix production bug
```

### Delete a task

Remove a task permanently using its ID:

```bash
python task_manager.py delete 2
```

```
Deleted task 2: Buy groceries
```

## Priority levels

Tasks can have one of three priority levels:

- `high`
- `medium` (default)
- `low`

Set a priority when adding a task with the `--priority` flag:

```bash
python task_manager.py add "Renew passport" --priority low
```

If you don't specify `--priority`, the task defaults to `medium`.

When you run `list`, tasks are automatically sorted so `high` priority
tasks appear first, followed by `medium`, then `low`. Tasks that were
created before this feature existed (with no priority saved) are treated
as `medium`.

## Data storage

All tasks are saved in `tasks.json` in the same folder as
`task_manager.py`. Each task is stored as a JSON object with an `id`,
`description`, `done` flag, and `priority`. You generally don't need to
edit this file by hand, but it's plain, readable JSON if you ever want
to inspect or back it up.
