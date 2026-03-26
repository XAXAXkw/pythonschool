import tkinter as tk
import random
import math
import time

# --- CONSTANTS & CONFIG ---
WIDTH, HEIGHT = 800, 600
SKY_COLOR = "#40E0D0"
GRASS_COLOR = "#8DB600"
ROMAN_RED = "#8B0000"

class Walker:
    """Handles all Player Visuals and Animations"""
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.pos = [x, y]
        self.arm_up = False
        self.shake = 0
        
        # Create persistent parts (Optimization: Create once, move later)
        self.shadow = canvas.create_oval(0,0,0,0, fill="#1B3022", outline="", stipple="gray50")
        self.leg_l = canvas.create_line(0,0,0,0, smooth=True, fill="black")
        self.leg_r = canvas.create_line(0,0,0,0, smooth=True, fill="black")
        self.arm_l = canvas.create_line(0,0,0,0, smooth=True, fill="black")
        self.arm_r = canvas.create_line(0,0,0,0, smooth=True, fill="black")
        self.body = canvas.create_rectangle(0,0,0,0, fill="red", outline="")
        self.head = canvas.create_rectangle(0,0,0,0, fill="black")
        self.belt = canvas.create_rectangle(0,0,0,0, fill="white")

    def update_animation(self, swing, arm_swing, bob):
        cx, cy = self.pos[0] + random.randint(-self.shake, self.shake), self.pos[1] + bob
        
        # Move Body Parts
        self.canvas.coords(self.shadow, cx-25, self.pos[1]+18, cx+5, self.pos[1]+24)
        self.canvas.coords(self.body, cx-5, cy-10, cx+5, cy+10)
        self.canvas.coords(self.head, cx-5, cy-10, cx+5, cy-7)
        self.canvas.coords(self.belt, cx-5, cy+7, cx+5, cy+10)
        
        # Update Curved Limbs
        self.draw_curve(self.leg_l, cx-2, cy+10, cx-2+swing, cy+24, swing*0.5)
        self.draw_curve(self.leg_r, cx+2, cy+10, cx+2-swing, cy+24, -swing*0.5)
        self.draw_curve(self.arm_l, cx-5, cy-2, cx-8-arm_swing, cy+8, -arm_swing*0.5)
        
        if self.arm_up:
            self.draw_curve(self.arm_r, cx+5, cy-2, cx+12, cy-20, 5)
        else:
            self.draw_curve(self.arm_r, cx+5, cy-2, cx+8+arm_swing, cy+8, arm_swing*0.5)

    def draw_curve(self, obj, x1, y1, x2, y2, bend):
        mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2
        self.canvas.coords(obj, x1, y1, mx, my, x2, y2)

class GameApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=GRASS_COLOR, highlightthickness=0)
        self.canvas.pack()
        
        # State Management
        self.state = 'INTRO'
        self.walker = Walker(self.canvas, 400, 350)
        self.limits = {"N": False, "S": False, "E": False, "W": False}
        self.keys = {}
        
        # Timers & Input
        self.start_time = time.time()
        self.press_count = 0
        self.last_press = 0
        self.walk_timer = 0
        
        self.setup_world()
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.run()

    def setup_world(self):
        self.canvas.create_rectangle(0, 0, WIDTH, 100, fill=SKY_COLOR, outline="")
        self.clouds = [[random.randint(0, 800), random.randint(10, 70), random.uniform(0.3, 0.8)] for _ in range(6)]
        self.cloud_objs = [self.canvas.create_oval(0,0,0,0, fill="white", outline="", stipple="gray50") for _ in self.clouds]

    def key_press(self, e):
        k = e.keysym.lower()
        self.keys[k] = True
        now = time.time()
        
        if self.state == 'INTRO' and k == 'space': self.trigger_state('DANCING')
        
        # Rage Detection
        if self.state == 'PLAYING' and k in 'wasd':
            if self.is_at_limit():
                if now - self.last_press < 0.3: self.press_count += 1
                else: self.press_count = 1
                self.last_press = now
                if self.press_count > 2: self.trigger_state('ANGRY')

    def key_release(self, e): self.keys[e.keysym.lower()] = False

    def is_at_limit(self):
        px, py = self.walker.pos
        return py <= 120 or py >= 590 or px >= 795 or px <= 5

    def trigger_state(self, new_state):
        self.state = new_state
        self.state_start = time.time()
        # Reset specific state flags
        self.walker.arm_up = (new_state == 'DEFIANCE')
        self.walker.shake = 3 if new_state == 'ANGRY' else 0

    def run(self):
        elapsed = (time.time() - self.start_time) * 1000
        self.canvas.delete("ui") # Clear only UI layer
        
        # 1. Update Clouds
        for i, c in enumerate(self.clouds):
            c[0] -= c[2]
            if c[0] < -50: c[0] = 850
            self.canvas.coords(self.cloud_objs[i], c[0], c[1], c[0]+40, c[1]+15)

        # 2. State Machine Logic
        if self.state == 'INTRO':
            self.draw_roman_intro(elapsed)
            self.walker.update_animation(0, 0, 0)
            
        elif self.state == 'DANCING':
            dt = time.time() - self.state_start
            s, a, b = self.get_dance_values(dt)
            self.walker.update_animation(s, a, b)
            if dt > 2: self.trigger_state('SPEAKING' if not all(self.limits.values()) else 'DEFIANCE')

        elif self.state == 'SPEAKING':
            self.walker.update_animation(0, 0, 0)
            self.draw_bubble("Thanks to the Gods! I am free to go!!")
            if time.time() - self.state_start > 3: self.trigger_state('PLAYING')

        elif self.state == 'PLAYING':
            self.handle_movement()
            s, a, b = self.get_walk_values()
            self.walker.update_animation(s, a, b)
            if all(self.limits.values()): self.trigger_state('CRISIS')

        elif self.state == 'CRISIS':
            dt = time.time() - self.state_start
            self.handle_movement() # Allow movement during crisis
            self.walker.update_animation(*self.get_walk_values())
            msg = "Uhmmm!..." if dt < 1 else "I think that I am trapped inside a stupid code!"
            self.draw_bubble(msg)
            if dt > 7: self.trigger_state('DANCING')

        elif self.state == 'DEFIANCE':
            self.walker.update_animation(0, 0, 0)
            self.draw_bubble("FUCK the Gods!")
            if time.time() - self.state_start > 2: 
                self.limits = {k: False for k in self.limits}
                self.trigger_state('PLAYING')

        elif self.state == 'ANGRY':
            self.walker.update_animation(10, 15, 0)
            self.draw_bubble("LET ME GO, YOU K@NT!", size=33, color="red")
            if time.time() - self.state_start > 2: self.trigger_state('PLAYING')

        self.root.after(16, self.run)

    def handle_movement(self):
        moved = False
        if self.keys.get('w'): self.walker.pos[1] -= 4; moved = True
        if self.keys.get('s'): self.walker.pos[1] += 4; moved = True
        if self.keys.get('a'): self.walker.pos[0] -= 4; moved = True
        if self.keys.get('d'): self.walker.pos[0] += 4; moved = True
        
        # Limit Checks
        px, py = self.walker.pos
        if py <= 120: self.walker.pos[1]=120; self.limits["N"]=True
        if py >= 590: self.walker.pos[1]=590; self.limits["S"]=True
        if px >= 795: self.walker.pos[0]=795; self.limits["E"]=True
        if px <= 5:   self.walker.pos[0]=5;   self.limits["W"]=True
        
        self.walk_timer = self.walk_timer + 0.25 if moved else 0

    def get_walk_values(self):
        s = math.sin(self.walk_timer)*6
        a = math.sin(self.walk_timer)*5
        b = math.sin(self.walk_timer*2)*2 if self.walk_timer > 0 else 0
        return s, a, b

    def get_dance_values(self, t):
        s, a, b = math.sin(t*20)*15, math.cos(t*20)*18, math.sin(t*15)*7
        jump = -60 * (((t-1.6)*2.5) * (1 - ((t-1.6)*2.5)) * 4) if t > 1.6 else 0
        return s, a, b + jump

    def draw_roman_intro(self, ms):
        tit, sub = "V E N T E N V S   W A L K E R", "T H E   R E T U R N"
        self.canvas.create_text(403, 203, text=tit, fill=ROMAN_RED, font=("Times", 36, "bold"), tags="ui")
        self.canvas.create_text(400, 200, text=tit, fill="white", font=("Times", 36, "bold"), tags="ui")
        self.canvas.create_text(402, 252, text=sub, fill=ROMAN_RED, font=("Times", 18, "bold"), tags="ui")
        self.canvas.create_text(400, 250, text=sub, fill="white", font=("Times", 18, "bold"), tags="ui")
        if (ms // 1000) % 2 == 0:
            self.canvas.create_text(400, 480, text="PRESS [ SPACE ] TO INITIALIZE", fill=ROMAN_RED, font=("Consolas", 12, "bold"), tags="ui")

    def draw_bubble(self, text, size=9, color="black"):
        cx, cy = self.walker.pos
        t_id = self.canvas.create_text(cx, cy - 50, text=text, fill=color, font=("Arial", size, "bold"), tags="ui")
        bbox = self.canvas.bbox(t_id)
        rect = self.canvas.create_rectangle(bbox[0]-10, bbox[1]-5, bbox[2]+10, bbox[3]+5, fill="white", outline="black", tags="ui")
        self.canvas.tag_raise(t_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()