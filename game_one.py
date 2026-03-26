import tkinter as tk
import random
import math

class GameWorld:
    def __init__(self, root):
        self.root = root
        self.root.title("VENTENVS: THE WALKER")
        
        # 1. Canvas Setup
        self.width = 800
        self.height = 600
        self.sky_height = 100
        self.buffer = 10 
        
        self.canvas = tk.Canvas(
            root, width=self.width, height=self.height,
            bg="#8DB600", highlightthickness=0
        )
        self.canvas.pack()

        # 2. Game Entities & Animation State
        self.player_pos = [400, 350] 
        self.speed = 4
        self.keys = {}
        self.walk_timer = 0 
        
        # 3. Cloud System
        self.clouds = []
        for _ in range(6):
            self.clouds.append([
                random.randint(0, 800), 
                random.randint(10, 70), 
                random.uniform(0.3, 0.8),
                random.randint(30, 50)
            ])

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.update()

    def key_down(self, event):
        self.keys[event.keysym.lower()] = True

    def key_up(self, event):
        self.keys[event.keysym.lower()] = False

    def move_entities(self):
        moving = False
        if self.keys.get('w'): self.player_pos[1] -= self.speed; moving = True
        if self.keys.get('s'): self.player_pos[1] += self.speed; moving = True
        if self.keys.get('a'): self.player_pos[0] -= self.speed; moving = True
        if self.keys.get('d'): self.player_pos[0] += self.speed; moving = True

        if moving:
            self.walk_timer += 0.25 
        else:
            self.walk_timer = 0 

        # Boundaries
        self.player_pos[0] = max(5, min(795, self.player_pos[0]))
        north_limit = self.sky_height + 10 + self.buffer
        self.player_pos[1] = max(north_limit, min(590, self.player_pos[1]))

        for cloud in self.clouds:
            cloud[0] -= cloud[2]
            if cloud[0] < -60:
                cloud[0] = 850
                cloud[1] = random.randint(10, 70)

    def render(self):
        self.canvas.delete("all")
        
        # 1. Sky & Clouds
        self.canvas.create_rectangle(0, 0, 800, self.sky_height, fill="#40E0D0", outline="")
        for x, y, _, w in self.clouds:
            self.canvas.create_oval(x, y, x + w, y + (w/2.5), fill="#FFFFFF", outline="", stipple="gray50")

        # 2. Animation Calculations
        cx, base_cy = self.player_pos
        bob = math.sin(self.walk_timer * 2) * 2 if self.walk_timer > 0 else 0
        cy = base_cy + bob
        
        # Swing logic
        swing = math.sin(self.walk_timer) * 6
        arm_swing = math.sin(self.walk_timer) * 5
        leg_len = 12
        arm_len = 8

        # 3. Dark Green Shadow
        self.canvas.create_oval(
            cx - 25, base_cy + 18, cx + 5, base_cy + 24, 
            fill="#1B3022", outline="", stipple="gray50"
        )
        
        # 4. Animated Legs
        self.canvas.create_line(cx - 2, cy + 10, cx - 2 + swing, cy + 10 + leg_len, fill="#000000", width=1)
        self.canvas.create_line(cx + 2, cy + 10, cx + 2 - swing, cy + 10 + leg_len, fill="#000000", width=1)
        
        # 5. Animated Arms
        self.canvas.create_line(cx - 5, cy - 2, cx - 8 - arm_swing, cy + arm_len, fill="#000000", width=1)
        self.canvas.create_line(cx + 5, cy - 2, cx + 8 + arm_swing, cy + arm_len, fill="#000000", width=1)

        # 6. Player Body
        self.canvas.create_rectangle(cx - 5, cy - 10, cx + 5, cy + 10, fill="#FF0000", outline="")
        self.canvas.create_rectangle(cx - 5, cy - 10, cx + 5, cy - 7, fill="#000000", outline="") # Black Hat
        self.canvas.create_rectangle(cx - 5, cy + 7, cx + 5, cy + 10, fill="#FFFFFF", outline="") # White Trim

    def update(self):
        self.move_entities()
        self.render()
        self.root.after(16, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameWorld(root)
    root.mainloop()