import pygame

from fragment_of_society.core import config
from fragment_of_society.entities import Player
from fragment_of_society.entities.enemy import Enemy
from fragment_of_society.world.tile_map import TileMap
from fragment_of_society.rendering import Camera, HitboxRenderer
from fragment_of_society.inputs import InputManager, GameAction # ✅ Added GameAction
from fragment_of_society.components import Collision # ✅ Moved to top

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Fragment of Society")
        self.clock = pygame.time.Clock()

        self.player = Player(x=200, y=200)
        self.player.base_speed = 300 
        self.enemies = []
        self.tilemap = TileMap()
        self.camera = Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.camera.follow(self.player)
        self.hitbox_renderer = HitboxRenderer(self.screen)
        
        # Input Manager Setup & Editor Key Mapping
        self.input_manager = InputManager.get_instance()
        self.input_manager.map_key(pygame.K_TAB, GameAction.EDITOR_TOGGLE)
        self.input_manager.map_key(pygame.K_o, GameAction.EDITOR_SAVE)
        self.input_manager.map_key(pygame.K_p, GameAction.EDITOR_LOAD)
        self.input_manager.map_key(pygame.K_n, GameAction.EDITOR_NEXT_TILE)

        self.running = True
        self.dt = 0.0
        
        self.edit_mode = False
        
        # Setup our brush cycle: Wall, Eraser/Floor, Player Spawn, Enemy Spawn
        self.available_tiles = [1, 0, 99, 50]
        self.tile_names = {1: "Wall", 0: "Eraser", 99: "Player Spawn", 50: "Enemy Spawn"}
        self.current_tile_idx = 0
        self.current_tile = self.available_tiles[self.current_tile_idx]
        
        self.ui_font = pygame.font.SysFont(None, 36)
        self.resizing_map = False
        self.size_input_text = ""
        self.game_state = "PLAYING" # Can be: "PLAYING", "GAME_OVER", "ROOM_CLEARED"
        self.apply_map_spawns()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            #Handle Text Input Mode First
            if self.resizing_map:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            # Parse "20 15" or "20x15" or "20,15"
                            clean_str = self.size_input_text.replace('x', ' ').replace(',', ' ')
                            w, h = map(int, clean_str.split())
                            self.tilemap.resize(w, h)
                            print(f"Map successfully resized to {w}x{h}!")
                        except ValueError:
                            print("Invalid input. Please use format 'Width Height' (e.g., '20 15').")
                        
                        self.resizing_map = False
                        self.size_input_text = ""
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.resizing_map = False
                        self.size_input_text = ""
                    
                    elif event.key == pygame.K_BACKSPACE:
                        self.size_input_text = self.size_input_text[:-1]
                    
                    else:
                        self.size_input_text += event.unicode
                
                # Skip standard game inputs while typing!
                continue 

            #Editor Mode Specific Raw Pygame Events
            if event.type == pygame.KEYDOWN:
                if self.edit_mode and not self.resizing_map:
                    if event.key == pygame.K_r: # 'R' to Resize
                        self.resizing_map = True
                        self.size_input_text = ""
                        # Reset movement inputs so the player stops
                        self.input_manager.keyboard._pressed = {a: False for a in self.input_manager.keyboard._pressed}

    def update(self):
        if self.resizing_map:
            return 
        
        self.input_manager.update()
        
        # Editor Toggling...
        if self.input_manager.is_action_just_pressed(GameAction.EDITOR_TOGGLE):
            self.edit_mode = not self.edit_mode

        # GAME LOGIC
        if not self.edit_mode:
            
            # Handle GAME OVER State
            if self.game_state == "GAME_OVER":
                # Wait for the player to press 'R' to restart
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    # Reset the player and reload the current map
                    self.player.hp = self.player.max_hp
                    self.player.is_dead = False
                    self.apply_map_spawns()
                    self.game_state = "PLAYING"
                return # Stop updating physics and AI

            # Handle ROOM CLEARED State
            if self.game_state == "ROOM_CLEARED":
                # Wait for the player to press 'ENTER' to go to the next map
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    # For now, we just reload the same map. 
                    # Later, this will load "room_2.json" or "hub.json"
                    self.apply_map_spawns()
                    self.game_state = "PLAYING"
                return # Stop updating physics and AI

            # --- NORMAL PLAYING STATE ---
            self.player.handle_input(self.input_manager)
            walls = self.tilemap.get_wall_hitboxes()

            self._move_and_collide(self.player, walls, self.dt)
            for enemy in self.enemies:
                self._move_and_collide(enemy, walls, self.dt)

            if self.player.attack_hitbox:
                for enemy in self.enemies:
                    if enemy.id not in self.player.hit_targets and Collision.check_collision(self.player.attack_hitbox, enemy.hitbox):
                        enemy.take_damage(15) 
                        self.player.hit_targets.add(enemy.id) 

            # Enemies hitting the player
            if not self.player.is_dead:
                for enemy in self.enemies:
                    if Collision.check_collision(enemy.hitbox, self.player.hitbox):
                        self.player.take_damage(10) 
                        
            # Check for Player Death -> Trigger Game Over
            if self.player.is_dead:
                self.game_state = "GAME_OVER"

            self.player.update(self.dt)
            for enemy in self.enemies:
                enemy.update(self.dt)
                
            self.enemies = [e for e in self.enemies if not e.is_dead]

            # Check for Victory -> Trigger Room Cleared
            # If the list of enemies is empty, the room is conquered!
            if len(self.enemies) == 0 and self.game_state == "PLAYING":
                self.game_state = "ROOM_CLEARED"

            self.camera.update()

        # EDITOR LOGIC
        if self.edit_mode:
            # 1. FREE CAMERA MOVEMENT
            cam_speed = 600 * self.dt
            if self.input_manager.is_action_pressed(GameAction.MOVE_UP):
                self.camera.offset_y -= cam_speed
            if self.input_manager.is_action_pressed(GameAction.MOVE_DOWN):
                self.camera.offset_y += cam_speed
            if self.input_manager.is_action_pressed(GameAction.MOVE_LEFT):
                self.camera.offset_x -= cam_speed
            if self.input_manager.is_action_pressed(GameAction.MOVE_RIGHT):
                self.camera.offset_x += cam_speed

            # 2. Existing Editor Controls
            if self.input_manager.is_action_just_pressed(GameAction.EDITOR_SAVE):
                self.tilemap.save()
                print("Level Saved!")
            if self.input_manager.is_action_just_pressed(GameAction.EDITOR_LOAD):
                self.tilemap.load()
                self.apply_map_spawns() 
                print("Level Loaded!")
            
            # Allow cycling through our new brush types using the 'N' key
            if self.input_manager.is_action_just_pressed(GameAction.EDITOR_NEXT_TILE):
                self.current_tile_idx = (self.current_tile_idx + 1) % len(self.available_tiles)
                self.current_tile = self.available_tiles[self.current_tile_idx]
            
            # Tile Placement via Mouse
            mx, my = self.input_manager.get_mouse_position()
            world_x = mx + self.camera.offset_x
            world_y = my + self.camera.offset_y
            row, col = self.tilemap.world_to_tile(world_x, world_y)

            buttons = pygame.mouse.get_pressed()
            if buttons[0]: # Left click
                self.tilemap.set_tile(row, col, self.current_tile)
            if buttons[2]: # Right click
                self.tilemap.set_tile(row, col, 0)

    def apply_map_spawns(self):
        """Finds entity spawn tiles and places the entities there."""
        player_spawns = self.tilemap.get_entity_spawns(99)
        if player_spawns:
            self.player.x, self.player.y = player_spawns[0]
            self.player.hitbox.update_center(self.player.x, self.player.y)
            
        # Spawn Enemies
        self.enemies.clear() # Remove old enemies when a new map loads
        enemy_spawns = self.tilemap.get_entity_spawns(50)
        for ex, ey in enemy_spawns:
            # Pass the player as the target so they know who to chase
            new_enemy = Enemy(x=ex, y=ey, target=self.player)
            self.enemies.append(new_enemy)
            
    def _move_and_collide(self, entity, walls, dt):
        """Handles movement and wall sliding for ANY entity."""
        # Calculate final speed applying stats (assuming base 100% speed)
        final_speed = entity.base_speed * (1 + entity.stats.speed / 100)
        
        dx = entity.movement_input[0] * final_speed * dt
        dy = entity.movement_input[1] * final_speed * dt

        # ---- X AXIS ----
        entity.x += dx
        entity.hitbox.update_center(entity.x, entity.y)
        for wall in walls:
            if Collision.check_collision(entity.hitbox, wall):
                response = Collision.get_response(entity.hitbox, wall)
                if response:
                    entity.x += response.x
                    entity.hitbox.update_center(entity.x, entity.y)

        # ---- Y AXIS ----
        entity.y += dy
        entity.hitbox.update_center(entity.x, entity.y)
        for wall in walls:
            if Collision.check_collision(entity.hitbox, wall):
                response = Collision.get_response(entity.hitbox, wall)
                if response:
                    entity.y += response.y
                    entity.hitbox.update_center(entity.x, entity.y)

    def draw(self):
        self.screen.fill((135, 206, 235))
        cx, cy = self.camera.offset_x, self.camera.offset_y

        self.tilemap.draw(self.screen, cx, cy, self.edit_mode)
        
        # Draw Enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, cx, cy)
            
        self.player.draw(self.screen, cx, cy)
        
        if self.edit_mode:
            for wall in self.tilemap.get_wall_hitboxes():
                self.hitbox_renderer.render(wall, (255, 0, 0), cx, cy)
            
            if not self.resizing_map:
                brush_name = self.tile_names[self.current_tile]
                mode_text = self.ui_font.render(f"EDIT MODE ON | Brush: {brush_name} | 'N' to Cycle | 'R' to Resize", True, (255, 255, 255))
                self.screen.blit(mode_text, (10, 10))

        if self.player.attack_hitbox:
            self.hitbox_renderer.render(
                self.player.attack_hitbox, (255, 255, 0), cx, cy
            )

        if self.resizing_map:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            prompt_surf = self.ui_font.render("Enter new map size (Width Height) e.g., '30 20':", True, (255, 255, 255))
            prompt_rect = prompt_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(prompt_surf, prompt_rect)

            input_surf = self.ui_font.render(self.size_input_text + "_", True, (255, 255, 0))
            input_rect = input_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(input_surf, input_rect)

            cancel_surf = self.ui_font.render("Press ENTER to confirm, ESC to cancel", True, (150, 150, 150))
            cancel_rect = cancel_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(cancel_surf, cancel_rect)
        
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((50, 0, 0, 180)) # Dark red tint
            self.screen.blit(overlay, (0, 0))
            
            death_text = self.ui_font.render("YOU DIED", True, (255, 50, 50))
            restart_text = self.ui_font.render("Press 'R' to Restart", True, (255, 255, 255))
            self.screen.blit(death_text, death_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 20)))
            self.screen.blit(restart_text, restart_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 + 20)))

        elif self.game_state == "ROOM_CLEARED":
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 50, 0, 180)) # Dark green tint
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.ui_font.render("ROOM CLEARED!", True, (50, 255, 50))
            next_text = self.ui_font.render("Press 'ENTER' to continue", True, (255, 255, 255))
            self.screen.blit(win_text, win_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 20)))
            self.screen.blit(next_text, next_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 + 20)))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
        pygame.quit()