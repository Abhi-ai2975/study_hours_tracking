import tkinter as tk
from datetime import datetime
import json
import os
import sys

# Import config and storage to read data
from src.config import DATA_FILE
from src.storage import load_data, seconds_to_str

class StudyWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Study Hours")
        self.attributes("-topmost", True)  # Always on top
        self.overrideredirect(True)       # Frameless
        
        # Dark theme colors (Catppuccin Mocha inspired)
        self.bg_color = "#1E1E2E"
        self.fg_color = "#CDD6F4"
        self.accent_color = "#89B4FA"
        
        self.configure(bg="#000000") # Dark background for the corners
        try:
            self.wm_attributes("-transparentcolor", "#000000")
        except tk.TclError:
            pass # Not supported on all Linux distros, will just fall back to a black background
        
        # Dimensions for the widget
        width, height = 220, 50
        
        # Create a Canvas instead of a Frame for drawing shapes
        self.canvas = tk.Canvas(self, width=width, height=height, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw a rounded rectangle (pill shape)
        radius = 20
        self.create_rounded_rectangle(0, 0, width, height, radius, fill=self.bg_color, outline=self.accent_color, width=2)
        
        # Label to show time (placed on the canvas)
        self.time_label = tk.Label(self, text="Loading...", font=("Segoe UI", 12, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.time_label.place(relx=0.1, rely=0.5, anchor=tk.W)
        
        # Close button (placed on the canvas)
        self.close_btn = tk.Label(self, text="×", font=("Segoe UI", 14, "bold"), bg=self.bg_color, fg="#F38BA8", cursor="hand2")
        self.close_btn.place(relx=0.9, rely=0.5, anchor=tk.E)
        self.close_btn.bind("<Button-1>", lambda e: self.destroy())
        
        # Binding for dragging the window (bind to canvas and labels)
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

        
        self.time_label.bind("<ButtonPress-1>", self.start_move)
        self.time_label.bind("<ButtonRelease-1>", self.stop_move)
        self.time_label.bind("<B1-Motion>", self.do_move)
        
        self.x = 0
        self.y = 0
        
        # Position initially at bottom right (guess based on 1080p)
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cood = int(screen_width - 200)
        y_cood = int(screen_height - 150)
        self.geometry(f"+{x_cood}+{y_cood}")
        
        self.update_data()
        
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        if self.x is not None and self.y is not None:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f"+{x}+{y}")
            
    def update_data(self):
        try:
            data = load_data()
            current_date = datetime.now().strftime("%Y-%m-%d")
            seconds = data.get(current_date, 0)
            self.time_label.config(text=f"⏱️ {seconds_to_str(seconds)}")
        except Exception as e:
            self.time_label.config(text="Error")
            print(f"Error loading data: {e}")
            
        # Refresh every 5 seconds
        self.after(5000, self.update_data)

if __name__ == "__main__":
    app = StudyWidget()
    app.mainloop()
