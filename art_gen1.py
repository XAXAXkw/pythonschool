import tkinter as tk
import random
import math
import colorsys

class FibonacciCanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VENTENVS PHI-STACK")
        
        # 1. Dark Style
        self.bg_dark = "#121212"
        self.btn_dark = "#2C2C2C"
        self.text_light = "#E0E0E0"
        self.accent = "#FFFF00"
        self.root.configure(bg=self.bg_dark)
        
        # 2. Dimensions & State
        self.canvas_w = 350
        self.canvas_h = 500
        self.phi = 1.618
        self.current_bg_rgb = (255, 255, 255)
        self.last_radius = 100 

        # 3. UI Layout
        self.canvas = tk.Canvas(
            root, width=self.canvas_w, height=self.canvas_h,
            highlightthickness=2, highlightbackground=self.accent, 
            bd=0, bg=self.bg_dark
        )
        self.canvas.pack(padx=20, pady=20)

        # Control Frame
        self.ctrl_frame = tk.Frame(root, bg=self.bg_dark)
        self.ctrl_frame.pack(fill="x", padx=40)

        # Slider
        tk.Label(self.ctrl_frame, text="BASE SCALE (%)", 
                 fg=self.accent, bg=self.bg_dark, font=("Consolas", 9)).pack()
        self.scale_var = tk.DoubleVar(value=60)
        self.slider = tk.Scale(
            self.ctrl_frame, from_=10, to=90, orient="horizontal",
            variable=self.scale_var, bg=self.bg_dark, fg=self.text_light,
            troughcolor=self.btn_dark, highlightthickness=0,
            command=lambda x: self.reset_artwork() 
        )
        self.slider.pack(fill="x", pady=5)

        # Button Frame
        self.btn_frame = tk.Frame(root, bg=self.bg_dark)
        self.btn_frame.pack(pady=20)

        self.btn_reset = tk.Button(
            self.btn_frame, text="NEWARTWORK", command=self.reset_artwork,
            bg=self.btn_dark, fg=self.text_light, width=15,
            activebackground=self.accent, font=("Consolas", 10, "bold"), relief="flat"
        )
        self.btn_reset.grid(row=0, column=0, padx=5)

        self.btn_add = tk.Button(
            self.btn_frame, text="ADD SHAPE", command=self.add_extra_shape,
            bg=self.btn_dark, fg=self.accent, width=15,
            activebackground=self.accent, font=("Consolas", 10, "bold"), relief="flat"
        )
        self.btn_add.grid(row=0, column=1, padx=5)

        self.reset_artwork()

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)

    def get_harmonic_modifier(self):
        comp_rgb = (255 - self.current_bg_rgb[0], 255 - self.current_bg_rgb[1], 255 - self.current_bg_rgb[2])
        r, g, b = [x/255.0 for x in comp_rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + (7/360.0)) % 1.0
        new_r, _, _ = colorsys.hsv_to_rgb(h, s, v)
        return (new_r * 255) * 0.5

    def draw_shape(self, radius, cx=None, cy=None):
        s_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        modifier = self.get_harmonic_modifier()
        final_rgb = (s_rgb[0] + modifier, s_rgb[1] + modifier, s_rgb[2] + modifier)
        
        if cx is None: cx = random.randint(0, self.canvas_w)
        if cy is None: cy = random.randint(0, self.canvas_h)
        
        num_points = random.randint(12, 18)
        points = []
        for i in range(num_points):
            angle = (i * 2 * math.pi) / num_points
            r_var = radius * random.uniform(0.7, 1.3)
            points.extend([cx + r_var * math.cos(angle), cy + r_var * math.sin(angle)])

        self.canvas.create_polygon(points, fill=self.rgb_to_hex(final_rgb), smooth=True, splinesteps=60)

    def reset_artwork(self, _=None):
        # Clears everything and starts fresh
        self.canvas.delete("all")
        self.current_bg_rgb = (random.randint(40, 215), random.randint(40, 215), random.randint(40, 215))
        self.canvas.config(bg=self.rgb_to_hex(self.current_bg_rgb))

        percentage = self.scale_var.get() / 100.0
        base_large = (self.canvas_w / 2) * percentage * 1.5 
        
        # Draw Initial 3 Fibonacci Shapes
        self.draw_shape(base_large, random.randint(0, self.canvas_w), random.randint(0, self.canvas_h))
        mid = base_large / self.phi
        self.draw_shape(mid, random.randint(0, self.canvas_w), random.randint(0, self.canvas_h))
        self.last_radius = mid / self.phi
        self.draw_shape(self.last_radius, random.randint(0, self.canvas_w), random.randint(0, self.canvas_h))

    def add_extra_shape(self):
        # Adds a new shape on TOP of existing ones
        self.last_radius = self.last_radius / self.phi
        if self.last_radius < 5: self.last_radius = 40 # Reset if too small
        self.draw_shape(self.last_radius)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x800")
    app = FibonacciCanvasApp(root)
    root.mainloop()