import pyxel
from dataclasses import dataclass

LENGTH = 160
HEIGHT = 120

class Character:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update_state(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2

        if self.x < 0:
            self.x = 0
        if self.x > LENGTH:
            self.x = LENGTH
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT:
            self.y = HEIGHT

    def draw(self):
        pyxel.circ(self.x, self.y, 5, 9)
        pyxel.pset(self.x - 2, self.y, 0)
        pyxel.pset(self.x + 2, self.y, 0)
        pyxel.pset(self.x - 2, self.y - 1, 15)
        pyxel.pset(self.x + 2, self.y - 1, 15)


from enum import Enum
class GameState(Enum):
    SPLASH = 0
    RUNNING = 1

class App:
    state = GameState.RUNNING
    me = Character(80, 60)

    def __init__(self):
        pyxel.init(LENGTH, HEIGHT, title="Hippo")
        pyxel.run(self.update, self.draw)

    def check_for_game_state(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.state = GameState.SPLASH
        if pyxel.btnp(pyxel.KEY_SPACE) and self.state == GameState.SPLASH:
            self.state = GameState.RUNNING

    def update(self):
        self.check_for_game_state()
        self.me.update_state()

    def draw(self):
        pyxel.cls(0)
        if self.state == GameState.SPLASH:
            pyxel.text(60, 50, "Hippopotomus!", pyxel.rndi(1, 15))
            pyxel.text(62, 60, "Press Space!", 3)
            return

        self.me.draw()

App()
