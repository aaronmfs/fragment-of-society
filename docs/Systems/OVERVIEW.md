# Systems Overview

This document provides an overview of the game's architecture and how all systems work together.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PYGAME LAYER                                │
│  game.py - Window, events, rendering, user input                    │
│  - Uses pygame for display and input                                │
│  - Converts pygame events to plain data                             │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                    keyboard/mouse/input
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PURE PYTHON LAYER                              │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐     │
│  │   GameEngine    │  │    PlayerAccount │  │   Controller    │     │
│  │  - State        │  │  - Character     │  │  - Movement     │     │
│  │  - Update loop  │  │  - Coins         │  │  - Attack       │     │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬────────┘     │
│           │                    │                     │              │
│           └────────────────────┼─────────────────────┘              │
│                                │                                    │
│                    ┌───────────┴───────────┐                        │
│                    │       Entity          │                        │
│                    │  - Position (x, y)    │                        │
│                    │  - Stats (hp, atk)    │                        │
│                    │  - Damage/Heal        │                        │
│                    └───────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
src/fragment_of_society/
├── game.py              # Pygame adapter (rendering, window)
├── game_engine.py       # Pure game logic (no pygame)
├── main.py             # Entry point
│
├── components/
│   └── stats.py        # Stats dataclass
│
├── entities/
│   └── entity.py       # Base entity class
│
├── player/
│   ├── character.py          # Character class
│   ├── player_account.py     # Player account + character
│   └── characters/
│       └── generic.py        # Generic character
│
├── controllers/
│   └── player_controller.py  # Movement logic
│
└── input/
    ├── keyboard_input.py     # Keyboard handling
    └── mouse_input.py       # Mouse handling
```

---

## Data Flow

### Human Playable (with pygame)
```
1. game.py: pygame.event.get() 
2. game.py: pygame.key.get_pressed(), pygame.mouse.get_pos()
3. game.py: Pass to game_engine.update(keyboard, mouse, events, dt)
4. game_engine: Pass to player.update(...)
5. player_account: Pass to player_controller.update(...)
6. player_controller: Update character position
7. game.py: Render character at (x, y)
```

### RL Agent (headless)
```
1. RL Agent: Create keyboard/mouse state
2. RL Agent: Call engine.update(keyboard, mouse, [], dt)
3. RL Agent: Get state via engine.get_state()
4. Repeat
```

---

## Key Principles

1. **No pygame in game logic** - All game logic files use pure Python
2. **Plain data types** - Use tuples, dicts, not pygame.Vector2/Rect
3. **Dependency injection** - Inputs passed in, not created internally
4. **Separation of concerns** - GameEngine handles logic, Game handles rendering

---

## How-to: Add New Systems

When adding new features, follow these principles:
- **Pure Python** - No pygame imports in game logic
- **Plain data types** - Use `tuple[float, float]` not `pygame.Vector2`
- **Dependency injection** - Pass dependencies as parameters
- **Update pattern** - Implement `update(dt)` method for time-based logic

---

### 1. Adding Hitbox

Hitboxes detect collisions between entities.

#### Step 1: Create component file
```python
# src/fragment_of_society/components/hitbox.py

from typing import Tuple, Optional

class Hitbox:
    def __init__(
        self,
        width: float,
        height: float,
        offset_x: float = 0,
        offset_y: float = 0
    ):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self._x: float = 0
        self._y: float = 0

    def set_position(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def get_rect(self) -> Tuple[float, float, float, float]:
        """Returns (x, y, width, height) - no pygame!"""
        return (
            self._x + self.offset_x - self.width / 2,
            self._y + self.offset_y - self.height / 2,
            self.width,
            self.height
        )

    def collides_with(self, other: "Hitbox") -> bool:
        """AABB collision - pure math"""
        self_rect = self.get_rect()
        other_rect = other.get_rect()
        return (self_rect[0] < other_rect[0] + other_rect[2] and
                self_rect[0] + self_rect[2] > other_rect[0] and
                self_rect[1] < other_rect[1] + other_rect[3] and
                self_rect[1] + self_rect[3] > other_rect[1])
```

#### Step 2: Add to Entity
```python
# src/fragment_of_society/entities/entity.py
from fragment_of_society.components.hitbox import Hitbox

class Entity:
    def __init__(self, x: float, y: float, hitbox: Hitbox = None):
        self.x = x
        self.y = y
        self.hitbox = hitbox
        if self.hitbox:
            self.hitbox.set_position(x, y)

    def update(self, dt: float) -> None:
        if self.hitbox:
            self.hitbox.set_position(self.x, self.y)
```

#### Step 3: Use in Controller
```python
# src/fragment_of_society/controllers/combat_controller.py
from fragment_of_society.components.hitbox import Hitbox

class CombatController:
    def check_collision(self, entity_a, entity_b) -> bool:
        if entity_a.hitbox and entity_b.hitbox:
            return entity_a.hitbox.collides_with(entity_b.hitbox)
        return False

    def update(self, entities: list, dt: float) -> None:
        for i, entity in enumerate(entities):
            entity.update(dt)
            if entity.hitbox:
                entity.hitbox.set_position(entity.x, entity.y)
```

---

### 2. Adding Skill System

Skills are abilities characters can use.

#### Step 1: Create Skill base class
```python
# src/fragment_of_society/components/skill.py

from typing import Optional
from dataclasses import dataclass

@dataclass
class Skill:
    name: str
    cooldown: float      # Seconds between uses
    duration: float     # How long skill lasts
    mana_cost: int      # Mana required
    
    last_used: float = 0  # Timestamp of last use
    
    def can_use(self, current_time: float, mana: int) -> bool:
        return (current_time - self.last_used >= self.cooldown and 
                mana >= self.mana_cost)
    
    def use(self, current_time: float) -> None:
        self.last_used = current_time
    
    def update(self, dt: float) -> None:
        """Override for active effects"""
        pass
    
    def is_active(self, current_time: float) -> bool:
        if self.duration <= 0:
            return False
        return current_time - self.last_used < self.duration


class AttackSkill(Skill):
    def __init__(self):
        super().__init__(
            name="Basic Attack",
            cooldown=0.5,
            duration=0,
            mana_cost=0,
            damage=10
        )
        self.damage = 10


class HealSkill(Skill):
    def __init__(self):
        super().__init__(
            name="Heal",
            cooldown=5.0,
            duration=0,
            mana_cost=20,
            heal_amount=30
        )
        self.heal_amount = 30
```

#### Step 2: Add to Character
```python
# src/fragment_of_society/player/character.py
from fragment_of_society.components.skill import Skill

class Character(Entity):
    def __init__(self, name: str, stats, skills: list[Skill] = None):
        super().__init__(...)
        self.skills = skills or []
        self.mana = 100
        self.max_mana = 100
    
    def use_skill(self, skill_index: int, current_time: float) -> bool:
        if skill_index >= len(self.skills):
            return False
        skill = self.skills[skill_index]
        if skill.can_use(current_time, self.mana):
            skill.use(current_time)
            self.mana -= skill.mana_cost
            return True
        return False
    
    def update(self, dt: float) -> None:
        super().update(dt)
        for skill in self.skills:
            skill.update(dt)
```

---

### 3. Adding Combat System

Combat handles damage, effects, and combat logic.

#### Step 1: Create Combat System
```python
# src/fragment_of_society/systems/combat_system.py

from typing import Optional
from fragment_of_society.entities.entity import Entity

class CombatSystem:
    def __init__(self):
        pass
    
    def calculate_damage(
        self,
        attacker: Entity,
        defender: Entity,
        skill_bonus: int = 0
    ) -> int:
        """Calculate damage after defense"""
        base_damage = attacker.stats.attack + skill_bonus
        defense = defender.stats.defense
        return max(1, base_damage - defense)
    
    def apply_damage(
        self,
        defender: Entity,
        damage: int
    ) -> None:
        """Apply damage to defender"""
        defender.take_damage(damage)
    
    def attack(
        self,
        attacker: Entity,
        defender: Entity,
        skill_bonus: int = 0
    ) -> int:
        """Full attack: calculate and apply damage"""
        damage = self.calculate_damage(attacker, defender, skill_bonus)
        self.apply_damage(defender, damage)
        return damage
    
    def check_death(self, entity: Entity) -> bool:
        """Check if entity died"""
        return not entity.is_alive()
    
    def update(self, entities: list, dt: float) -> None:
        """Update all entities in combat"""
        for entity in entities:
            entity.update(dt)
```

#### Step 2: Integrate into GameEngine
```python
# src/fragment_of_society/game_engine.py
from fragment_of_society.systems.combat_system import CombatSystem

class GameEngine:
    def __init__(self):
        self.combat = CombatSystem()
        self.enemies = []
    
    def update(self, keyboard, mouse, events, dt):
        # Update player
        self.player.update(keyboard, mouse, events, dt)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt)
        
        # Check collisions
        self.check_combat()
    
    def check_combat(self):
        if self.player.active_character.hitbox and self.enemies:
            for enemy in self.enemies:
                if self.combat.attack(
                    self.player.active_character,
                    enemy
                ):
                    print(f"Hit enemy! HP: {enemy.hp}")
```

---

### 4. Adding Enemy AI

AI controls enemy behavior.

#### Step 1: Create AI base class
```python
# src/fragment_of_society/ai/base_ai.py

from typing import Protocol

class Entity(Protocol):
    x: float
    y: float
    stats: any

class AI:
    def __init__(self, entity: Entity):
        self.entity = entity
    
    def update(self, target, dt: float) -> None:
        """Override with AI behavior"""
        pass


class ChaseAI(AI):
    """Simple chase AI - moves toward target"""
    def update(self, target, dt: float) -> None:
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 0:
            speed = 100 * (1 + self.entity.stats.speed / 100)
            self.entity.x += (dx / distance) * speed * dt
            self.entity.y += (dy / distance) * speed * dt


class PatrolAI(AI):
    """Patrol between points"""
    def __init__(self, entity, waypoints: list):
        super().__init__(entity)
        self.waypoints = waypoints
        self.current_index = 0
    
    def update(self, target, dt: float) -> None:
        waypoint = self.waypoints[self.current_index]
        dx = waypoint[0] - self.entity.x
        dy = waypoint[1] - self.entity.y
        
        distance = (dx * dx + dy * dy) ** 0.5
        if distance < 10:
            self.current_index = (self.current_index + 1) % len(self.waypoints)
        else:
            speed = 50 * (1 + self.entity.stats.speed / 100)
            self.entity.x += (dx / distance) * speed * dt
            self.entity.y += (dy / distance) * speed * dt
```

#### Step 2: Add to Enemy
```python
# src/fragment_of_society/enemies/base_enemy.py

from fragment_of_society.entities.entity import Entity
from fragment_of_society.ai.base_ai import ChaseAI

class Enemy(Entity):
    def __init__(self, x: float, y: float, ai: AI = None):
        super().__init__(x, y)
        self.ai = ai or ChaseAI(self)
    
    def update(self, dt: float, target) -> None:
        if self.ai:
            self.ai.update(target, dt)
        super().update(dt)
```

---

## Checklist for New Systems

- [ ] Create pure Python class (no pygame imports)
- [ ] Use plain data types (tuple, dict, not Vector2/Rect)
- [ ] Implement `update(dt)` method for time-based logic
- [ ] Add to appropriate layer (Entity, Controller, or System)
- [ ] Integrate into GameEngine
- [ ] Add to get_state() for RL observations
- [ ] Add rendering in game.py (pygame layer)
