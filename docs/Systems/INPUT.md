# Input System Documentation

The input system is designed to be **pygame-free** - it uses plain Python data types, making it compatible with RL training environments.

---

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│   Pygame Events     │────▶│   InputAdapter      │
│  (from game loop)   │     │  (in game.py)       │
└─────────────────────┘     └──────────┬──────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │   KeyboardInput + MouseInput  │
                        │   (Pure Python - RL Friendly) │
                        └───────────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │   PlayerController            │
                        │   (Game Logic)                │
                        └───────────────────────────────┘
```

---

## KeyboardInput

### Quick Start

```python
from fragment_of_society.input import KeyboardInput

keyboard = KeyboardInput()

# In game loop - pass pygame key states
keyboard.set_keys_state(pygame.key.get_pressed())
keyboard.update()

# Check input
if keyboard.is_held("move_up"):
    print("Moving up!")

if keyboard.is_pressed("interact"):
    print("Pressed interact!")

# Get movement vector (normalized)
move_x, move_y = keyboard.get_movement_vector()
```

### Default Bindings

| Action | Key | Holdable |
|--------|-----|----------|
| move_up | W | Yes |
| move_down | S | Yes |
| move_left | A | Yes |
| move_right | D | Yes |
| pause | ESC | No |
| interact | E | No |
| slot_1 | 1 | No |
| slot_2 | 2 | No |
| slot_3 | 3 | No |

### Methods

#### `set_keys_state(keys_state: Dict[int, bool])`
Set the current keyboard state from pygame.

```python
# Called from game.py
keyboard.set_keys_state(pygame.key.get_pressed())
```

#### `update() -> None`
Update pressed/released states. Call once per frame.

#### `is_held(action: str) -> bool`
Returns `True` if the key is currently held down.

```python
if keyboard.is_held("move_up"):
    player.y -= speed
```

#### `is_pressed(action: str) -> bool`
Returns `True` on the frame the key was pressed.

```python
if keyboard.is_pressed("interact"):
    player.interact()
```

#### `is_released(action: str) -> bool`
Returns `True` on the frame the key was released.

#### `get_movement_vector() -> Tuple[float, float]`
Returns normalized direction vector as `(x, y)`.

```python
dx, dy = keyboard.get_movement_vector()
# Returns: (0, 0), (1, 0), (-1, 1), etc.
```

### Custom Bindings

```python
keyboard.bind_key(119, "jump", holdable=False)  # 119 = W keycode
keyboard.unbind_key("slot_1")
```

---

## MouseInput

### Quick Start

```python
from fragment_of_society.input import MouseInput

mouse = MouseInput()

# In game loop - pass pygame events
pygame_events = pygame.event.get()
mouse.set_mouse_position(pygame.mouse.get_pos())
mouse.update(pygame_events)

# Check input
if mouse.is_pressed("attack"):
    print("Attacking!")

# Get position
x, y = mouse.get_position()
```

### Default Bindings

| Action | Button |
|--------|--------|
| attack | Left Click |
| aim | Right Click |
| middle_click | Middle Click |
| wheel_up | Scroll Up |
| wheel_down | Scroll Down |
| back | X1 |
| forward | X2 |

### Methods

#### `set_mouse_position(pos: Tuple[float, float])`
Set current mouse position.

```python
mouse.set_mouse_position(pygame.mouse.get_pos())
```

#### `set_mouse_delta(delta: Tuple[float, float])`
Set mouse movement delta.

```python
mouse.set_mouse_delta(event.rel)  # event.rel from MOUSEMOTION
```

#### `update(event_list: Optional[List] = None) -> None`
Update button states. Pass pygame events list.

```python
mouse.update(pygame.event.get())
```

#### `is_held(action: str) -> bool`
Returns `True` if mouse button is held.

#### `is_pressed(action: str) -> bool`
Returns `True` on the frame button was pressed.

#### `is_released(action: str) -> bool`
Returns `True` on the frame button was released.

#### `get_position() -> Tuple[float, float]`
Returns mouse position as `(x, y)`.

#### `get_delta() -> Tuple[float, float]`
Returns mouse movement since last frame as `(dx, dy)`.

#### `get_wheel_delta() -> int`
Returns scroll wheel delta (-1, 0, or 1).

---

## Integration with Game Loop

### Using with Pygame (Human Playable)

```python
import pygame
from fragment_of_society.input import KeyboardInput, MouseInput

pygame.init()
screen = pygame.display.set_mode((1280, 720))

keyboard = KeyboardInput()
mouse = MouseInput()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    # Update input
    keyboard.set_keys_state(pygame.key.get_pressed())
    mouse.set_mouse_position(pygame.mouse.get_pos())
    keyboard.update()
    mouse.update(events)
    
    # Use input
    dx, dy = keyboard.get_movement_vector()
    if mouse.is_pressed("attack"):
        print("Attack!")
    
    pygame.display.flip()
```

### Using with RL (Headless)

```python
from fragment_of_society.input import KeyboardInput, MouseInput

# No pygame needed!
keyboard = KeyboardInput()
mouse = MouseInput()

# Simulate input (from RL agent)
def step_agent(action):
    # action from RL model: e.g., {"move": [dx, dy], "attack": bool}
    
    # Set keyboard state based on action
    keys_state = {}
    if action.get("move", [0, 0])[1] < 0:
        keys_state[119] = True  # W
    # ... set other keys ...
    keyboard.set_keys_state(keys_state)
    keyboard.update()
    
    # Simulate mouse
    mouse.set_mouse_position(action.get("mouse_pos", (0, 0)))
    if action.get("attack"):
        # Create fake mouse press event
        class FakeEvent:
            type = 5  # MOUSEBUTTONDOWN
            button = 1  # LEFT
        mouse.update([FakeEvent()])
    
    return keyboard.get_movement_vector(), mouse.is_pressed("attack")
```

---

## Key Codes Reference

Common key codes used by KeyboardInput:

| Key | Code |
|-----|------|
| W | 119 |
| A | 97 |
| S | 115 |
| D | 100 |
| Space | 32 |
| Escape | 27 |
| E | 101 |
| 1-9 | 49-57 |

---

## Mouse Button Codes

| Button | Code |
|--------|------|
| Left | 1 |
| Middle | 2 |
| Right | 3 |
| Wheel Up | 4 |
| Wheel Down | 5 |
| X1 | 4 |
| X2 | 5 |
