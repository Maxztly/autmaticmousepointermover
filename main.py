import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic Mouse Mover")
        root.iconbitmap("pointer.ico")

        window_width = 300
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.is_running = False
        self.move_distance = 50  
        self.start_button_text = "Start"

        self.timer_label = tk.Label(root, text="Timer: 00:00:00", font=("Helvetica", 16))
        self.timer_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.distance_var = tk.StringVar()
        self.distance_var.set("Medium")

        self.distance_menu = ttk.Combobox(root, textvariable=self.distance_var, values=["Small", "Medium", "Large"], state="readonly")
        self.distance_menu.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.distance_menu.bind("<<ComboboxSelected>>", self.set_move_distance)

        self.start_button = tk.Button(root, text=self.start_button_text, command=self.start_movement)
        self.start_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Configure rows and columns to expand with window resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        self.timer_thread = None
        self.seconds = 0

        self.root.bind("<Escape>", self.stop_movement)

    def start_movement(self):
        if not self.is_running:
            self.is_running = True
            self.start_button_text = "Press ESC to exit"
            self.start_button.config(text=self.start_button_text)
            self.seconds = 0  # Reset the timer
            self.start_movement_thread()
            self.update_timer()

    def start_movement_thread(self):
        threading.Thread(target=self.move_mouse).start()

    def move_mouse(self):
        while self.is_running:
            pyautogui.move(self.move_distance, 0, duration=0.5)
            pyautogui.move(-self.move_distance, 0, duration=0.5)

    def update_timer(self):
        while self.is_running:
            hours = self.seconds // 3600
            minutes = (self.seconds // 60) % 60
            seconds = self.seconds % 60
            timer_text = f"Timer: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=timer_text)
            self.root.update()
            time.sleep(1)
            self.seconds += 1

    def stop_movement(self, event):
        if self.is_running:
            self.is_running = False
            self.start_button_text = "Start"
            self.start_button.config(text=self.start_button_text)

    def set_move_distance(self, event):
        selection = self.distance_var.get()
        if selection == "Small":
            self.move_distance = 20
        elif selection == "Medium":
            self.move_distance = 50
        elif selection == "Large":
            self.move_distance = 100

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()
