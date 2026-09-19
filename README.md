
# Pyxel Nibbler Collection

A small collection of arcade-style snake games built with Pyxel. This repo focuses on the Nibbler experiments, with a single-player version and a two-player head-to-head version.

## Included Games

### Nibbler

https://kitao.github.io/pyxel/web/launcher/?run=sciencebook.pyxel-nibbler.nibbler.nibbler

A single-player snake game with a few extra features:

- adjustable speed
- selectable number of food items
- different nibble shapes
- settings screen before play begins
- splash screen and game-over flow
- simple synth-like music loop

There is no way to win this game.

### Nibbler VS

https://kitao.github.io/pyxel/web/launcher/?run=sciencebook.pyxel-nibbler.nibbler_vs.nibbler_vs

A two-player version of the same snake game for head to head nibbling.

- snake vs snake gameplay
- two sets of controls
- food spawns shared across both snakes
- collision rules for walls and enemy bodies

## Controls

### Nibbler

- Arrow keys: move the snake
- S: open settings screen from the splash screen
- Enter/R: restart after game over, or at any time

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

Then run either game from its folder with Python.  For example:

```bash
cd nibbler_vs
python nibbler_vs.py
```

You can also install the VScode extension for Pyxel and run the game direcly in VScode.

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

In the /examples folder there is an example of ball physics.
In the /prototype there are some very ... nascent game ideas.
