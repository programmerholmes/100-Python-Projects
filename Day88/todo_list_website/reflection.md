# Reflection

I approached this project by first deciding what kind of todo list I wanted to build. Instead of only making a basic list where items can be crossed out, I built a more complete task manager with a normal list view and a Kanban-style board. I planned the app around the main actions a user would need: add, view, edit, complete, move, filter, and delete tasks.

The easiest part was understanding the basic idea of a todo list. Each task needs a title and a status, and those can be shown clearly on the page. Creating the HTML structure for task cards was also manageable.

The harder part was connecting everything together. The website needed routes, forms, validation, database queries, and templates. I had to think carefully about how each button should update the SQLite database and then redirect the user back to the correct page.

My biggest learning was that even a simple app has multiple layers. The frontend shows the user interface, Flask handles the routes, SQLite stores the data, and the templates connect the Python data to the HTML page.

If I did this project again, I would add user accounts, drag-and-drop cards, reminders, and maybe a dashboard that shows weekly productivity. I would also plan the database structure before writing the routes so the project is easier to expand later.
