# Trello Card Tracker

## In Progress

---

## Done

### Entity System
[Entity]: add entity base classes
WHAT: Base entity classes for all game objects

WHY: Foundation for all game objects
Checklist
- [x] entity base class
- [x] entity properties (x, y, rotation)

### Character System
[Character]: add character classes
WHAT: Character classes with stats and abilities

WHY: Player and NPCs need character system
Checklist
- [x] base character class
- [x] stats component
- [x] character inheritance

### Player Controller
[Player]: add player controller
WHAT: Player input handling and state management

WHY: Player needs to control character
Checklist
- [x] input handling
- [x] movement control
- [x] state management

### Input System
[Input]: add keyboard and mouse detection
WHAT: Keyboard and Mouse detection

WHY: for player ingame interaction
Checklist
- [x] keyboard
- [x] mouse
- [x] input manager

### Game Engine
[GameEngine]: add RL-ready game engine
WHAT: Pure Python game engine for RL training

WHY: Enables RL agents to interact with game
Checklist
- [x] game state management
- [x] entity updates
- [x] camera integration

### Renderer
[Renderer]: add debug and hitbox rendering
WHAT: Debug renderer and hitbox visualizer

WHY: Visual debugging during development
Checklist
- [x] debug renderer
- [x] hitbox renderer

### Camera System
[Camera]: add camera system
WHAT: Camera following player with world bounds

WHY: Viewport management for large worlds
Checklist
- [x] camera follow
- [x] world bounds
- [x] offset calculation

### Skills System
[Skills]: add skill system
WHAT: Composable skill system with SkillBuilder

WHY: Characters need skills for combat
Checklist
- [x] skill class
- [x] skill effects (damage, heal, buff, debuff, shield)
- [x] skill builder
- [x] pre-built skill library

### Attack System
[Attack]: add attack system
WHAT: Basic attack and skill attacks with hitboxes

WHY: Combat requires attack functionality
Checklist
- [x] basic attack
- [x] attack hitbox generation
- [x] AoE attacks

---

## Backlog

### Enemy AI
[EnemyAI]: add enemy AI
WHAT: Enemy behavior and decision making

WHY: Game needs challenges
Checklist
- [ ] basic AI
- [ ] pathfinding
- [ ] combat AI

### Map/Level System
[Map]: add map and level system
WHAT: Level loading and map tiles

WHY: Game needs environments
Checklist
- [ ] tile map
- [ ] level loader
- [ ] level editor
- [ ] world generation

### UI System
[UI]: add UI system
WHAT: HUD, menus, and overlays

WHY: Player feedback and navigation
Checklist
- [ ] HUD
- [ ] menus
- [ ] overlays

### Sprite Renderer
[Sprite]: add sprite renderer
WHAT: Sprite rendering for entities

WHY: Replace debug shapes with actual graphics
Checklist
- [ ] sprite loading
- [ ] sprite batching
- [ ] animation system
