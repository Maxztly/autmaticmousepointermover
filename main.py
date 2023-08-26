import tkinter as tk
import pyautogui
import threading
import time

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Mover")

        # Fenstergröße und Position festlegen
        window_width = 300
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.is_running = False
        self.move_distance = 50  # Standardbewegungsentfernung

        self.timer_label = tk.Label(root, text="Timer: 0 seconds")
        self.timer_label.pack()

        self.distance_var = tk.StringVar()
        self.distance_var.set("Medium")

        self.distance_menu = tk.OptionMenu(root, self.distance_var, "Small", "Medium", "Large", command=self.set_move_distance)
        self.distance_menu.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_movement)
        self.start_button.pack()

        self.timer_thread = None
        self.seconds = 0

        self.root.bind("<Escape>", self.stop_movement)

    def start_movement(self):
        if not self.is_running:
            self.is_running = True
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
            self.seconds += 1
            self.timer_label.config(text=f"Timer: {self.seconds} seconds")
            self.root.update()
            time.sleep(1)

    def stop_movement(self, event):
        self.is_running = False

    def set_move_distance(self, selection):
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
