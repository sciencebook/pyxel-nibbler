
# Pyxel Nibbler Collection

A small collection of arcade-style snake games built with Pyxel. This repo focuses on the Nibbler experiments, with a single-player version and a two-player head-to-head version.

## Included Games

### Nibbler

The main project in this repo is a single-player snake game with a few extra touches:

- adjustable speed
- selectable number of food items
- different nibble shapes
- settings screen before play begins
- splash screen and game-over flow
- simple synth-like music loop

Run it from the project directory:

```bash
cd nibbler
python nibbler.py
```

### Nibbler VS

A two-player version of the same idea, built as a competitive match:

- snake vs snake gameplay
- two sets of controls
- food spawns shared across both snakes
- collision rules for walls and enemy bodies
- restart support with the Enter key

Run it from the project directory:

```bash
cd nibbler_vs
python nibbler_vs.py
```

## Controls

### Nibbler

- Arrow keys: move the snake
- S: open settings screen from the splash screen
- Enter: restart after game over
- R: reset the game at any time
- Space: grow the snake instantly (debug/test shortcut)

### Nibbler VS

Player 1:
- W, A, S, D: move

Player 2:
- Arrow keys: move

Shared:
- Enter or R: restart

## How to Run

This project uses Pyxel. If you do not already have it installed, install it first:

```bash
pip install pyxel
```

Then run either game from its folder with Python.

## Project Structure

```text
pyxel/
├── README.md
├── nibbler/
│   ├── nibbler.py
│   ├── nibblerres.pyxres
│   └── ...
├── nibbler_vs/
│   ├── nibbler_vs.py
│   ├── nibbler_vsres.pyxres
│   └── ...
└── ...
```

## Notes

In the /examples folder there is an example of ball physics
In the /prototype there are some very ... nascent game ideas.
