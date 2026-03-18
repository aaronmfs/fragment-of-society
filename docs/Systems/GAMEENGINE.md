# Game Engine

The GameEngine is the core of the game's logic layer. It's **pure Python** with no pygame dependencies, making it perfect for RL training.

---

## Location

`src/fragment_of_society/game_engine.py`

---

## Overview

GameEngine handles all game logic without any rendering or window management. It can run headless (no display) for RL training.

---

## Class Reference

```python
class GameEngine:
    def __init__(self, screen_width: int = 1280, screen_height: int = 720):
        # Initializes game with player at center of screen
        
    def update(
        self,
        keyboard: KeyboardInput,
        mouse: MouseInput,
        events: list,
        dt: float
    ) -> None:
        # Updates game state with input
        # Call once per frame
        
    def get_state(self) -> dict:
        # Returns current game state as dict
        # For RL observations
```

---

## Game State

`get_state()` returns:

```python
{
    "player_x": float,      # Player X position
    "player_y": float,      # Player Y position
    "player_hp": int,       # Current HP
    "player_max_hp": int    # Maximum HP
}
```

---

## Usage Examples

### Human Playable (with game.py)

```python
# game.py handles this automatically
from fragment_of_society.game import Game

game = Game()
game.run()
```

### RL Agent (Headless)

```python
from fragment_of_society.game_engine import GameEngine
from fragment_of_society.input import KeyboardInput, MouseInput
import time

# Initialize (no pygame needed!)
engine = GameEngine(1280, 720)
keyboard = KeyboardInput()
mouse = MouseInput()

# Training loop
for episode in range(1000):
    # Reset
    engine = GameEngine()
    
    for step in range(1000):
        # Get current state
        state = engine.get_state()
        
        # RL agent chooses action
        action = agent.select_action(state)
        
        # Convert RL action to input
        keys_state = {i: False for i in range(512)}
        if action == "up":
            keys_state[119] = True   # W
        elif action == "down":
            keys_state[115] = True   # S
        # ... etc
        
        keyboard.set_keys_state(keys_state)
        keyboard.update()
        
        # Step simulation
        engine.update(keyboard, mouse, [], 0.016)
        
        # Check if episode done
        if state["player_hp"] <= 0:
            break
```

### Minimal Example

```python
from fragment_of_society.game_engine import GameEngine
from fragment_of_society.input import KeyboardInput, MouseInput

engine = GameEngine()
keyboard = KeyboardInput()
mouse = MouseInput()

# Step without input (player stands still)
engine.update(keyboard, mouse, [], 0.016)

# Get state
state = engine.get_state()
print(f"Position: ({state['player_x']}, {state['player_y']})")
print(f"HP: {state['player_hp']}/{state['player_max_hp']}")
```

---

## Game.py (Pygame Adapter)

For human playability, `game.py` wraps GameEngine with pygame:

```python
import pygame
from fragment_of_society.game_engine import GameEngine
from fragment_of_society.input import KeyboardInput, MouseInput

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.engine = GameEngine(1280, 720)
        self.keyboard = KeyboardInput()
        self.mouse = MouseInput()
        self.dt = 0.0

    def run(self):
        while self.engine.running:
            # Handle pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.engine.running = False
            
            # Update inputs
            self.keyboard.set_keys_state(pygame.key.get_pressed())
            self.mouse.set_mouse_position(pygame.mouse.get_pos())
            
            # Update engine
            self.engine.update(self.keyboard, self.mouse, events, self.dt)
            
            # Render
            self.screen.fill("purple")
            x = self.engine.player.active_character.x
            y = self.engine.player.active_character.y
            pygame.draw.circle(self.screen, "red", (int(x), int(y)), 40)
            pygame.display.flip()
            
            self.dt = self.clock.tick(60) / 1000
```

---

## For RL Integration

The GameEngine provides:

1. **State observations** via `get_state()`
2. **Step function** via `update(keyboard, mouse, events, dt)`
3. **Pure Python** - no graphics dependencies

### Typical RL Loop

```python
engine = GameEngine()
keyboard = KeyboardInput()
mouse = MouseInput()

while True:
    # 1. Get observation
    obs = engine.get_state()
    
    # 2. Agent chooses action
    action = agent.act(obs)
    
    # 3. Convert action to input
    keys = action_to_keys(action)
    keyboard.set_keys_state(keys)
    keyboard.update()
    
    # 4. Step
    engine.update(keyboard, mouse, [], dt)
    
    # 5. Check reward/done
    reward = compute_reward(obs, engine.get_state())
    done = obs["player_hp"] <= 0
```

---

## Extending for RL

To add more state for RL:

```python
# In game_engine.py
def get_state(self) -> dict:
    return {
        "player_x": self.player.active_character.x,
        "player_y": self.player.active_character.y,
        "player_hp": self.player.active_character.hp,
        "player_max_hp": self.player.active_character.stats.max_hp,
        # Add more for RL:
        # "coins": self.player.coins,
        # "enemy_count": len(self.enemies),
    }
```
