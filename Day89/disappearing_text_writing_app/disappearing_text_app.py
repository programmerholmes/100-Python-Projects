"""
Disappearing Text Writing App
-----------------------------
A desktop writing app inspired by The Most Dangerous Writing App.

Rule:
If the user stops typing for more than 5 seconds, everything they wrote disappears.

Controls:
- Start Session: begins a new dangerous writing session.
- Pause: pauses the timer and typing area.
- Restart: clears the text and starts over.
- Safe Exit: closes the program.

This app uses Tkinter only, so no extra packages are required.
"""

import os
import sys
import time
import tkinter as tk
from tkinter import messagebox


# ---------------------------------------------------------
# Tkinter path fix for some Windows/PyCharm installations.
# This is useful for Python 3.13 setups where Tkinter cannot
# find init.tcl automatically.
# ---------------------------------------------------------
def configure_tcl_tk_paths():
    possible_roots = [
        sys.base_prefix,
        sys.prefix,
        os.path.dirname(os.path.dirname(sys.executable)),
    ]

    for root in possible_roots:
        tcl_library = os.path.join(root, "tcl", "tcl8.6")
        tk_library = os.path.join(root, "tcl", "tk8.6")

        if os.path.exists(os.path.join(tcl_library, "init.tcl")):
            os.environ["TCL_LIBRARY"] = tcl_library

            if os.path.exists(os.path.join(tk_library, "tk.tcl")):
                os.environ["TK_LIBRARY"] = tk_library

            return


configure_tcl_tk_paths()


# ---------------------------------------------------------
# Main app class
# ---------------------------------------------------------
class DisappearingTextApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Disappearing Text Writing App")
        self.window.geometry("900x650")
        self.window.minsize(760, 560)
        self.window.config(bg="#101820")

        # Main settings
        self.max_idle_seconds = 5
        self.warning_seconds = 3

        # State variables
        self.session_active = False
        self.paused = False
        self.text_deleted = False
        self.last_key_time = None
        self.after_id = None

        self.build_layout()
        self.reset_interface()

    # -----------------------------------------------------
    # GUI layout
    # -----------------------------------------------------
    def build_layout(self):
        self.title_label = tk.Label(
            self.window,
            text="Disappearing Text Writing App",
            font=("Helvetica", 24, "bold"),
            fg="#FEE715",
            bg="#101820",
        )
        self.title_label.pack(pady=(18, 6))

        self.subtitle_label = tk.Label(
            self.window,
            text="Keep typing. Stop for more than 5 seconds and your writing disappears.",
            font=("Helvetica", 12),
            fg="white",
            bg="#101820",
        )
        self.subtitle_label.pack(pady=(0, 12))

        self.info_frame = tk.Frame(self.window, bg="#101820")
        self.info_frame.pack(fill="x", padx=30)

        self.timer_label = tk.Label(
            self.info_frame,
            text="Time left: 5.0s",
            font=("Helvetica", 16, "bold"),
            fg="#9BE7FF",
            bg="#101820",
        )
        self.timer_label.pack(side="left")

        self.stats_label = tk.Label(
            self.info_frame,
            text="Words: 0 | Characters: 0",
            font=("Helvetica", 12),
            fg="white",
            bg="#101820",
        )
        self.stats_label.pack(side="right")

        self.progress_canvas = tk.Canvas(
            self.window,
            height=18,
            bg="#1E2A36",
            highlightthickness=0,
        )
        self.progress_canvas.pack(fill="x", padx=30, pady=12)

        self.text_box = tk.Text(
            self.window,
            wrap="word",
            font=("Georgia", 15),
            padx=16,
            pady=16,
            bg="#F9F7F0",
            fg="#222222",
            insertbackground="#222222",
            relief="flat",
            undo=True,
        )
        self.text_box.pack(fill="both", expand=True, padx=30, pady=(0, 12))
        self.text_box.bind("<KeyRelease>", self.on_key_release)

        self.button_frame = tk.Frame(self.window, bg="#101820")
        self.button_frame.pack(pady=(0, 16))

        self.start_button = tk.Button(
            self.button_frame,
            text="Start Session",
            font=("Helvetica", 12, "bold"),
            width=14,
            command=self.start_session,
            bg="#FEE715",
            fg="#101820",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.start_button.grid(row=0, column=0, padx=8)

        self.pause_button = tk.Button(
            self.button_frame,
            text="Pause",
            font=("Helvetica", 12, "bold"),
            width=14,
            command=self.toggle_pause,
            bg="#9BE7FF",
            fg="#101820",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.pause_button.grid(row=0, column=1, padx=8)

        self.restart_button = tk.Button(
            self.button_frame,
            text="Restart",
            font=("Helvetica", 12, "bold"),
            width=14,
            command=self.restart_session,
            bg="#FFFFFF",
            fg="#101820",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.restart_button.grid(row=0, column=2, padx=8)

        self.exit_button = tk.Button(
            self.button_frame,
            text="Safe Exit",
            font=("Helvetica", 12, "bold"),
            width=14,
            command=self.safe_exit,
            bg="#FF6B6B",
            fg="white",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.exit_button.grid(row=0, column=3, padx=8)

        self.message_label = tk.Label(
            self.window,
            text="Press Start Session when you are ready.",
            font=("Helvetica", 12, "italic"),
            fg="#DDE6ED",
            bg="#101820",
        )
        self.message_label.pack(pady=(0, 14))

    # -----------------------------------------------------
    # App controls
    # -----------------------------------------------------
    def reset_interface(self):
        self.session_active = False
        self.paused = False
        self.text_deleted = False
        self.last_key_time = None

        if self.after_id is not None:
            self.window.after_cancel(self.after_id)
            self.after_id = None

        self.text_box.config(state="disabled")
        self.pause_button.config(state="disabled", text="Pause")
        self.draw_progress_bar(1.0, "#9BE7FF")
        self.timer_label.config(text="Time left: 5.0s", fg="#9BE7FF")
        self.update_stats()

    def start_session(self):
        self.session_active = True
        self.paused = False
        self.text_deleted = False
        self.last_key_time = time.time()

        self.text_box.config(state="normal")
        self.text_box.focus_set()
        self.pause_button.config(state="normal", text="Pause")
        self.message_label.config(text="Write now. Every key press resets the 5-second timer.", fg="#DDE6ED")

        self.update_countdown()

    def restart_session(self):
        answer = messagebox.askyesno(
            "Restart Session",
            "Restarting will clear your current writing. Do you want to continue?",
        )

        if answer:
            self.text_box.config(state="normal")
            self.text_box.delete("1.0", "end")
            self.start_session()
            self.update_stats()

    def toggle_pause(self):
        if not self.session_active or self.text_deleted:
            return

        self.paused = not self.paused

        if self.paused:
            self.text_box.config(state="disabled")
            self.pause_button.config(text="Resume")
            self.message_label.config(text="Paused. The countdown is stopped.", fg="#FEE715")
        else:
            self.text_box.config(state="normal")
            self.text_box.focus_set()
            self.pause_button.config(text="Pause")
            self.last_key_time = time.time()
            self.message_label.config(text="Resumed. Keep typing.", fg="#DDE6ED")
            self.update_countdown()

    def safe_exit(self):
        self.window.destroy()

    # -----------------------------------------------------
    # Typing and countdown logic
    # -----------------------------------------------------
    def on_key_release(self, event=None):
        if not self.session_active or self.paused or self.text_deleted:
            return

        # Ignore keys that do not represent actual writing/editing.
        ignored_keys = {
            "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
            "Caps_Lock", "Left", "Right", "Up", "Down", "Home", "End",
            "Prior", "Next", "Escape",
        }

        if event is not None and event.keysym in ignored_keys:
            return

        self.last_key_time = time.time()
        self.message_label.config(text="Good. Keep going.", fg="#DDE6ED")
        self.update_stats()

    def update_countdown(self):
        if not self.session_active or self.paused or self.text_deleted:
            return

        if self.last_key_time is None:
            self.last_key_time = time.time()

        idle_time = time.time() - self.last_key_time
        time_left = self.max_idle_seconds - idle_time

        if time_left <= 0:
            self.delete_everything()
            return

        percentage_left = time_left / self.max_idle_seconds

        if time_left <= self.warning_seconds:
            color = "#FF6B6B"
            self.timer_label.config(fg=color)
            self.message_label.config(text="Warning: type something or your text will disappear!", fg=color)
        else:
            color = "#9BE7FF"
            self.timer_label.config(fg=color)

        self.timer_label.config(text=f"Time left: {time_left:.1f}s")
        self.draw_progress_bar(percentage_left, color)

        self.after_id = self.window.after(100, self.update_countdown)

    def delete_everything(self):
        self.text_deleted = True
        self.session_active = False
        self.paused = False

        self.text_box.config(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.config(state="disabled")

        self.pause_button.config(state="disabled", text="Pause")
        self.timer_label.config(text="Time left: 0.0s", fg="#FF6B6B")
        self.draw_progress_bar(0, "#FF6B6B")
        self.update_stats()

        # Simple system bell. It is optional and does not require extra files.
        self.window.bell()

        self.message_label.config(
            text="Too slow. Your writing disappeared. Press Start Session to try again.",
            fg="#FF6B6B",
        )

    # -----------------------------------------------------
    # Display helpers
    # -----------------------------------------------------
    def update_stats(self):
        text = self.text_box.get("1.0", "end-1c")
        words = len(text.split())
        characters = len(text)
        self.stats_label.config(text=f"Words: {words} | Characters: {characters}")

    def draw_progress_bar(self, percentage_left, color):
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()

        if width <= 1:
            width = 820

        fill_width = width * max(0, min(percentage_left, 1))

        self.progress_canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill="#1E2A36",
            outline="",
        )
        self.progress_canvas.create_rectangle(
            0,
            0,
            fill_width,
            height,
            fill=color,
            outline="",
        )


# ---------------------------------------------------------
# Run the app
# ---------------------------------------------------------
def main():
    window = tk.Tk()
    app = DisappearingTextApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
