import tkinter as tk
import random
import math
import time

# --- CONSTANTS & CONFIG ---
WIDTH, HEIGHT = 800, 600
SKY_COLOR = "#40E0D0"
GRASS_COLOR = "#8DB600"
ROMAN_RED = "#8B0000"
HORIZON_Y = 120 

class Walker:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.pos = [x, y]
        self.arm_up = False
        self.shake = 0
        self.scale = 1.0 
        
        self.shadow = canvas.create_oval(0,0,0,0, fill="#1B3022", outline="", stipple="gray50")
        self.leg_l = canvas.create_line(0,0,0,0, smooth=True, fill="black", width=2)
        self.leg_r = canvas.create_line(0,0,0,0, smooth=True, fill="black", width=2)
        self.arm_l = canvas.create_line(0,0,0,0, smooth=True, fill="black", width=2)
        self.arm_r = canvas.create_line(0,0,0,0, smooth=True, fill="black", width=2)
        self.body = canvas.create_rectangle(0,0,0,0, fill="red", outline="")
        self.head = canvas.create_rectangle(0,0,0,0, fill="black")
        self.belt = canvas.create_rectangle(0,0,0,0, fill="white")

    def update_animation(self, swing, arm_swing, bob):
        range_y = HEIGHT - HORIZON_Y
        self.scale = 0.5 + ((self.pos[1] - HORIZON_Y) / range_y) * 0.5
        s = self.scale
        cx, cy = self.pos[0] + random.randint(-self.shake, self.shake), self.pos[1] + (bob * s)
        
        self.canvas.coords(self.shadow, cx-(25*s), self.pos[1]+(18*s), cx+(5*s), self.pos[1]+(24*s))
        self.canvas.coords(self.body, cx-(5*s), cy-(10*s), cx+(5*s), cy+(10*s))
        self.canvas.coords(self.head, cx-(5*s), cy-(10*s), cx+(5*s), cy-(7*s))
        self.canvas.coords(self.belt, cx-(5*s), cy+(7*s), cx+(5*s), cy+(10*s))
        
        self.draw_curve(self.leg_l, cx-(2*s), cy+(10*s), cx-((2-swing)*s), cy+(24*s), swing*0.4*s)
        self.draw_curve(self.leg_r, cx+(2*s), cy+(10*s), cx+((2+swing)*s), cy+(24*s), -swing*0.4*s)
        self.draw_curve(self.arm_l, cx-(5*s), cy-(2*s), cx-((8+arm_swing)*s), cy+(8*s), -arm_swing*0.4*s)
        
        if self.arm_up:
            self.draw_curve(self.arm_r, cx+(5*s), cy-(2*s), cx+(12*s), cy-(20*s), 5*s)
        else:
            self.draw_curve(self.arm_r, cx+(5*s), cy-(2*s), cx+((8+arm_swing)*s), cy+(8*s), arm_swing*0.4*s)

    def draw_curve(self, obj, x1, y1, x2, y2, bend):
        mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2
        self.canvas.coords(obj, x1, y1, mx, my, x2, y2)

class GameApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=GRASS_COLOR, highlightthickness=0)
        self.canvas.pack()
        
        self.state = 'INTRO'
        self.walker = Walker(self.canvas, 400, 350)
        self.limits = {"N": False, "S": False, "E": False, "W": False}
        self.keys = {}
        self.start_time = time.time()
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
        if self.state == 'INTRO' and k == 'space': self.trigger_state('DANCING')

    def key_release(self, e): self.keys[e.keysym.lower()] = False

    def trigger_state(self, new_state):
        self.state = new_state
        self.state_start = time.time()

    def run(self):
        now = time.time()
        self.canvas.delete("ui") 
        
        for i, c in enumerate(self.clouds):
            c[0] -= c[2]
            if c[0] < -50: c[0] = 850
            self.canvas.coords(self.cloud_objs[i], c[0], c[1], c[0]+40, c[1]+15)

        if self.state == 'INTRO':
            self.draw_roman_intro()
            self.walker.update_animation(0, 0, 0)
            
        elif self.state == 'DANCING':
            dt = now - self.state_start
            s, a, b = self.get_dance_values(dt)
            self.walker.update_animation(s, a, b)
            if dt > 2: self.trigger_state('SPEAKING')

        elif self.state == 'SPEAKING':
            self.walker.update_animation(0, 0, 0)
            self.draw_speak("Thanks to the Gods! I am free to go!!")
            if now - self.state_start > 3: self.trigger_state('PLAYING')

        elif self.state == 'PLAYING':
            self.handle_movement()
            self.walker.update_animation(*self.get_walk_values())
            if all(self.limits.values()): self.trigger_state('CRISIS')

        elif self.state == 'CRISIS':
            dt = now - self.state_start
            self.handle_movement()
            self.walker.update_animation(*self.get_walk_values())
            
            if dt < 12.0:
                msg = "Uhmmm!..." if dt < 2.5 else "I think that I am trapped inside a stupid code!"
                if dt < 10.0 or int(now * 5) % 2 == 0:
                    self.draw_think(msg)

        self.root.after(16, self.run)

    def handle_movement(self):
        moved = False
        speed = 2.0 * self.walker.scale 
        if self.keys.get('w'): self.walker.pos[1] -= speed; self.walker.pos[0] += speed * 0.7; moved = True
        if self.keys.get('s'): self.walker.pos[1] += speed; self.walker.pos[0] -= speed * 0.7; moved = True
        if self.keys.get('a'): self.walker.pos[0] -= speed; moved = True
        if self.keys.get('d'): self.walker.pos[0] += speed; moved = True
        
        px, py = self.walker.pos
        if py <= HORIZON_Y: self.walker.pos[1]=HORIZON_Y; self.limits["N"]=True
        if py >= 590: self.walker.pos[1]=590; self.limits["S"]=True
        if px >= 795: self.walker.pos[0]=795; self.limits["E"]=True
        if px <= 5:   self.walker.pos[0]=5;   self.limits["W"]=True
        self.walk_timer += (0.08 * self.walker.scale) if moved else 0

    def get_walk_values(self):
        s, a = math.sin(self.walk_timer * 4) * 5, math.cos(self.walk_timer * 4) * 2
        b = math.sin(self.walk_timer * 8) * 1.0 if self.walk_timer > 0 else 0
        return s, a, b

    def get_dance_values(self, t):
        s, a, b = math.sin(t*20)*15, math.cos(t*20)*18, math.sin(t*15)*7
        jump = -60 * (((t-1.6)*2.5) * (1 - ((t-1.6)*2.5)) * 4) if t > 1.6 else 0
        return s, a, b + jump

    def draw_roman_intro(self):
        tit, sub = "V E N T E N V S   W A L K E R", "T H E   R E T U R N"
        # Shadow layer
        self.canvas.create_text(403, 203, text=tit, fill=ROMAN_RED, font=("Times", 36, "bold"), tags="ui")
        # Main Title
        self.canvas.create_text(400, 200, text=tit, fill="white", font=("Times", 36, "bold"), tags="ui")
        # Subtitle Shadow
        self.canvas.create_text(402, 252, text=sub, fill=ROMAN_RED, font=("Times", 18, "bold"), tags="ui")
        # Subtitle
        self.canvas.create_text(400, 250, text=sub, fill="white", font=("Times", 18, "bold"), tags="ui")
        
        if (int(time.time()) % 2 == 0):
            self.canvas.create_text(400, 480, text="PRESS [ SPACE ] TO INITIALIZE", fill=ROMAN_RED, font=("Consolas", 12, "bold"), tags="ui")

    def draw_speak(self, text):
        cx, cy = self.walker.pos
        off_y = 55 * self.walker.scale
        t_id = self.canvas.create_text(cx, cy - off_y, text=text, fill="black", font=("Arial", 11, "bold"), tags="ui")
        b = self.canvas.bbox(t_id)
        self.canvas.create_rectangle(b[0]-10, b[1]-5, b[2]+10, b[3]+5, fill="white", outline="black", tags="ui")
        self.canvas.tag_raise(t_id)

    def draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_think(self, text):
        cx, cy = self.walker.pos
        s = self.walker.scale
        off_y = 65 * s
        t_id = self.canvas.create_text(cx, cy - off_y, text=text, fill="black", font=("Arial", 11, "italic", "bold"), tags="ui")
        b = self.canvas.bbox(t_id)
        self.draw_rounded_rect(b[0]-12, b[1]-8, b[2]+12, b[3]+8, 15, fill="white", outline="black", tags="ui")
        self.canvas.create_oval(cx-4*s, cy-45*s, cx+2*s, cy-39*s, fill="white", outline="black", tags="ui")
        self.canvas.create_oval(cx-2*s, cy-34*s, cx+1*s, cy-31*s, fill="white", outline="black", tags="ui")
        self.canvas.tag_raise(t_id)

if __name__ == "__main__":
    root = tk.Tk(); app = GameApp(root); root.mainloop()