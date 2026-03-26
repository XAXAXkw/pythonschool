import tkinter as tk

# Create main window
window = tk.Tk()
window.title("Red Circle on Green Background")

# Canvas size
WIDTH = 400
HEIGHT = 400

# Create canvas with green background
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="green")
canvas.pack()

# Circle properties
radius = 100
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Draw red circle
canvas.create_oval(
    center_x - radius,
    center_y - radius,
    center_x + radius,
    center_y + radius,
    fill="red"
)

# Run the application
window.mainloop()
