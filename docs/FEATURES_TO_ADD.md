# Features to Be Added

## 1. Hitbox (Easy)
**Location:** `src/fragment_of_society/components/hitbox.py`

**Description:** Component class for entity collision detection.

**Suggested structure:**
```python
class Hitbox:
    def __init__(self, width, height, offset_x=0, offset_y=0):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
```

**Depends on:** Nothing

---

## 2. Renderer (Easy)
**Location:** `src/fragment_of_society/renderers/renderer.py`

**Description:** Base renderer class for drawing entities to screen.

**Suggested structure:**
```python
class Renderer:
    def __init__(self, screen):
        self.screen = screen
    
    def render(self, entity):
        raise NotImplementedError
```

**Depends on:** Nothing

---

## 3. Attack (Medium)
**Location:** `src/fragment_of_society/systems/attack.py`

**Description:** System for handling attack logic (cooldowns, damage calculation, animation triggers).

**Suggested structure:**
```python
class Attack:
    def __init__(self, damage, cooldown, attack_type):
        self.damage = damage
        self.cooldown = cooldown
        self.last_used = 0
        self.attack_type = attack_type
    
    def can_attack(self, current_time):
        pass
    
    def execute(self, attacker, target):
        pass
```

**Depends on:** Entity (for attacker/target)

---

## 4. AttackHitbox (Hard)
**Location:** `src/fragment_of_society/systems/attack.py`

**Description:** Temporal hitbox created during an attack animation that deals damage to entities it intersects.

**Suggested structure:**
```python
class AttackHitbox:
    def __init__(self, owner, offset, size, duration, damage):
        self.owner = owner
        self.offset = offset
        self.size = size
        self.duration = duration
        self.damage = damage
        self.created_at = 0
        self.active = False
    
    def activate(self, current_time):
        pass
    
    def check_collision(self, entity):
        pass
    
    def deactivate(self):
        pass
```

**Depends on:** Entity, Hitbox, Attack

---

## Summary

| Feature | Location | Difficulty |
|---------|----------|------------|
| Hitbox | `components/hitbox.py` | Easy |
| Renderer | `renderers/renderer.py` | Easy |
| Attack | `systems/attack.py` | Medium |
| AttackHitbox | `systems/attack.py` | Hard |

---

## Directory Structure After Adding

```
src/fragment_of_society/
├── components/
│   ├── stats.py
│   └── hitbox.py          # NEW
├── systems/
│   └── attack.py          # NEW
├── renderers/
│   └── renderer.py        # NEW
├── entities/
├── input/
└── controllers/
```
