import tkinter as tk
import random
import math
import colorsys

class HarmonicOrganicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VENTENVS HARMONIC GEN")
        self.root.configure(bg="black") 

        self.win_size = 600
        self.border_width = 30
        self.canvas = tk.Canvas(root, width=self.win_size, height=self.win_size, highlightthickness=0, bd=0)
        self.canvas.pack(padx=self.border_width, pady=self.border_width)

        self.btn = tk.Button(root, text="GENERATE HARMONIC COMP", command=self.generate, bg="#222", fg="white", font=("Courier", 12, "bold"))
        self.btn.pack(pady=(0, 20))
        self.generate()

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)

    def get_harmonic_modifier(self, bg_rgb):
        """Calculates 50% of the red prop of (Background Complement + 7 degrees)"""
        # 1. Get Complement
        comp_rgb = (255 - bg_rgb[0], 255 - bg_rgb[1], 255 - bg_rgb[2])
        
        # 2. Shift Hue by 7 degrees (7/360 approx 0.0194)
        r, g, b = [x/255.0 for x in comp_rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = (h + (25/360.0)) % 1.0
        
        # 3. Back to RGB to get the new Red proportion
        new_r, _, _ = colorsys.hsv_to_rgb(h, s, v)
        
        # 4. Return 50% of that red value (scaled back to 0-255)
        return (new_r * 255) * 0.5

    def generate_single_shape(self, base_rgb, modifier, cx, cy, base_r):
        # Apply the red modifier to the shape's original color
        final_rgb = (base_rgb[0] + modifier, base_rgb[1] + modifier, base_rgb[2] + modifier)
        shape_hex = self.rgb_to_hex(final_rgb)
        
        num_points = random.randint(6, 10)
        points = []
        for i in range(num_points):
            angle = (i * 2 * math.pi) / num_points
            r = base_r * random.uniform(0.6, 1.4)
            points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])

        self.canvas.create_polygon(points, fill=shape_hex, smooth=True, splinesteps=40)

    def generate(self):
        self.canvas.delete("all")
        
        # 1. Random Background
        bg_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.canvas.config(bg=self.rgb_to_hex(bg_rgb))

        # 2. Calculate the global harmonic modifier
        red_modifier = self.get_harmonic_modifier(bg_rgb)

        # 3. Generate 3 Shapes with the modifier applied
        sizes = [(160, 200), (90, 130), (50, 80)]
        for min_r, max_r in sizes:
            s_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cx = random.randint(150, 450)
            cy = random.randint(150, 450)
            self.generate_single_shape(s_rgb, red_modifier, cx, cy, random.randint(min_r, max_r))

if __name__ == "__main__":
    root = tk.Tk()
    app = HarmonicOrganicApp(root)
    root.mainloop()