```mermaid
classDiagram
    %% Data Classes
    class Stats {
        +int max_hp
        +int attack
        +int defense
        +int speed
    }
    
    class MageStats {
        +int mana
        +int magic_damage
    }
    
    class KeyBinding {
        +int key
        +str action
        +bool holdable
    }
    
    class MouseButtonBinding {
        +int button
        +str action
    }

    %% Inheritance Relationships
    MageStats --|> Stats : extends
    
    %% Entity Hierarchy
    class Entity {
        -UUID id
        -Stats stats
        -pygame.Vector2 pos
        -int _hp
        +hp: int {property}
        +update(dt: float)
        +take_damage(amount: int)
        +heal(amount: int)
        +is_alive(): bool
    }
    
    class Character {
        +str name
        +float speed
    }
    
    class Generic {
        +__init__(x, y, name, stats)
    }
    
    Entity <|-- Character
    Character <|-- Generic
    
    %% Player and Controllers
    class Player {
        +str account_name
        +int coins
        +Character active_character
        +KeyboardInput keyboard
        +MouseInput mouse
        +update(events: list)
    }
    
    class PlayerController {
        -Player player
        -Character character
        +update(dt: float)
    }
    
    PlayerController --> Player : controls
    
    %% Input Classes
    class KeyboardInput {
        -Dict~str, KeyBinding~ _bindings
        -set _actions_pressed
        -set _actions_just_pressed
        -set _actions_just_released
        +bind_key(key: int, action: str, holdable: bool)
        +unbind_key(action: str)
        +update()
        +is_held(action: str): bool
        +is_pressed(action: str): bool
        +is_released(action: str): bool
        +get_movement_vector(): pygame.math.Vector2
    }
    
    class MouseInput {
        -Dict~str, MouseButtonBinding~ _button_bindings
        -set _buttons_pressed
        -set _buttons_just_pressed
        -set _buttons_just_released
        -pygame.math.Vector2 _mouse_pos
        -pygame.math.Vector2 _mouse_delta
        -int _wheel_y
        -bool _relative_mode
        +bind_button(button: int, action: str)
        +unbind_button(action: str)
        +update(event_list: list)
        +is_held(action: str): bool
        +is_pressed(action: str): bool
        +is_released(action: str): bool
        +get_position(): pygame.math.Vector2
        +get_delta(): pygame.math.Vector2
        +get_wheel_delta(): int
        +set_relative_mode(enabled: bool)
        +is_relative_mode(): bool
        +hide_cursor()
        +show_cursor()
        +get_world_position(camera_offset, zoom): pygame.math.Vector2
    }
    
    %% Game Class
    class Game {
        +pygame.Surface screen
        +pygame.time.Clock clock
        +bool running
        +float dt
        +Player player
        +PlayerController player_controller
        -list events
        +handle_events()
        +update()
        +draw()
        +run()
    }
    
    %% Relationships
    Entity --> Stats : has
    Player --> Character : active_character
    Player --> KeyboardInput : keyboard
    Player --> MouseInput : mouse
    Game --> Player : player
    Game --> PlayerController : player_controller
    KeyboardInput --> KeyBinding : uses
    MouseInput --> MouseButtonBinding : uses
```
