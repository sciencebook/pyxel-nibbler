import pyxel
from dataclasses import dataclass

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
    
    def __init__(self, state: BallState, color = 8):
        self.state = state
        self.color = color

    def draw(self):
        pyxel.circ(self.state.x, self.state.y, 2, self.color)

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


from enum import Enum
class GameState(Enum):
    SPLASH = 0
    RUNNING = 1

class App:
    state = GameState.SPLASH
    balls: list[Ball] = []

    def __init__(self):
        pyxel.init(160, 120)
        pyxel.run(self.update, self.draw)

    def _add_balls(self):
        for _ in range(200):
            self.balls.append(
                Ball(
                    BallState(
                        x=pyxel.rndi(0, pyxel.width),
                        y=pyxel.rndi(0, pyxel.height-20),
                        vx=pyxel.rndi(-5, 5),
                        vy=pyxel.rndi(-5, 5)
                    ),
                    color=pyxel.rndi(1, 15)
                )
            )
            self.balls[-1].GRAVITY += pyxel.rndf(-0.5, 0.5)  # Randomize gravity slightly for each ball
            self.balls[-1].ELASTICITY += pyxel.rndf(-0.1, 0.149)  # Randomize elasticity slightly for each ball

    def check_for_user_input(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.balls.clear()  # Clear all balls
            self.state = GameState.SPLASH
        if pyxel.btnp(pyxel.KEY_SPACE) and self.state == GameState.SPLASH:
            self.state = GameState.RUNNING
            self._add_balls()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            for ball in self.balls:
                ball.state.vy = pyxel.rndf(-5, -20)  # Jump velocity
                ball.state.vx = pyxel.rndf(-2, 2)  # Random horizontal velocity

    def update(self):
        self.check_for_user_input()
        for ball in self.balls:
            ball.update_state()

    def draw(self):
        pyxel.cls(0)
        if self.state == GameState.SPLASH:
            pyxel.text(60, 50, "Ball Party!!!", pyxel.rndi(1, 15))
            pyxel.text(62, 60, "Press Space!", 3)

        for ball in self.balls:
            ball.draw()

App()
