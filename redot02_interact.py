import tkinter as tk
import random
import colorsys

class RebelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VENTENVS CONTROL DECK")
        self.root.configure(bg="#1a1a1a")
        
        # 1. State Variables
        self.total_pool = 250   
        self.radius_a = 125     
        self.center_a = (250, 250)
        self.center_b = (100, 100)
        
        self.bg_rgb = (20, 40, 20) # Dark Start
        self.border_color = "#FFFF00"

        # 2. UI Setup
        self.canvas = tk.Canvas(
            root, width=500, height=500, 
            highlightthickness=10, 
            highlightbackground=self.border_color
        )
        self.canvas.pack(pady=20)

        # 3. Separate Button Rows
        self.control_frame = tk.Frame(root, bg="#1a1a1a")
        self.control_frame.pack(pady=10)

        # Row 1: Size Controls (Inverted)
        tk.Label(self.control_frame, text="DIMENSIONS:", fg="white", bg="#1a1a1a").grid(row=0, column=0, padx=10)
        tk.Button(self.control_frame, text="GROW A / SHRINK B", width=20, command=lambda: self.update_size(15)).grid(row=0, column=1, padx=5)
        tk.Button(self.control_frame, text="SHRINK A / GROW B", width=20, command=lambda: self.update_size(-15)).grid(row=0, column=2, padx=5)

        # Row 2: Color & Placement Controls
        tk.Label(self.control_frame, text="AESTHETICS:", fg="white", bg="#1a1a1a").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.control_frame, text="RANDOMIZE COLORS", width=20, bg="#444", fg="white", command=self.randomize_colors).grid(row=1, column=1, padx=5)
        tk.Button(self.control_frame, text="RANDOMIZE POSITIONS", width=20, bg="#444", fg="white", command=self.randomize_positions).grid(row=1, column=2, padx=5)

        self.randomize_colors()
        self.randomize_positions()

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(int(c) for c in rgb)

    def randomize_colors(self):
        """Full Hue Range (0 to 360 degrees)"""
        # Randomize background across full spectrum
        self.bg_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Circle A: Complementary
        self.circle_a_rgb = (255 - self.bg_rgb[0], 255 - self.bg_rgb[1], 255 - self.bg_rgb[2])
        
        # Circle B: Analogous (45 Degree shift)
        r, g, b = [x/255.0 for x in self.bg_rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + 0.125) % 1.0 
        self.circle_b_rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v))
        
        self.canvas.config(bg=self.rgb_to_hex(self.bg_rgb))
        self.draw_circles()

    def randomize_positions(self):
        """Moves circles without changing size or color"""
        self.center_a = (random.randint(100, 400), random.randint(100, 400))
        self.center_b = (random.randint(100, 400), random.randint(100, 400))
        self.draw_circles()

    def update_size(self, amount):
        """Inverted sizing: A increases, B decreases"""
        new_a = self.radius_a + amount
        if 20 <= new_a <= 230:
            self.radius_a = new_a
            self.draw_circles()

    def draw_circles(self):
        self.canvas.delete("all")
        # Draw B first so A (the complement) is on top if they overlap
        rb = self.total_pool - self.radius_a
        self.render_oval(self.center_b, rb, self.circle_b_rgb)
        self.render_oval(self.center_a, self.radius_a, self.circle_a_rgb)

    def render_oval(self, center, r, color_rgb):
        cx, cy = center
        x0, y0 = cx - r, cy - r
        x1, y1 = cx + r, cy + r
        self.canvas.create_oval(x0, y0, x1, y1, fill=self.rgb_to_hex(color_rgb), outline="")

if __name__ == "__main__":
    root = tk.Tk()
    app = RebelApp(root)
    root.mainloop()