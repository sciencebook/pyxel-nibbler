import pyxel
from dataclasses import dataclass

from enum import Enum
class Dir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

BLOCK_SIZE = 5
TICK_RATE = 5
SCREEN_WIDTH = 180  #240
SCREEN_HEIGHT = 120  #180

NUMBER_OF_NIBBLES = 15

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

    def __init__(self, x: int, y: int, dir: Dir):
       self.body = []
       self.body.append(
           SnakeSegment(x, y, dir, pyxel.rndi(1,16))
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

    def check_snake_collision(self, snake: Snake | None = None):
        body = snake.body if snake else self.body[1:]
        head = self.body[0]
        for i in range(len(body)):
            if body[i].x == head.x and body[i].y == head.y:
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
    SPLASH = 0
    RUNNING = 1
    GAME_OVER = 2

class App:
    state = GameState.SPLASH
    loser: list[int] = []
    snake1: Snake
    snake2: Snake
    nibbles: list[Nibble]
    music: bool

    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Nibbler")
        pyxel.load("nibbler_vsres.pyxres")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.state = GameState.SPLASH
        self.loser = []

        x = SCREEN_WIDTH // 2 - 25
        y = SCREEN_HEIGHT // 2 - 10
        self.snake1 = Snake(x, y, Dir.RIGHT)
        self.snake2 = Snake(x + 50, y, Dir.LEFT)

        self.nibbles = []
        for _ in range(NUMBER_OF_NIBBLES):
            self.nibbles.append(Nibble(self.snake1.body + self.snake2.body))
        
        pyxel.stop()
        self.music = False
        
    def game_over(self):
        self.state = GameState.GAME_OVER
        pyxel.stop()
        pyxel.playm(0)
    
    def _check_game_state_controls(self):
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.KEY_RETURN):
            self.reset()
        if self.state == GameState.SPLASH:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_LEFT) \
              or pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.KEY_A):
                self.state = GameState.RUNNING
    
    def _check_snake_controls(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.snake2.change_direction(Dir.UP)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.snake2.change_direction(Dir.DOWN)
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.snake2.change_direction(Dir.LEFT)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.snake2.change_direction(Dir.RIGHT)
        if pyxel.btnp(pyxel.KEY_W):
            self.snake1.change_direction(Dir.UP)
        elif pyxel.btnp(pyxel.KEY_S):
            self.snake1.change_direction(Dir.DOWN)
        elif pyxel.btnp(pyxel.KEY_A):
            self.snake1.change_direction(Dir.LEFT)
        elif pyxel.btnp(pyxel.KEY_D):
            self.snake1.change_direction(Dir.RIGHT)

    def _check_nibble_collision(self):
        for snake in [self.snake1, self.snake2]:
            head = snake.body[0]
            for n in self.nibbles:
                if head.x == n.x and head.y == n.y:
                    pyxel.play(3, 0)
                    snake.grow(n.color)
                    n.reset(self.snake1.body + self.snake2.body)

    def update(self):
        self._check_game_state_controls()
        if self.state == GameState.GAME_OVER or self.state == GameState.SPLASH:
            return

        if not self.music:
            pyxel.playm(1, loop=True)
            self.music = True

        self._check_snake_controls()
        if pyxel.frame_count % TICK_RATE != 1:
            return

        for snake in [self.snake1, self.snake2]:
            snake.update()

        if self.snake1.check_wall_collision() \
            or self.snake1.check_snake_collision() \
            or self.snake1.check_snake_collision(self.snake2):
            self.loser.append(1)
        if self.snake2.check_wall_collision() \
            or self.snake2.check_snake_collision() \
            or self.snake2.check_snake_collision(self.snake1):
            self.loser.append(2)
        if len(self.loser) > 0:
            self.game_over()
            return
        self._check_nibble_collision()

    def draw(self):
        if self.state == GameState.GAME_OVER:
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 7)
            if len(self.loser) == 2:
                pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "It's a Draw!", 7)
            else:
                winner = 1 if self.loser[0] == 2 else 2
                wincol = self.snake1.body[0].col if winner == 1 else self.snake2.body[0].col
                pyxel.text(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2, f"Player {winner} Wins!", wincol)

            pyxel.text(SCREEN_WIDTH // 2 - 41, SCREEN_HEIGHT // 2 + 10, "Press Return to reset", 9)
            return

        pyxel.cls(0)
        self.snake1.draw()
        self.snake2.draw()
        for n in self.nibbles:
            pyxel.circ(n.x+2, n.y+2, 1, n.color)
            # pyxel.pal(2, n.color)
            # pyxel.blt(n.x, n.y, 0, 10, 0, 5 * n.i, 5, 10)
            # pyxel.pal()
            # pyxel.circ(n.x+2, n.y+2, 2, n.color)
            # pyxel.circ(n.x+2, n.y+2, 1, (n.color + 1) % 16)

        if self.state == GameState.SPLASH:
            pyxel.blt(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10, 0, 16, 0, 33,15, 13, 0, 2)
            pyxel.text(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10, "Nibbler", 2)
            pyxel.text(SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2, "Press any Arrow Key to Start", 7)
            pyxel.text(SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 + 15, "Player 1: WASD", self.snake1.body[0].col)
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 + 25, "Player 2: Arrow Keys", self.snake2.body[0].col)
        
App()
