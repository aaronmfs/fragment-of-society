# UML Class Diagram - Fragment of Society

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                GAME                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                              Game                                    │   │
│  │  - screen: Surface        - player: Player                          │   │
│  │  - clock: Clock           - player_controller: PlayerController    │   │
│  │  - running: bool          - events: list                           │   │
│  │  - dt: float                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                        │
│  │    PlayerController │    │       Player        │                        │
│  │  - player: Player    │◄───│  +account_name     │                        │
│  │  - character: Char    │    │  +coins            │                        │
│  │  +update()           │    │  +active_character │                        │
│  └─────────────────────┘    │  +keyboard         │                        │
│                            │  +mouse             │                        │
│                            └──────────┬──────────┘                        │
│                                       │                                    │
│                                       ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      CHARACTERS (Entity Hierarchy)                  │   │
│  │                                                                      │   │
│  │    ┌─────────┐         ┌────────────┐         ┌─────────┐          │   │
│  │    │ Entity  │◄────────│  Character │◄────────│ Generic │          │   │
│  │    ├─────────┤         ├────────────┤         └─────────┘          │   │
│  │    │ -id     │         │ +name      │                                │   │
│  │    │ -stats  │         │ +speed     │                                │   │
│  │    │ -pos    │         └────────────┘                                │   │
│  │    │ -_hp    │                                                       │   │
│  │    │ +hp     │                                                       │   │
│  │    │ +update │                                                       │   │
│  │    └─────────┘                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐
│   INPUT SYSTEM      │  │    COMPONENTS       │
│                     │  │                     │
│ ┌─────────────────┐ │  │ ┌─────────────────┐ │
│ │ KeyboardInput   │ │  │ │     Stats       │ │
│ ├─────────────────┤ │  │ ├─────────────────┤ │
│ │ -_bindings      │ │  │ │ +max_hp         │ │
│ │ -_actions_*     │ │  │ │ +attack         │ │
│ │ +bind_key()     │ │  │ │ +defense         │ │
│ │ +is_held()      │ │  │ │ +speed           │ │
│ │ +get_movement() │ │  │ └─────────────────┘ │
│ └─────────────────┘ │  │            │         │
│                     │  │            ▼         │
│ ┌─────────────────┐ │  │ ┌─────────────────┐ │
│ │   MouseInput    │ │  │ │   MageStats     │ │
│ ├─────────────────┤ │  │ ├─────────────────┤ │
│ │ -_button_bind..│ │  │ │ +mana            │ │
│ │ -_mouse_pos    │ │  │ │ +magic_damage    │ │
│ │ +bind_button()  │ │  │ └─────────────────┘ │
│ │ +get_position() │ │  │                     │
│ │ +get_world_pos()│ │  │ ┌─────────────────┐ │
│ └─────────────────┘ │  │ │   KeyBinding   │ │
│                     │  │ ├─────────────────┤ │
│ ┌─────────────────┐ │  │ │ +key            │ │
│ │KeyBinding*      │ │  │ │ +action         │ │
│ ├─────────────────┤ │  │ │ +holdable       │ │
│ │ +key            │ │  │ └─────────────────┘ │
│ │ +action         │ │  │                     │
│ │ +holdable       │ │  │ ┌─────────────────┐ │
│ └─────────────────┘ │  │ │MouseButtonBind..│ │
│                     │  │ ├─────────────────┤ │
│ ┌─────────────────┐ │  │ │ +button         │ │
│ │MouseButtonBind..│ │  │ │ +action         │ │
│ ├─────────────────┤ │  │ └─────────────────┘ │
│ │ +button         │ │  │                     │
│ │ +action         │ │  │ * Helper/Data classes│
│ └─────────────────┘ │  │                     │
└─────────────────────┘  └─────────────────────┘
```

## Inheritance Hierarchy

```
Entity (abstract base)
    │
    └── Character
            │
            └── Generic
            │
            └── (future: PlayerCharacter, Enemy, NPC, etc.)

Stats
    │
    └── MageStats
```

## Relationships Summary

| Relationship | Type | Description |
|-------------|------|-------------|
| Entity → Stats | Composition | Entity owns a Stats object |
| Character → Entity | Inheritance | Character extends Entity |
| Generic → Character | Inheritance | Generic extends Character |
| MageStats → Stats | Inheritance | MageStats extends Stats |
| Player → Character | Aggregation | Player holds active_character |
| Player → KeyboardInput | Composition | Player owns keyboard input |
| Player → MouseInput | Composition | Player owns mouse input |
| Game → Player | Composition | Game owns player |
| Game → PlayerController | Composition | Game owns controller |
| PlayerController → Player | Dependency | Controller references player |
| KeyboardInput → KeyBinding | Composition | Keyboard owns bindings |
| MouseInput → MouseButtonBinding | Composition | Mouse owns bindings |
