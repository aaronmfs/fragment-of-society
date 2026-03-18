# Fragment of Society - Documentation

## Quick Links

- [Systems Documentation](./Systems/OVERVIEW.md) - Architecture and how-to guides
- [Input System](./Systems/INPUT.md) - Keyboard and mouse input
- [Entity System](./Systems/ENTITY.md) - Entities, characters, controllers
- [Game Engine](./Systems/GAMEENGINE.md) - Core game logic for RL

---

## Project Overview

**Fragment of Society** is a 2D top-down dungeon crawler built with Python/Pygame. Designed for both human playability and RL training.

### Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│   game.py           │────▶│   GameEngine        │
│  (Pygame Adapter)   │     │  (Pure Python)      │
└─────────────────────┘     └─────────────────────┘
```

- **game.py** - Pygame layer (window, rendering, input)
- **game_engine.py** - Pure Python game logic (RL-friendly)
- **input/** - pygame-free keyboard/mouse handling
- **entities/** - Base entity classes

---

## Key Features

| Feature | Status |
|---------|--------|
| Entity System | ✅ Done |
| Character System | ✅ Done |
| Player Account & Controller | ✅ Done |
| Input System (Keyboard/Mouse) | ✅ Done |
| Game Engine (RL-ready) | ✅ Done |

---

## Planned Features

| Feature | Status |
|---------|--------|
| Renderer | 🔲 TODO |
| Camera System | 🔲 TODO |
| Attack System | 🔲 TODO |
| Enemy AI | 🔲 TODO |
| Map/Level System | 🔲 TODO |
| UI System | 🔲 TODO |

---

## For RL Developers

```python
from fragment_of_society.game_engine import GameEngine
from fragment_of_society.input import KeyboardInput, MouseInput

engine = GameEngine()
keyboard = KeyboardInput()
mouse = MouseInput()

# Get state
state = engine.get_state()
# {"player_x": ..., "player_y": ..., "player_hp": ..., "player_max_hp": ...}

# Step
engine.update(keyboard, mouse, [], dt)
```

See [GameEngine](./Systems/GAMEENGINE.md) for full RL integration guide.

---

## Running the Game

```bash
cd src
python -m fragment_of_society.main
```

Or:

```bash
python src/fragment_of_society/main.py
```

---

## GitHub

[Repository](https://github.com/aaronmfs/team-sanction)
