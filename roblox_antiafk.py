import time
import tkinter as tk

import pydirectinput


STEPS = [
    ("w", 2),
    ("s", 2),
    (None, 30),
]
START_DELAY = 5 

pydirectinput.PAUSE = 0


class App:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.held = None
        self.step = 0
        self.step_end = 0.0

        root.title("Key Presser")
        root.geometry("300x160")
        root.attributes("-topmost", True)
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.status = tk.Label(root, text="Stopped", font=("Segoe UI", 13))
        self.status.pack(pady=15)

        self.button = tk.Button(root, text="Start", width=14, height=2, command=self.toggle)
        self.button.pack()

    def toggle(self):
        self.stop() if self.running else self.start()

    def start(self):
        self.running = True
        self.step = len(STEPS) - 1
        self.step_end = time.perf_counter() + START_DELAY
        self.button.config(text="Stop")
        self.tick()

    def stop(self):
        self.running = False
        self.release()
        self.button.config(text="Start")
        self.status.config(text="Stopped")

    def release(self):
        if self.held:
            pydirectinput.keyUp(self.held)
            self.held = None

    def close(self):
        self.release()
        self.root.destroy()

    def tick(self):
        if not self.running:
            return
        now = time.perf_counter()

        if now >= self.step_end:
            self.release()
            self.step = (self.step + 1) % len(STEPS)
            key, seconds = STEPS[self.step]
            if key:
                pydirectinput.keyDown(key)
                self.held = key
            self.step_end = now + seconds

        left = max(0, self.step_end - now)
        if self.held:
            self.status.config(text=f"Holding {self.held.upper()} ({left:.1f}s left)")
        else:
            self.status.config(text=f"Break ({left:.0f}s left)")

        self.root.after(50, self.tick)


root = tk.Tk()
App(root)
root.mainloop()