import pyxel
from dataclasses import dataclass
from enum import Enum

BLOCK_SIZE = 5
SCREEN_WIDTH = 120  #240
SCREEN_HEIGHT = 100  #180

@dataclass
class Settings:
    speed: int = 0
    number_of_nibbles: int = 2
    nibble_shape: int = 0

TICK_RATES = [5, 3, 2]
NUMBERS_OF_NIBBLES = [5, 10, 15, 20, 25]

class SettingsScreen:
    selected = "speed"
    s = Settings()

    def number_of_nibbles(self):
        return NUMBERS_OF_NIBBLES[self.s.number_of_nibbles]
    def tick_rate(self):
        return TICK_RATES[self.s.speed]
    def song(self):
        return [1, 3, 5][self.s.speed]
    def nibble_shape(self):
        return self.s.nibble_shape

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.selected == "speed": self.selected = "num"
            elif self.selected == "num": self.selected = "nibbs"
            elif self.selected == "nibbs": self.selected = "speed"
        elif pyxel.btnp(pyxel.KEY_UP):
            if self.selected == "speed": self.selected = "nibbs"
            elif self.selected == "nibbs": self.selected = "num"
            elif self.selected == "num": self.selected = "speed"
        elif pyxel.btnp(pyxel.KEY_LEFT):
            if self.selected == "speed": self.s.speed = max(0, self.s.speed - 1)
            elif self.selected == "num": self.s.number_of_nibbles = max(0, self.s.number_of_nibbles - 1)
            elif self.selected == "nibbs": self.s.nibble_shape = max(0, self.s.nibble_shape - 1)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            if self.selected == "speed": self.s.speed = min(2, self.s.speed + 1)
            elif self.selected == "num": self.s.number_of_nibbles = min(4, self.s.number_of_nibbles + 1)
            elif self.selected == "nibbs": self.s.nibble_shape = min(3, self.s.nibble_shape + 1)

    def draw(self):
        pyxel.rect(5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10, 1)
        pyxel.rectb(5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10, 7)
        pyxel.text(25, 13, "Settings", 7)

        cursor_y = -10
        pyxel.text(25, 23, "Speed", 8)
        pyxel.text(25, 33, "|---|---|", 7)
        pyxel.text(25 + (self.s.speed ) * 16, 33, "I", 8)
        if (self.selected == "speed"): cursor_y = 23

        pyxel.text(25, 43, "Number of Nibbles", 9)
        pyxel.text(25, 53, "|---|---|---|---|", 7)
        pyxel.text(25 + (self.s.number_of_nibbles ) * 16, 53, "I", 9)
        if self.selected == "num": cursor_y = 43

        pyxel.text(25, 63, "Nibble Shape", 10)
        pyxel.text(25, 73, "|---|---|---|", 7)
        pyxel.text(25 + (self.s.nibble_shape ) * 16, 73, "I", 10)
        if self.selected == "nibbs": cursor_y = 63

        pyxel.text(18, cursor_y, ">", 7)

        pyxel.text(55, 83, "(press return)", 7)

class Dir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

@dataclass
class SnakeSegment:
    x: int
    y: int
    dir: Dir 
    col: int

class Snake:
    body: list[SnakeSegment]
    new_dir: Dir | None = None
    size = BLOCK_SIZE

    def __init__(self):
        self.body = []
        self.color_count = 3
        self.body.append(
           SnakeSegment(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 10, Dir.RIGHT, pyxel.rndi(1,16))
        )

    def change_direction(self, dir: Dir):
        if (self.body[0].dir.value + dir.value) % 2 != 0 \
            or len(self.body) == 1:
            self.new_dir = dir

    def grow(self, color: int):
        end = self.body[-1]
        x = end.x; y = end.y
        match end.dir:
            case Dir.RIGHT: x -= self.size
            case Dir.LEFT: x += self.size
            case Dir.UP: y += self.size
            case Dir.DOWN: y -= self.size
        self.body.append(
            SnakeSegment(x, y, end.dir, color)
        )

    def check_wall_collision(self):
        head = self.body[0]
        if head.x > pyxel.width - self.size or head.x < 0 \
            or head.y > pyxel.height - self.size or head.y < 0:
            return True

    def check_self_collision(self):
        head = self.body[0]
        for i in range(len(self.body) - 1, 0, -1):
            s = self.body[i]
            if s.x == head.x and s.y == head.y:
                return True
        return False

    def update(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self .body[i - 1].y
            self.body[i].dir = self.body[i - 1].dir
        
        head = self.body[0]
        move_direction = self.new_dir if self.new_dir else head.dir
        match move_direction:
            case Dir.RIGHT: head.x += self.size
            case Dir.LEFT: head.x -= self.size
            case Dir.UP: head.y -= self.size
            case Dir.DOWN: head.y += self.size
        head.dir = move_direction
        self.new_dir = None

    def draw(self):
        for s in self.body:
            pyxel.rect(s.x, s.y, self.size, self.size, s.col)

        head = self.body[0]
        eyes = []
        if (head.dir == Dir.RIGHT or head.dir == Dir.LEFT):
            eyes = [(2,1),(2,3)]
        else:
            eyes = [(1,2),(3,2)]
        for i,j in eyes:
            pyxel.pset(head.x + i, head.y + j, (head.col + 1) % 16)

        tongue = []
        if head.dir == Dir.RIGHT:
            tongue = [(5,2),(6,2),(7,1),(7,3)]
        elif head.dir == Dir.LEFT:
            tongue = [(-1,2),(-2,2),(-3,1),(-3,3)]
        elif head.dir == Dir.UP:
            tongue = [(2,-1),(2,-2),(1,-3),(3,-3)]
        elif head.dir == Dir.DOWN:
            tongue = [(2,5),(2,6),(1,7),(3,7)]
        for i,j in tongue:
            pyxel.pset(head.x + i, head.y + j, 8)

class Nibble:
    x: int
    y: int
    color: int
    i: int = 1

    def __init__(self, snake_body: list[SnakeSegment]):
        self.reset(snake_body)

    def reset(self, snake: list[SnakeSegment]):
        while True:
            self.i = 1 if pyxel.rndi(0, 1) == 0 else -1
            self.x = pyxel.floor(pyxel.rndi(0, pyxel.width) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = pyxel.floor(pyxel.rndi(0, pyxel.height) / BLOCK_SIZE) * BLOCK_SIZE
            if True not in map(lambda s: s.x == self.x and s.y == self.y, snake):
                self.color = pyxel.rndi(1,16)
                break

class GameState(Enum):
    SETTINGS = -1
    SPLASH = 0
    RUNNING = 1
    GAME_OVER = 2

class App:
    settings: SettingsScreen
    state = GameState.SPLASH
    snake: Snake
    nibbles: list[Nibble]
    music: bool

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Nibbler")
        pyxel.load("nibblerres.pyxres")
        self.settings = SettingsScreen()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.state = GameState.SPLASH
        self.snake = Snake()
        self.nibbles = []
        for _ in range(self.settings.number_of_nibbles()):
            self.nibbles.append(Nibble(self.snake.body))
        
        pyxel.stop()
        self.music = False

    def settings_mode(self):
        self.state = GameState.SETTINGS
        
    def game_over(self):
        pyxel.stop()
        self.state = GameState.GAME_OVER
        pyxel.playm(0)
    
    def _check_game_state_controls(self):
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.KEY_RETURN):
            self.reset()
        elif self.state == GameState.SPLASH and self.state != GameState.SETTINGS:
            if pyxel.btnp(pyxel.KEY_S):
                self.settings_mode()
            elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_LEFT):
                self.state = GameState.RUNNING
    
    def _check_snake_controls(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.snake.change_direction(Dir.UP)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.snake.change_direction(Dir.DOWN)
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.snake.change_direction(Dir.LEFT)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.snake.change_direction(Dir.RIGHT)

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.snake.grow(color=pyxel.rndi(1,16))

    def _check_nibble_collision(self):
        head = self.snake.body[0]
        for n in self.nibbles:
            if head.x == n.x and head.y == n.y:
                pyxel.play(3, 0)
                self.snake.grow(n.color)
                n.reset(self.snake.body)

    def update(self):
        self._check_game_state_controls()
        if self.state == GameState.SETTINGS:
            self.settings.update()
        if self.state == GameState.GAME_OVER or self.state == GameState.SPLASH or self.state == GameState.SETTINGS:
            return

        if not self.music:
            pyxel.playm(self.settings.song(), loop=True)
            self.music = True

        self._check_snake_controls()
        if pyxel.frame_count % self.settings.tick_rate() == 1:
            self.snake.update()
            if self.snake.check_wall_collision() or self.snake.check_self_collision():
                self.game_over()
                return
            self._check_nibble_collision()

    def draw(self):
        if self.state == GameState.GAME_OVER:
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 7)
            pyxel.text(SCREEN_WIDTH // 2 - 41, SCREEN_HEIGHT // 2, "Press Return to reset", 9)
            return

        pyxel.cls(0)
        self.snake.draw()
        for n in self.nibbles:
            if self.settings.nibble_shape() == 0:
                pyxel.circ(n.x+2, n.y+2, 1, n.color)
            elif self.settings.nibble_shape() == 1:
                pyxel.circ(n.x+2, n.y+2, 2, n.color)
            elif self.settings.nibble_shape() == 2:
                pyxel.rect(n.x, n.y, 5, 5, n.color)
            elif self.settings.nibble_shape() == 3:
                pyxel.pal(2, n.color)
                pyxel.blt(n.x, n.y, 0, 10, 0, 5 * n.i, 5, 10)
                pyxel.pal()

        if self.state == GameState.SETTINGS:
            self.settings.draw()
        elif self.state == GameState.SPLASH:
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 10, "Nibbler", 5)
            pyxel.text(SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2, "Press any Arrow Key to Start", 7)
            pyxel.text(SCREEN_WIDTH // 2 - 38, SCREEN_HEIGHT // 2 + 10, "Press S for settings", 6)
        

App()
