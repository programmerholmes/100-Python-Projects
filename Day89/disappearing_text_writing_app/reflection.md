# Reflection

For this project, I approached the app by first breaking the problem into smaller parts. The main requirements were a text editor, a timer, and logic that checks whether the user has stopped typing. I decided to use Tkinter because it is built into Python and works well for simple desktop applications.

The easiest part was creating the basic window, labels, buttons, and text box. Tkinter makes it simple to place these elements on the screen. The harder part was making the countdown work properly without freezing the app. I used the `after()` method instead of a normal `while` loop because a loop would block the GUI from updating.

The biggest learning from this project was how event-driven programming works. Instead of the program running from top to bottom once, it waits for events like button clicks and key presses. Every time the user types, the app records the current time. Then the countdown function repeatedly checks how long it has been since the last key press.

If I improved this project later, I might add writing goals, different difficulty levels, session statistics, or a mode where the user has to write for a certain number of minutes to win. I could also improve the design with custom themes or add a safe practice mode where the text does not disappear.
