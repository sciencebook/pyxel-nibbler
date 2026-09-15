import pyxel
from dataclasses import dataclass, field

@dataclass
class BallState:
    x: float
    y: float
    vx: float # pixels per time
    vy: float

class Ball:
    GRAVITY = 9.8 * 0.1  # Gravity constant for the simulation
    DT = .5  # Time step for the simulation
    ELASTICITY = 0.85 
    FLOOR_FRICTION = 0.98
    r = 2
    
    def __init__(self, state: BallState, color = 8):
        self.state = state
        self.color = color

    def draw(self):
        pyxel.circ(self.state.x, self.state.y, self.r, self.color)

    def update_state(self):
        # if self.state.y < pyxel.height:  # Only apply gravity if the ball is above the floor
        self.state.vy += (self.GRAVITY * self.DT)  # Apply gravity to vertical velocity
        self.state.x += self.state.vx * self.DT
        self.state.y += self.state.vy * self.DT
        if self.state.y >= pyxel.height: # below floor
            self.state.y = pyxel.height
            self.state.vy *= -self.ELASTICITY  # Reverse velocity and apply damping 
            self.state.vx *= self.FLOOR_FRICTION  # Apply horizontal friction
        elif self.state.y <= 0: # above ceiling
            self.state.y = 0
            self.state.vy *= -self.ELASTICITY  # Reverse velocity and apply damping
        if self.state.x >= pyxel.width: # right wall
            self.state.x = pyxel.width
            self.state.vx *= -self.ELASTICITY  # Reverse velocity and apply damping
        elif self.state.x <= 0: # left wall
            self.state.x = 0
            self.state.vx *= -self.ELASTICITY  # Reverse velocity and apply damping

class Sprite:
    dir = "R"
    blink_state: int = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        if self.dir == 'L':
            pyxel.blt(self.x, self.y, 0, 8, self.blink_state * 8, 8, 8, 2)
        else:
            pyxel.blt(self.x, self.y, 0, 0, self.blink_state * 8, 8, 8, 2)

        if self.blink_state == 1:
            self.blink_state = 2
        elif self.blink_state == 2:
            self.blink_state = 0

    def blink(self):
        self.blink_state = 1
 
class Target:
    blink_state: int = 0
    blink_length: int = 10
    w = 16
    h = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32 + (pyxel.ceil(self.blink_state / self.blink_length) * self.w), 0, self.w, self.h)

    def score_hit(self):
        self.blink_state = 1

    def update(self):
        if self.blink_state >= 1:
            self.blink_state += 1
        if self.blink_state > self.blink_length:
            self.blink_state = 0

class Targeting:
    xpct = 0
    xpct_dir = 1
    x_picked = False
    ypct = 0
    ypct_dir = 1
    y_picked = False
    is_visible = True

    def __init__(self, x, y):
        self.hlx = x - 2
        self.hly = y - 3
        self.vlx = x + 11
        self.vly = y - 2

    def draw(self):
        if not self.is_visible:
            return
        xlen = 11
        ylen = 10
        pyxel.line(self.hlx, self.hly, self.hlx + xlen, self.hly, 7)
        pyxel.pset(self.hlx + (xlen * self.xpct * .01), self.hly, 12)
        pyxel.line(self.vlx, self.vly + ylen, self.vlx, self.vly, 7)
        pyxel.pset(self.vlx, self.vly + ylen - (ylen * self.ypct * .01), 12)

    def hide(self):
        self.is_visible = False
    def show(self):
        self.is_visible = True
        self.x_picked = False
        self.y_picked = False
        self.xpct = 0
        self.ypct = 0
        self.xpct_dir = 1
        self.ypct_dir = 1

    def space_pressed(self):
        if not self.x_picked:
            self.x_picked = True
        elif not self.y_picked:
            self.y_picked = True
            return True
        return False

    def update(self):
        if not self.x_picked:
            self.xpct += 5 * self.xpct_dir
            if self.xpct >= 100:
                self.xpct_dir = -1
            elif self.xpct <= 0:
                self.xpct_dir = 1
        elif not self.y_picked:
            self.ypct += 5 * self.ypct_dir
            if self.ypct >= 100:
                self.ypct_dir = -1
            elif self.ypct <= 0:
                self.ypct_dir = 1

from enum import Enum
class GameState(Enum):
    SPLASH = 0
    RUNNING = 1
    # PAUSED = 2
    # GAME_OVER = 3

class App:
    state = GameState.RUNNING
    balls: list[Ball] = []
    score = 0

    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("my_resource.pyxres")

        self.sprite = Sprite(20, 70)
        self.target = Target(100, 30)
        self.targeting = Targeting(20, 70)

        pyxel.run(self.update, self.draw)

    def check_for_user_input(self):
        throw = False
        if pyxel.btnp(pyxel.KEY_Q):
            self.balls.clear()  # Clear all balls
            self.state = GameState.SPLASH
        elif pyxel.btnp(pyxel.KEY_SPACE):
            throw = self.targeting.space_pressed()
        elif pyxel.btnp(pyxel.KEY_R):
            self.targeting.show()

        if throw:
            vx = (self.targeting.xpct - 50) * 0.3
            vy = (self.targeting.ypct - 50) * -0.3
            self.balls.append(
                Ball(
                    BallState(
                        x=self.sprite.x + 4,
                        y=self.sprite.y + 4,
                        vx=vx,
                        vy=vy
                    ),
                    color=pyxel.rndi(1, 15)
                )
            )
            self.targeting.hide()    

    def check_for_ball_hit(self):
        for ball in self.balls:
            if ball.state.x + ball.r * 2 >= self.target.x + 1 and ball.state.x <= self.target.x + self.target.w - 1\
                and ball.state.y + ball.r * 2 >= self.target.y + 1 and ball.state.y <= self.target.y + self.target.h - 1:

                self.target.score_hit()
                self.score += 1

    def update(self):
        self.check_for_user_input()

        for ball in self.balls:
            ball.update_state()

        self.target.update()
        self.targeting.update()

        self.check_for_ball_hit()

        if pyxel.frame_count % 250 == 0:
            self.sprite.blink()

    def draw(self):
        pyxel.cls(0)
        if self.state == GameState.SPLASH:
            pyxel.text(60, 50, "Ball Party!!!", pyxel.rndi(1, 15))
            pyxel.text(62, 60, "Press Space!", 3)
            # pyxel.text(32, 70, "Press SPACE to Party HARDER", 3)

        self.sprite.draw()
        self.target.draw()
        self.targeting.draw()

        for ball in self.balls:
            ball.draw()

        pyxel.text(5, 5, f"Score: {self.score}", 7)
App()
