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

# Draw circle and keep reference
circle = canvas.create_oval(
    center_x - radius,
    center_y - radius,
    center_x + radius,
    center_y + radius,
    fill="red"
)

# Add text inside the circle
text = canvas.create_text(
    center_x,
    center_y,
    text="Hellow",
    fill="white",
    font=("Arial", 16, "bold")
)

# Function to shrink the circle
def shrink_circle():
    global radius
    if radius > 10:  # prevent disappearing completely
        radius -= 10
        canvas.coords(
            circle,
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        )

# Frame for input section
frame = tk.Frame(window)
frame.pack(pady=10)

# Label
label = tk.Label(frame, text="whats ya name?")
label.pack()

# Entry field
entry = tk.Entry(frame)
entry.pack()

# Button to shrink circle
button = tk.Button(frame, text="Shrink Circle", command=shrink_circle)
button.pack(pady=5)

# Run the application
window.mainloop()