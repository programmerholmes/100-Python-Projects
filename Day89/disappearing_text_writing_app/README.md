# Disappearing Text Writing App

This is a desktop writing app built with Python and Tkinter.

The idea is simple: the user must keep writing. If they stop typing for more than 5 seconds, everything they wrote disappears.

## Features

- Desktop GUI built with Tkinter
- Large writing area
- 5-second inactivity countdown
- Countdown resets whenever the user types
- Text is automatically deleted when time runs out
- Live word count and character count
- Warning message when time is almost gone
- Start, pause, restart, and exit buttons
- No external Python packages required

## How to run

Open a terminal in this folder and run:

```bash
python disappearing_text_app.py
```

Or on Windows, double-click:

```text
run_windows.bat
```

## Controls

- **Start Session**: starts the dangerous writing session
- **Pause**: pauses the countdown and disables the text box
- **Restart**: clears the current writing and starts again
- **Safe Exit**: closes the app

## Project notes

This project uses Tkinter's `after()` method to check the timer every 100 milliseconds. Every key press updates `last_key_time`. If the difference between the current time and the last key time becomes greater than 5 seconds, the text box is cleared.
