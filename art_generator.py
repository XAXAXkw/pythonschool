import tkinter as tk
import random
import math
import colorsys

class FibonacciCanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VENTENVS TEXTILE-PHI")
        
        # 1. Dark Style
        self.bg_dark = "#121212"
        self.btn_dark = "#2C2C2C"
        self.text_light = "#E0E0E0"
        self.accent = "#FFFF00"
        self.root.configure(bg=self.bg_dark)
        
        # 2. Dimensions
        self.canvas_w = 350
        self.canvas_h = 500
        self.phi = 1.618

        # 3. UI Layout
        self.canvas = tk.Canvas(
            root, width=self.canvas_w, height=self.canvas_h,
            highlightthickness=2, highlightbackground=self.accent, 
            bd=0, bg=self.bg_dark
        )
        self.canvas.pack(padx=20, pady=20)

        # Control Frame for Slider
        self.ctrl_frame = tk.Frame(root, bg=self.bg_dark)
        self.ctrl_frame.pack(fill="x", padx=40)

        tk.Label(self.ctrl_frame, text="PRIMARY SHAPE SCALE (%)", 
                 fg=self.accent, bg=self.bg_dark, font=("Consolas", 9)).pack()

        self.scale_var = tk.DoubleVar(value=60)
        self.slider = tk.Scale(
            self.ctrl_frame, from_=10, to=90, orient="horizontal",
            variable=self.scale_var, bg=self.bg_dark, fg=self.text_light,
            troughcolor=self.btn_dark, highlightthickness=0,
            command=lambda x: self.generate() 
        )
        self.slider.pack(fill="x", pady=5)

        self.btn = tk.Button(
            root, text="NEWARTWORK", command=self.generate,
            bg=self.btn_dark, fg=self.text_light,
            activebackground=self.accent, font=("Consolas", 10, "bold"),
            relief="flat", padx=30, pady=10
        )
        self.btn.pack(pady=20)

        self.generate()

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)

    def apply_canvas_texture(self, base_rgb):
        """Creates a woven textile effect using micro-lines"""
        # Vertical threads
        for x in range(0, self.canvas_w, 2):
            # Subtle jitter in color to simulate thread depth
            shade = random.randint(-10, 10)
            color = self.rgb_to_hex((base_rgb[0]+shade, base_rgb[1]+shade, base_rgb[2]+shade))
            self.canvas.create_line(x, 0, x, self.canvas_h, fill=color, stipple="gray25")
        
        # Horizontal threads
        for y in range(0, self.canvas_h, 2):
            shade = random.randint(-8, 8)
            color = self.rgb_to_hex((base_rgb[0]+shade, base_rgb[1]+shade, base_rgb[2]+shade))
            self.canvas.create_line(0, y, self.canvas_w, y, fill=color, stipple="gray12")

    def get_harmonic_modifier(self, bg_rgb):
        comp_rgb = (255 - bg_rgb[0], 255 - bg_rgb[1], 255 - bg_rgb[2])
        r, g, b = [x/255.0 for x in comp_rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + (7/360.0)) % 1.0
        new_r, _, _ = colorsys.hsv_to_rgb(h, s, v)
        return (new_r * 255) * 0.5

    def generate_single_shape(self, base_rgb, modifier, cx, cy, radius):
        final_rgb = (base_rgb[0] + modifier, base_rgb[1] + modifier, base_rgb[2] + modifier)
        shape_hex = self.rgb_to_hex(final_rgb)
        
        num_points = random.randint(12, 18)
        points = []
        for i in range(num_points):
            angle = (i * 2 * math.pi) / num_points
            r_var = radius * random.uniform(0.7, 1.3)
            points.extend([cx + r_var * math.cos(angle), cy + r_var * math.sin(angle)])

        # The shape is drawn on top of the background texture
        self.canvas.create_polygon(points, fill=shape_hex, smooth=True, splinesteps=60)

    def generate(self, _=None):
        self.canvas.delete("all")
        
        # 1. Background & Texture
        bg_rgb = (random.randint(40, 215), random.randint(40, 215), random.randint(40, 215))
        self.canvas.config(bg=self.rgb_to_hex(bg_rgb))
        self.apply_canvas_texture(bg_rgb) # Add the textile weave
        
        red_mod = self.get_harmonic_modifier(bg_rgb)

        # 2. Fibonacci Sizing
        percentage = self.scale_var.get() / 100.0
        base_large = (self.canvas_w / 2) * percentage * 1.5 
        base_medium = base_large / self.phi
        base_small = base_medium / self.phi

        # 3. Composition with 50% Bleed
        composition = [(base_large, 0.1, 0.4), (base_medium, 0.35, 0.65), (base_small, 0.6, 0.9)]

        for radius, y_min, y_max in composition:
            s_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cx = random.randint(0, self.canvas_w)
            cy = random.randint(int(self.canvas_h * y_min), int(self.canvas_h * y_max))
            self.generate_single_shape(s_rgb, red_mod, cx, cy, radius)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x800")
    app = FibonacciCanvasApp(root)
    root.mainloop()