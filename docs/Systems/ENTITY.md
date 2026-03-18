# Entity System

The entity system provides the base classes for all game objects. It's designed to be **pure Python** with no pygame dependencies.

---

## Stats

### Location
`src/fragment_of_society/components/stats.py`

### Overview
Data class holding character statistics.

### Class Reference

```python
@dataclass
class Stats:
    max_hp: int      # Maximum health points
    attack: int      # Attack damage
    defense: int     # Damage reduction
    speed: int       # Movement speed multiplier (affects final speed)
    
    def get_damageReduction(self, incoming: int) -> int:
        # Returns damage after defense
        # Formula: max(1, incoming - defense)
        # Minimum damage is always 1
```

### Extended Stats

```python
class MageStats(Stats):
    mana: int           # Magic energy
    magic_damage: int   # Magic attack damage
```

### Usage Example

```python
from fragment_of_society.components import Stats

# Create stats
stats = Stats(
    max_hp=100,
    attack=15,
    defense=10,
    speed=20
)

# Calculate damage reduction
damage = stats.get_damageReduction(25)  # 25 - 10 = 15 damage
min_damage = stats.get_damageReduction(5)  # max(1, 5 - 10) = 1 damage
```

---

## Entity

### Location
`src/fragment_of_society/entities/entity.py`

### Overview
Base class for all game objects that have health. Pure Python - no pygame.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| x | float | X position |
| y | float | Y position |
| id | uuid.UUID | Unique identifier |
| stats | Stats | Entity statistics |
| hp | int | Current health (property) |

### Class Reference

```python
class Entity:
    def __init__(
        self,
        x: float,
        y: float,
        stats: Stats | None = None
    ) -> None:
        # Creates entity at (x, y) with optional stats
        # Default stats: max_hp=10, attack=10, defense=10, speed=10

    @property
    def hp(self) -> int:
        # Returns current HP
        
    @hp.setter
    def hp(self, value: int) -> None:
        # Sets HP, clamped to [0, max_hp]
        
    def update(self, dt: float) -> None:
        # Override for per-frame logic
        pass
        
    def take_damage(self, amount: int) -> None:
        # Reduces HP by (amount - defense), minimum 1 damage
        
    def heal(self, amount: int) -> None:
        # Increases HP, capped at max_hp
        
    def is_alive(self) -> bool:
        # Returns True if HP > 0
```

### Usage Example

```python
from fragment_of_society.entities import Entity
from fragment_of_society.components import Stats

# Create entity
entity = Entity(100, 200, Stats(max_hp=100, attack=10, defense=5, speed=10))

# Modify HP
entity.take_damage(20)  # Takes 15 damage (20 - 5 defense)
entity.heal(10)       # Heals 10 HP

# Check status
if entity.is_alive():
    print(f"Alive! HP: {entity.hp}/{entity.stats.max_hp}")
```

---

## Character

### Location
`src/fragment_of_society/player/character.py`

### Overview
Extends Entity with character-specific attributes for player characters.

### Class Reference

```python
class Character(Entity):
    def __init__(
        self,
        name: str,
        stats: Stats,
        x: float = 0,
        y: float = 0
    ) -> None:
        # Creates character at (x, y) with name and stats
        
    def __repr__(self) -> str:
        # Returns: "Character(name, id=..., hp=.../...)"
```

### Usage Example

```python
from fragment_of_society.player.character import Character
from fragment_of_society.components import Stats

# Create character
char = Character(
    name="Hero",
    stats=Stats(max_hp=100, attack=15, defense=10, speed=20),
    x=100,
    y=200
)

print(char)  # Character(Hero, id=..., hp=100/100)
```

---

## PlayerAccount

### Location
`src/fragment_of_society/player/player_account.py`

### Overview
Manages player account data and connects to player controller.

### Class Reference

```python
class PlayerAccount:
    def __init__(
        self,
        account_name: str,
        coins: int,
        active_character: Character
    ) -> None:
        # Creates account with character
        
    def update(
        self,
        keyboard: KeyboardInput,
        mouse: MouseInput,
        events: list,
        dt: float
    ) -> None:
        # Updates player controller with input
```

### Usage Example

```python
from fragment_of_society.player.player_account import PlayerAccount
from fragment_of_society.player.characters import Generic
from fragment_of_society.input import KeyboardInput, MouseInput

# Create player
player = PlayerAccount("Player1", 100, Generic(400, 300))

# Update with input
keyboard = KeyboardInput()
mouse = MouseInput()

player.update(keyboard, mouse, [], 0.016)  # dt = 16ms
```

---

## PlayerController

### Location
`src/fragment_of_society/controllers/player_controller.py`

### Overview
Translates input into character movement. Pure Python - handles movement logic.

### Class Reference

```python
class PlayerController:
    def __init__(self, character: Character) -> None:
        # Creates controller for character
        
    def handle_movement(self, keyboard: KeyboardInput, dt: float) -> None:
        # Calculates final speed: 650 * (1 + stats.speed / 100)
        # Updates character position based on keyboard input
        
    def update(
        self,
        keyboard: KeyboardInput,
        mouse: MouseInput,
        events: list,
        dt: float
    ) -> None:
        # Updates keyboard/mouse states
        # Calls handle_movement
```

### Movement Speed Formula

```
final_speed = 650 * (1 + stats.speed / 100)
```

| Speed Stat | Multiplier | Final Speed |
|------------|------------|-------------|
| 0 | 1.0 | 650 |
| 10 | 1.1 | 715 |
| 20 | 1.2 | 780 |
| 50 | 1.5 | 975 |
| 100 | 2.0 | 1300 |

---

## Inheritance Hierarchy

```
Entity (entities/entity.py)
    │
    └── Character (player/character.py)
            │
            └── Generic (player/characters/generic.py)
```

---

## Adding New Character Types

Create a new file in `player/characters/`:

```python
# player/characters/warrior.py
from fragment_of_society.player.character import Character
from fragment_of_society.components import Stats

class Warrior(Character):
    def __init__(self, x, y, name="Warrior"):
        stats = Stats(
            max_hp=120,
            attack=20,
            defense=15,
            speed=10
        )
        super().__init__(name=name, stats=stats, x=x, y=y)
```

Then import it:

```python
from fragment_of_society.player.characters.warrior import Warrior
```
