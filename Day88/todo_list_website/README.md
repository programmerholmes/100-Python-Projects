# TaskFlow Todo List Website

A complete Flask + SQLite todo list website for the Todo List assignment.

## Features

- Add new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- Track task status: To Do, In Progress, Done
- Add category, priority, description, and due date
- Search tasks
- Filter by status, priority, and category
- Kanban-style board view
- SQLite database storage
- JSON API endpoint
- Reflection page for the developer diary

## How to run

Open a terminal inside this folder and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open this URL in your browser:

```text
http://127.0.0.1:5000
```

On Windows, you can also double-click:

```text
run_windows.bat
```

## API Routes

```text
GET /api/tasks
GET /api/tasks/<task_id>
```

## Main Pages

```text
/           Main todo list
/add        Add a task
/edit/<id>  Edit a task
/kanban     Kanban board
/reflection Reflection answer
```
