# Fragment of Society - Game Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Architecture](#architecture)
4. [Core Components](#core-components)
5. [Input System](#input-system)
6. [Game Loop](#game-loop)
7. [Adding New Features](#adding-new-features)
8. [Running the Game](#running-the-game)
9. [Future Features](#future-features)

---

## Project Overview

**Fragment of Society** is a 2D top-down dungeon crawler game built with Python and Pygame. The game explores real social issues through its level design and narrative.

### Game Concept

- **Genre:** Top-down pixel dungeon crawler
- **Inspiration:** Soul Knight, Super Mario
- **Core Loop:** Explore levels → Fight enemies → Defeat boss → Unlock next level

### Tech Stack

- **Language:** Python 3.x
- **Game Engine:** Pygame
- **Architecture:** Component-based Entity System

---

## Project Structure

```
team-sanction/
├── src/
│   └── fragment_of_society/
│       ├── components/
│       │   ├── __init__.py
│       │   ├── stats.py          # Stats dataclass for entities
│       │   └── hitbox.py         # Hitbox, HitboxGroup, AttackHitbox
│       ├── entities/
│       │   └── entity.py         # Base Entity class
│       ├── player/
│       │   ├── player_account.py # Player account (manages character + input)
│       │   ├── character.py      # Character class (extends Entity)
│       │   └── characters/
│       │       ├── __init__.py
│       │       └── generic.py   # Generic character type (extends Character)
│       ├── enemies/
│       │   └── generic_enemy.py  # Generic enemy (extends Entity)
│       ├── controllers/
│       │   └── player_controller.py  # Handles player movement
│       ├── input/
│       │   ├── __init__.py
│       │   ├── keyboard_input.py # Keyboard input handling
│       │   └── mouse_input.py    # Mouse input handling
│       ├── game.py               # Main Game class
│       └── main.py               # Entry point
├── docs/
│   ├── README.md                 # Quick reference
│   ├── FEATURES_TO_ADD.md       # Planned features
│   └── UMLClass/                 # UML diagrams
└── README.md                     # Project readme
```

---

## Architecture

### Entity-Component System

The game uses a simple Entity-Component pattern:

```
Entity (base class)
    ├── Character (player characters)
    │       └── Generic (specific character type)
    └── GenericEnemy (enemies)
```

### Key Design Patterns

1. **Component Pattern:** Stats and Hitboxes are passed as separate objects to entities
2. **Controller Pattern:** PlayerController handles input-to-movement translation
3. **Input Abstraction:** Keyboard and Mouse are abstracted into separate classes

### Data Flow

```
User Input → Input Classes → Player → PlayerController → Character Position Update
                     ↓
                  Game Loop (handle_events → update → draw)
```

---

## Core Components

### 1. Stats (`components/stats.py`)

Data class holding character statistics.

```python
@dataclass
class Stats:
    max_hp: int      # Maximum health points
    attack: int     # Attack damage
    defense: int    # Damage reduction
    speed: int      # Movement speed multiplier
```

**Extended Stats:**
```python
@dataclass
class MageStats(Stats):  # For magic-using characters
    mana: int           # Magic energy
    magic_damage: int   # Magic attack damage
```

---

### 2. Entity (`entities/entity.py`)

Base class for all game objects that have health.

**Properties:**
- `id`: Unique identifier (UUID)
- `stats`: Stats object
- `pos`: Position (pygame.Vector2)
- `hp`: Current health (property with getter/setter)
- `hitbox`: Optional Hitbox for collision detection
- `hitboxes`: HitboxGroup containing all hitboxes

**Methods:**
- `update(dt)`: Override for per-frame logic
- `take_damage(amount)`: Reduce HP
- `heal(amount)`: Increase HP (capped at max_hp)
- `is_alive()`: Check if HP > 0
- `get_hitbox_rect()`: Get pygame.Rect for collision

**HP Property Logic:**
```python
@hp.setter
def hp(self, value: int) -> None:
    self._hp = max(0, min(value, self.stats.max_hp))  # Clamped to [0, max_hp]
```

---

### 3. Character (`player/character.py`)

Extends Entity with character-specific attributes for player characters.

**Properties:**
- `name`: Character name
- `speed`: Movement speed in pixels/second

**Constructor:**
```python
def __init__(self, name: str, stats: Stats, speed: float = 650, x: float = 0, y: float = 0, hitbox = None):
```

---

### 4. Generic (`player/characters/generic.py`)

A basic player character class extending Character. Used as the default character.

```python
class Generic(Character):
    def __init__(self, x, y, name="Generic", stats=None, hitbox=None, speed=30):
```

---

### 5. PlayerAccount (`player/player_account.py`)

Manages player account data and input handling.

**Properties:**
- `account_name`: Player's account name
- `coins`: Currency for unlocking characters
- `active_character`: Currently controlled Character
- `keyboard`: KeyboardInput instance
- `mouse`: MouseInput instance

**Methods:**
- `update(events)`: Update input states

---

### 6. GenericEnemy (`enemies/generic_enemy.py`)

A basic enemy class extending Entity. Used as a template for creating enemies.

```python
class GenericEnemy(Entity):
    def __init__(self, name="Generic Enemy", stats=None, x=0, y=0, hitbox=None):
```

---

### 7. Hitbox (`components/hitbox.py`)

Collision detection component that can be attached to entities.

**Properties:**
- `width`: Hitbox width
- `height`: Hitbox height
- `offset_x`: X offset from entity position
- `offset_y`: Y offset from entity position

**Methods:**
- `set_parent(pos)`: Link hitbox to entity position
- `get_rect()`: Get pygame.Rect for collision
- `get_center()`: Get center position as Vector2
- `collides_with(other)`: Check collision with another Hitbox
- `contains_point(x, y)`: Check if point is inside
- `draw(surface, color, width)`: Draw hitbox outline (debug)

---

### 8. HitboxGroup (`components/hitbox.py`)

Group of hitboxes for entities with multiple collision areas.

**Methods:**
- `add(hitbox)`: Add hitbox to group
- `remove(hitbox)`: Remove hitbox from group
- `clear()`: Remove all hitboxes
- `collides_with(hitbox)`: Check if any hitbox collides
- `collides_with_group(other_group)`: Check collision with another group
- `draw(surface, color, width)`: Draw all hitboxes

---

### 9. AttackHitbox (`components/hitbox.py`)

Temporary hitbox for melee attacks with damage and knockback.

**Properties:**
- `duration`: How long the hitbox lasts (seconds)
- `damage`: Damage dealt on hit
- `knockback`: Knockback force

**Methods:**
- `activate()`: Start the attack
- `deactivate()`: End the attack early
- `update(dt)`: Update timer, returns True if still active
- `is_active()`: Check if attack is ongoing
- `draw(surface, color, width)`: Only draws when active

---

### 6. PlayerController (`controllers/player_controller.py`)

Translates input into character movement.

**Logic:**
1. Gets movement vector from keyboard
2. Calculates final speed: `base_speed * (1 + stats.speed / 100)`
3. Updates character position: `pos += movement * final_speed * dt`

---

### 7. Game (`game.py`)

Main game orchestrator.

**Responsibilities:**
- Window/screen management
- Game clock management
- Event handling
- Game state updates
- Rendering

**Key Attributes:**
- `screen`: Pygame display surface
- `clock`: Frame rate controller
- `running`: Main loop flag
- `dt`: Delta time (seconds since last frame)
- `player`: Player instance
- `player_controller`: PlayerController instance

**Game Loop:**
```python
def run(self):
    while self.running:
        self.handle_events()  # Process input
        self.update()          # Update game state
        self.draw()            # Render
        self.dt = self.clock.tick(60) / 1000  # 60 FPS, dt in seconds
```

---

## Input System

### KeyboardInput (`input/keyboard_input.py`)

Handles keyboard button presses and key bindings.

**Default Bindings:**
| Key | Action |
|-----|--------|
| W | move_up |
| S | move_down |
| A | move_left |
| D | move_right |
| SPACE | jump |
| ESCAPE | pause |
| E | interact |
| 1-4 | slot_1-4 |
| I | inventory |
| TAB | map |

**Methods:**
- `bind_key(key, action, holdable)`: Assign action to key
- `unbind_key(action)`: Remove binding
- `update()`: Poll current key states
- `is_held(action)`: Returns True if key is currently held
- `is_pressed(action)`: Returns True on key press frame
- `is_released(action)`: Returns True on key release frame
- `get_movement_vector()`: Returns normalized direction vector

---

### MouseInput (`input/mouse_input.py`)

Handles mouse buttons and position.

**Default Bindings:**
| Button | Action |
|--------|--------|
| Left | attack |
| Right | aim |
| Middle | middle_click |
| Wheel Up | wheel_up |
| Wheel Down | wheel_down |
| X1 | back |
| X2 | forward |

**Methods:**
- `bind_button(button, action)`: Assign action to mouse button
- `update(event_list)`: Process mouse events
- `is_held(action)`: Check if button held
- `is_pressed(action)`: Check if button just pressed
- `get_position()`: Get mouse screen position
- `get_delta()`: Get mouse movement since last frame
- `get_world_position(camera_offset, zoom)`: Convert screen to world coords

---

## Adding New Features

### 1. Adding a New Character Type

Create a new file in `player/characters/`:

```python
# player/characters/warrior.py
from fragment_of_society.player.character import Character
from fragment_of_society.components.stats import Stats

class Warrior(Character):
    def __init__(self, x, y, name="Warrior", stats=None, hitbox=None, speed=50):
        if stats is None:
            stats = Stats(max_hp=100, attack=15, defense=10, speed=20)
        super().__init__(name, stats, speed, x, y, hitbox)
```

### 2. Adding a New Enemy Type

Create a new file in `enemies/`:

```python
# enemies/slime.py
from fragment_of_society.components import Stats, Hitbox
from fragment_of_society.enemies.generic_enemy import GenericEnemy

class Slime(GenericEnemy):
    def __init__(self, x, y):
        stats = Stats(max_hp=30, attack=5, defense=2, speed=15)
        hitbox = Hitbox(width=30, height=30)
        super().__init__(name="Slime", stats=stats, x=x, y=y, hitbox=hitbox)
```

### 3. Adding a New Component

Create a new file in `components/`:

```python
# components/inventory.py
from dataclasses import dataclass

@dataclass
class Inventory:
    capacity: int = 20
    items: list = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []
    
    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False
```

### 4. Adding a New System

Create a new file in `systems/`:

```python
# systems/combat.py
class CombatSystem:
    def __init__(self, game):
        self.game = game
    
    def process_attack(self, attacker, target):
        damage = attacker.stats.attack - target.stats.defense
        target.take_damage(max(1, damage))  # Minimum 1 damage
```

### 5. Adding a New Renderer

Create a new file in `renderers/`:

```python
# renderers/entity_renderer.py
class EntityRenderer:
    def __init__(self, screen):
        self.screen = screen
    
    def render(self, entity):
        # Draw entity to screen
        pass
```

---

## Running the Game

### Prerequisites

```bash
pip install pygame
```

### Run the Game

```bash
cd src
python -m fragment_of_society.main
```

Or simply:

```bash
python src/fragment_of_society/main.py
```

### Controls

- **WASD**: Move
- **Mouse**: Aim/Attack
- **ESC**: Pause

---

## Future Features

See [FEATURES_TO_ADD.md](./FEATURES_TO_ADD.md) for detailed information on planned features.

| Feature | Status |
|---------|--------|
| Hitbox | ✅ DONE |
| AttackHitbox | ✅ DONE |
| Renderer | TODO |
| Attack System | TODO |
| Camera System | TODO |
| Enemy AI | TODO |

---

## Conventions

### Naming

- Classes: `PascalCase` (e.g., `PlayerController`)
- Methods/Variables: `snake_case` (e.g., `get_movement_vector`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_SPEED`)

### File Organization

- One class per file (unless tightly coupled)
- File name matches class name (lowercase)
- Dataclasses for simple data containers
- Properties for computed values

### Type Hints

Always use type hints for function signatures:

```python
def update(self, dt: float) -> None:
    ...

def get_position(self) -> pygame.math.Vector2:
    ...
```

---

## Troubleshooting

### Pygame not found
```bash
pip install pygame
```

### Import errors
Make sure you're running from the correct directory:
```bash
cd src
python -m fragment_of_society.main
```

### Performance issues
- Check `dt` calculation in game loop
- Ensure delta time is used for all movement calculations

---

## Contributing

When adding new features:

1. Create placeholder files as documented in `FEATURES_TO_ADD.md`
2. Add TODO comments with detailed implementation notes
3. Update UML diagrams in `docs/UMLClass/`
4. Update this documentation

---

*Last Updated: March 2026*
