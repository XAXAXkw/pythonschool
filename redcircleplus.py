import tkinter as tk

# Create main window
window = tk.Tk()
window.title("Red Circle on Green Background")

# Canvas size
WIDTH = 400
HEIGHT = 400

# Create canvas with green background
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="#00ff00")
canvas.pack()

# Circle properties
radius = 100
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Track current background color
current_bg = "#00ff00"

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

# Function to compute complementary color
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    r = 255 - int(hex_color[0:2], 16)
    g = 255 - int(hex_color[2:4], 16)
    b = 255 - int(hex_color[4:6], 16)
    return f"#{r:02x}{g:02x}{b:02x}"

# Update circle size and color
def update_circle():
    canvas.coords(
        circle,
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius
    )
    # Update circle color to complementary of background
    comp_color = get_complementary(current_bg)
    canvas.itemconfig(circle, fill=comp_color)

# Function to shrink the circle
def shrink_circle():
    global radius
    if radius > 10:
        radius -= 10
        update_circle()

# Function to grow the circle
def grow_circle():
    global radius
    if radius < min(WIDTH, HEIGHT) // 2:
        radius += 10
        update_circle()

# Change background color using slider
def update_bg(value):
    global current_bg
    v = int(value)
    # Gradient from green to blue
    current_bg = f"#00{v:02x}{(255 - v):02x}"
    canvas.config(bg=current_bg)

# Frame for controls
frame = tk.Frame(window)
frame.pack(pady=10)

# Label
label = tk.Label(frame, text="whats ya name?")
label.pack()

# Entry field
entry = tk.Entry(frame)
entry.pack()

# Buttons
shrink_btn = tk.Button(frame, text="Shrink Circle", command=shrink_circle)
shrink_btn.pack(pady=2)

grow_btn = tk.Button(frame, text="Grow Circle", command=grow_circle)
grow_btn.pack(pady=2)

# Slider for background color
slider = tk.Scale(frame, from_=0, to=255, orient="horizontal", label="Background Color", command=update_bg)
slider.pack(pady=5)

# Run the application
window.mainloop()