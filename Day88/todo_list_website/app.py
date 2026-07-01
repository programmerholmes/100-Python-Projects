from datetime import date, datetime
import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-me"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "tasks.db")

PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["todo", "doing", "done"]


def get_db_connection():
    """Open a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the tasks table if it does not already exist."""
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'todo',
            due_date TEXT,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
        """
    )
    connection.commit()
    connection.close()


def seed_db():
    """Add a few starter tasks so the website does not look empty at first launch."""
    connection = get_db_connection()
    task_count = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    if task_count == 0:
        starter_tasks = [
            (
                "Finish Python project",
                "Complete the Todo List website and test the main features.",
                "School",
                "High",
                "doing",
                date.today().isoformat(),
            ),
            (
                "Review Flask routes",
                "Practice creating routes for add, edit, delete, and complete actions.",
                "Study",
                "Medium",
                "todo",
                "",
            ),
            (
                "Take a short break",
                "Step away from the screen and come back with fresh focus.",
                "Personal",
                "Low",
                "done",
                "",
            ),
        ]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for title, description, category, priority, status, due_date in starter_tasks:
            completed_at = now if status == "done" else None
            connection.execute(
                """
                INSERT INTO tasks
                (title, description, category, priority, status, due_date, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (title, description, category, priority, status, due_date, now, completed_at),
            )

        connection.commit()

    connection.close()


def fetch_task(task_id):
    """Return one task by id, or None if it does not exist."""
    connection = get_db_connection()
    task = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    connection.close()
    return task


def get_filter_options():
    """Return categories stored in the database for the filter dropdown."""
    connection = get_db_connection()
    categories = connection.execute(
        "SELECT DISTINCT category FROM tasks WHERE category IS NOT NULL AND category != '' ORDER BY category"
    ).fetchall()
    connection.close()
    return [row["category"] for row in categories]


def validate_task_form(form):
    """Validate and clean form data from add/edit pages."""
    title = form.get("title", "").strip()
    description = form.get("description", "").strip()
    category = form.get("category", "General").strip() or "General"
    priority = form.get("priority", "Medium")
    status = form.get("status", "todo")
    due_date = form.get("due_date", "").strip()

    errors = []

    if not title:
        errors.append("Task title is required.")

    if priority not in PRIORITIES:
        errors.append("Invalid priority selected.")

    if status not in STATUSES:
        errors.append("Invalid status selected.")

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Due date must be a real date.")

    cleaned = {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": status,
        "due_date": due_date,
    }

    return cleaned, errors


@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "all")
    priority = request.args.get("priority", "all")
    category = request.args.get("category", "all")

    query = "SELECT * FROM tasks WHERE 1 = 1"
    params = []

    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR category LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    if status in STATUSES:
        query += " AND status = ?"
        params.append(status)

    if priority in PRIORITIES:
        query += " AND priority = ?"
        params.append(priority)

    if category != "all":
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY CASE status WHEN 'doing' THEN 1 WHEN 'todo' THEN 2 ELSE 3 END, due_date = '', due_date ASC, id DESC"

    connection = get_db_connection()
    tasks = connection.execute(query, params).fetchall()
    stats = {
        "total": connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
        "todo": connection.execute("SELECT COUNT(*) FROM tasks WHERE status = 'todo'").fetchone()[0],
        "doing": connection.execute("SELECT COUNT(*) FROM tasks WHERE status = 'doing'").fetchone()[0],
        "done": connection.execute("SELECT COUNT(*) FROM tasks WHERE status = 'done'").fetchone()[0],
    }
    connection.close()

    return render_template(
        "index.html",
        tasks=tasks,
        stats=stats,
        priorities=PRIORITIES,
        statuses=STATUSES,
        categories=get_filter_options(),
        selected={
            "search": search,
            "status": status,
            "priority": priority,
            "category": category,
        },
        today=date.today().isoformat(),
    )


@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        cleaned, errors = validate_task_form(request.form)

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "task_form.html",
                page_title="Add Task",
                task=cleaned,
                priorities=PRIORITIES,
                statuses=STATUSES,
                form_action=url_for("add_task"),
            )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        completed_at = now if cleaned["status"] == "done" else None

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO tasks
            (title, description, category, priority, status, due_date, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cleaned["title"],
                cleaned["description"],
                cleaned["category"],
                cleaned["priority"],
                cleaned["status"],
                cleaned["due_date"],
                now,
                completed_at,
            ),
        )
        connection.commit()
        connection.close()

        flash("Task added successfully.", "success")
        return redirect(url_for("index"))

    return render_template(
        "task_form.html",
        page_title="Add Task",
        task={"priority": "Medium", "status": "todo", "category": "General"},
        priorities=PRIORITIES,
        statuses=STATUSES,
        form_action=url_for("add_task"),
    )


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = fetch_task(task_id)
    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        cleaned, errors = validate_task_form(request.form)

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "task_form.html",
                page_title="Edit Task",
                task={**cleaned, "id": task_id},
                priorities=PRIORITIES,
                statuses=STATUSES,
                form_action=url_for("edit_task", task_id=task_id),
            )

        completed_at = task["completed_at"]
        if cleaned["status"] == "done" and not completed_at:
            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif cleaned["status"] != "done":
            completed_at = None

        connection = get_db_connection()
        connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, category = ?, priority = ?, status = ?, due_date = ?, completed_at = ?
            WHERE id = ?
            """,
            (
                cleaned["title"],
                cleaned["description"],
                cleaned["category"],
                cleaned["priority"],
                cleaned["status"],
                cleaned["due_date"],
                completed_at,
                task_id,
            ),
        )
        connection.commit()
        connection.close()

        flash("Task updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template(
        "task_form.html",
        page_title="Edit Task",
        task=task,
        priorities=PRIORITIES,
        statuses=STATUSES,
        form_action=url_for("edit_task", task_id=task_id),
    )


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    task = fetch_task(task_id)
    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    new_status = "todo" if task["status"] == "done" else "done"
    completed_at = None if new_status != "done" else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_db_connection()
    connection.execute(
        "UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?",
        (new_status, completed_at, task_id),
    )
    connection.commit()
    connection.close()

    flash("Task status updated.", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = fetch_task(task_id)
    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    connection = get_db_connection()
    connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()

    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.route("/kanban")
def kanban():
    connection = get_db_connection()
    todo_tasks = connection.execute("SELECT * FROM tasks WHERE status = 'todo' ORDER BY id DESC").fetchall()
    doing_tasks = connection.execute("SELECT * FROM tasks WHERE status = 'doing' ORDER BY id DESC").fetchall()
    done_tasks = connection.execute("SELECT * FROM tasks WHERE status = 'done' ORDER BY completed_at DESC, id DESC").fetchall()
    connection.close()

    return render_template(
        "kanban.html",
        columns=[
            ("To Do", "todo", todo_tasks),
            ("In Progress", "doing", doing_tasks),
            ("Done", "done", done_tasks),
        ],
        today=date.today().isoformat(),
    )


@app.route("/move/<int:task_id>/<status>", methods=["POST"])
def move_task(task_id, status):
    if status not in STATUSES:
        flash("Invalid status.", "danger")
        return redirect(url_for("kanban"))

    task = fetch_task(task_id)
    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("kanban"))

    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "done" else None

    connection = get_db_connection()
    connection.execute("UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?", (status, completed_at, task_id))
    connection.commit()
    connection.close()

    flash("Task moved.", "success")
    return redirect(url_for("kanban"))


@app.route("/reflection")
def reflection():
    return render_template("reflection.html")


@app.route("/api/tasks")
def api_tasks():
    connection = get_db_connection()
    tasks = connection.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    connection.close()
    return jsonify([dict(task) for task in tasks])


@app.route("/api/tasks/<int:task_id>")
def api_task_detail(task_id):
    task = fetch_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(dict(task))


if __name__ == "__main__":
    init_db()
    seed_db()
    app.run(debug=True)
