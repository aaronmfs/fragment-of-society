import pygame
from fragment_of_society.core import config
from fragment_of_society.inputs import GameAction

class LevelEditor:
    def __init__(self, game_instance):
        self.game = game_instance # We keep a reference to the main game to access the camera, tilemap, etc.
        self.ui_font = pygame.font.SysFont(None, 36)
        
        # Toolbar Settings
        self.toolbar_height = 80 
        self.button_size = 50
        self.button_spacing = 20
        self.show_grid = True
        self.fill_mode = False
        
        self.typing_label = False
        self.label_input_text = ""
        self.label_target_pos = (0, 0)
        
        # Brush Inventory (Added 70 for the Tutorial Buff!)
        self.available_tiles = [1, 0, 99, 50, 2, 98, 70]
        self.tile_names = {
            1: "Wall", 0: "Eraser", 99: "Player Spawn", 
            50: "Enemy Spawn", 2: "Forcefield", 98: "Level End", 70: "Buff Item"
        }
        self.current_tile_idx = 0
        self.current_tile = self.available_tiles[self.current_tile_idx]
        
        # Resizing State
        self.resizing_map = False
        self.size_input_text = ""

    def handle_events(self, event):
        """Intercepts events when Edit Mode is active."""
        if self.resizing_map:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        clean_str = self.size_input_text.replace('x', ' ').replace(',', ' ')
                        w, h = map(int, clean_str.split())
                        self.game.tilemap.resize(w, h)
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
            return True # Consume event
        
        if self.typing_label:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.label_input_text.strip():
                        # Save the label to the tilemap!
                        self.game.tilemap.labels.append({
                            "text": self.label_input_text,
                            "x": self.label_target_pos[0],
                            "y": self.label_target_pos[1]
                        })
                        print(f"Added label: '{self.label_input_text}'")
                    self.typing_label = False
                    self.label_input_text = ""
                elif event.key == pygame.K_ESCAPE:
                    self.typing_label = False
                    self.label_input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.label_input_text = self.label_input_text[:-1]
                else:
                    self.label_input_text += event.unicode
            return True

        if event.type == pygame.MOUSEWHEEL:
            current_zoom = getattr(self.game.camera, 'zoom', 1.0)
            if event.y > 0: 
                self.game.camera.zoom = min(2.0, current_zoom + 0.1)
            elif event.y < 0: 
                self.game.camera.zoom = max(0.3, current_zoom - 0.1)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                self.resizing_map = True
                self.size_input_text = ""
                self.game.input_manager.keyboard._pressed = {a: False for a in self.game.input_manager.keyboard._pressed}
            elif event.key == pygame.K_g: 
                self.show_grid = not self.show_grid

    def update(self, dt):
        """Handles editor mouse inputs and camera panning."""
        if self.resizing_map:
            return

        # 1. FREE CAMERA MOVEMENT
        cam_speed = 600 * dt
        if self.game.input_manager.is_action_pressed(GameAction.MOVE_UP): self.game.camera.offset_y -= cam_speed
        if self.game.input_manager.is_action_pressed(GameAction.MOVE_DOWN): self.game.camera.offset_y += cam_speed
        if self.game.input_manager.is_action_pressed(GameAction.MOVE_LEFT): self.game.camera.offset_x -= cam_speed
        if self.game.input_manager.is_action_pressed(GameAction.MOVE_RIGHT): self.game.camera.offset_x += cam_speed

        # 2. SAVE / LOAD
        if self.game.input_manager.is_action_just_pressed(GameAction.EDITOR_SAVE):
            # Tell it specifically to save to tutorial.json (or whatever level is loaded)
            self.game.tilemap.save(self.game.current_level) 
            print(f"Level Saved to {self.game.current_level}!")
        if self.game.input_manager.is_action_just_pressed(GameAction.EDITOR_LOAD):
            self.game.tilemap.load()
            self.game.apply_map_spawns() 
            print("Level Loaded!")
        
        # 3. MOUSE INTERACTION
        mx, my = self.game.input_manager.get_mouse_position()
        buttons = pygame.mouse.get_pressed()
        is_hovering_ui = my >= (config.SCREEN_HEIGHT - self.toolbar_height)

        if is_hovering_ui:
            if buttons[0]: 
                start_x = 20
                for idx, tile_id in enumerate(self.available_tiles):
                    btn_x = start_x + (idx * (self.button_size + self.button_spacing))
                    btn_y = config.SCREEN_HEIGHT - self.toolbar_height + (self.toolbar_height - self.button_size) // 2
                    
                    if btn_x <= mx <= btn_x + self.button_size and btn_y <= my <= btn_y + self.button_size:
                        self.current_tile_idx = idx
                        self.current_tile = tile_id
                        
                fill_btn_rect = pygame.Rect(config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - self.toolbar_height + 15, 150, 50)
                if fill_btn_rect.collidepoint(mx, my):
                    self.fill_mode = not self.fill_mode
                    pygame.time.wait(150) 
        else:
            zoom = getattr(self.game.camera, 'zoom', 1.0)
            world_x = (mx / zoom) + self.game.camera.offset_x
            world_y = (my / zoom) + self.game.camera.offset_y
            row, col = self.game.tilemap.world_to_tile(world_x, world_y)

            # Quick-Pick Pipette Tool
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LALT] and 0 <= row < self.game.tilemap.height and 0 <= col < self.game.tilemap.width:
                for l in [2, 1, 0]:
                    t = self.game.tilemap.layers[l][row][col]
                    if t != 0:
                        self.current_tile = t
                        break

            if buttons[0] and not keys[pygame.K_LALT]: 
                if self.fill_mode:
                    self.game.tilemap.flood_fill(row, col, self.current_tile)
                else:
                    self.game.tilemap.set_tile(row, col, self.current_tile)
            if buttons[2]: 
                self.game.tilemap.set_tile(row, col, 0)

    def draw_world_overlays(self, render_surf, cx, cy, view_w, view_h):
        """Draws the grid, hitboxes, and ghost brush onto the virtual surface."""
        if self.show_grid:
            tile_size = self.game.tilemap.tile_size
            start_x = - (cx % tile_size)
            start_y = - (cy % tile_size)

            for x in range(int(start_x), view_w, tile_size):
                pygame.draw.line(render_surf, (60, 60, 70), (x, 0), (x, view_h))
            for y in range(int(start_y), view_h, tile_size):
                pygame.draw.line(render_surf, (60, 60, 70), (0, y), (view_w, y))

        for wall in self.game.tilemap.get_wall_hitboxes():
            pygame.draw.rect(render_surf, (255, 0, 0), (wall.x - cx, wall.y - cy, wall.width, wall.height), 2)
        
        if not self.resizing_map:
            mx, my = self.game.input_manager.get_mouse_position()
            if my < config.SCREEN_HEIGHT - self.toolbar_height:
                zoom = getattr(self.game.camera, 'zoom', 1.0)
                world_x = (mx / zoom) + cx
                world_y = (my / zoom) + cy
                row, col = self.game.tilemap.world_to_tile(world_x, world_y)

                view_x = col * self.game.tilemap.tile_size - cx
                view_y = row * self.game.tilemap.tile_size - cy

                ghost_surf = pygame.Surface((self.game.tilemap.tile_size, self.game.tilemap.tile_size), pygame.SRCALPHA)
                self.game.tile_renderer.render(ghost_surf, self.current_tile, 0, 0)
                ghost_surf.set_alpha(128)
                
                render_surf.blit(ghost_surf, (view_x, view_y))
                
                # Tutorial Forcefield Indicator
                box_color = (0, 255, 255) if self.current_tile == 2 else (255, 255, 255)
                pygame.draw.rect(render_surf, box_color, (view_x, view_y, self.game.tilemap.tile_size, self.game.tilemap.tile_size), 2)
                
            for label_data in self.game.tilemap.labels:
                screen_x = label_data["x"] - cx
                screen_y = label_data["y"] - cy
                text_surf = self.ui_font.render(label_data["text"], True, (255, 255, 100))
                render_surf.blit(text_surf, (screen_x, screen_y))

    def draw_ui(self, screen):
        """Draws static UI elements directly to the main screen."""
        if not self.resizing_map:
            self._draw_minimap(screen)
            self._draw_toolbar(screen)
            hotkeys = "'O' Save | 'P' Load | 'R' Resize | 'G' Grid | 'ALT' Pipette | 'TAB' Play"
            hotkey_text = self.ui_font.render(hotkeys, True, (200, 200, 200))
            screen.blit(hotkey_text, (10, 10))
        elif self.typing_label:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            prompt_surf = self.ui_font.render("Enter label text:", True, (255, 255, 255))
            screen.blit(prompt_surf, prompt_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 40)))
            input_surf = self.ui_font.render(self.label_input_text + "_", True, (100, 255, 100))
            screen.blit(input_surf, input_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)))
        else:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            prompt_surf = self.ui_font.render("Enter new map size (Width Height) e.g., '30 20':", True, (255, 255, 255))
            screen.blit(prompt_surf, prompt_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 40)))
            input_surf = self.ui_font.render(self.size_input_text + "_", True, (255, 255, 0))
            screen.blit(input_surf, input_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)))

    def _draw_toolbar(self, screen):
        toolbar_rect = pygame.Rect(0, config.SCREEN_HEIGHT - self.toolbar_height, config.SCREEN_WIDTH, self.toolbar_height)
        pygame.draw.rect(screen, (40, 40, 50), toolbar_rect)
        pygame.draw.line(screen, (100, 100, 120), (0, config.SCREEN_HEIGHT - self.toolbar_height), (config.SCREEN_WIDTH, config.SCREEN_HEIGHT - self.toolbar_height), 3)

        start_x = 20
        for idx, tile_id in enumerate(self.available_tiles):
            btn_x = start_x + (idx * (self.button_size + self.button_spacing))
            btn_y = config.SCREEN_HEIGHT - self.toolbar_height + (self.toolbar_height - self.button_size) // 2
            btn_rect = pygame.Rect(btn_x, btn_y, self.button_size, self.button_size)

            is_selected = (self.current_tile == tile_id)
            bg_color = (200, 200, 50) if is_selected else (80, 80, 90)
            pygame.draw.rect(screen, bg_color, btn_rect, border_radius=5)

            icon_rect = btn_rect.inflate(-10, -10)
            if tile_id in [1, 2, 0, 70]: 
                if tile_id == 1: pygame.draw.rect(screen, (50, 50, 50), icon_rect)
                elif tile_id == 2: pygame.draw.rect(screen, (0, 255, 255), icon_rect)
                elif tile_id == 0: pygame.draw.rect(screen, (100, 200, 100), icon_rect)
                elif tile_id == 70: pygame.draw.polygon(screen, (255, 215, 0), [(icon_rect.midtop), (icon_rect.midright), (icon_rect.midbottom), (icon_rect.midleft)])
            elif tile_id == 99: pygame.draw.circle(screen, (0, 0, 255), icon_rect.center, icon_rect.width // 2)
            elif tile_id == 50: pygame.draw.circle(screen, (255, 0, 0), icon_rect.center, icon_rect.width // 2)
            elif tile_id == 98: pygame.draw.circle(screen, (255, 0, 255), icon_rect.center, icon_rect.width // 2)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=5)
            
        brush_name = self.tile_names.get(self.current_tile, "Unknown")
        tool_surf = self.ui_font.render(f"Tool: {brush_name}", True, (255, 255, 255))
        
        fill_btn_rect = pygame.Rect(config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - self.toolbar_height + 15, 150, 50)
        pygame.draw.rect(screen, (100, 200, 100) if self.fill_mode else (80, 80, 90), fill_btn_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), fill_btn_rect, 2, border_radius=5)
        
        mode_text = "Mode: FILL" if self.fill_mode else "Mode: PAINT"
        screen.blit(self.ui_font.render(mode_text, True, (255, 255, 255)), (fill_btn_rect.x + 15, fill_btn_rect.y + 15))
        screen.blit(tool_surf, (fill_btn_rect.x - tool_surf.get_width() - 30, config.SCREEN_HEIGHT - self.toolbar_height + (self.toolbar_height - tool_surf.get_height()) // 2))

    def _draw_minimap(self, screen):
        max_dim = 200.0
        px_scale_x = max_dim / max(1, self.game.tilemap.width)
        px_scale_y = max_dim / max(1, self.game.tilemap.height)
        pixel_size = max(1.0, min(8.0, min(px_scale_x, px_scale_y)))
        
        map_w = int(self.game.tilemap.width * pixel_size)
        map_h = int(self.game.tilemap.height * pixel_size)
        minimap_surf = pygame.Surface((map_w, map_h))
        minimap_surf.fill((20, 20, 20))
        
        for r in range(self.game.tilemap.height):
            for c in range(self.game.tilemap.width):
                color = None
                t2, t1, t0 = self.game.tilemap.layers[2][r][c], self.game.tilemap.layers[1][r][c], self.game.tilemap.layers[0][r][c]
                
                if t2 == 99: color = (0, 0, 255) 
                elif t2 == 50: color = (255, 0, 0) 
                elif t2 == 98: color = (255, 0, 255)
                elif t2 == 70: color = (255, 215, 0)
                elif t1 == 1: color = (100, 100, 100) 
                elif t1 == 2: color = (0, 255, 255) 
                elif t0 != 0: color = (50, 100, 50) 
                
                if color: pygame.draw.rect(minimap_surf, color, (int(c * pixel_size), int(r * pixel_size), int(pixel_size)+1, int(pixel_size)+1))
                
        zoom = getattr(self.game.camera, 'zoom', 1.0)
        rect_x = int((self.game.camera.offset_x / self.game.tilemap.tile_size) * pixel_size)
        rect_y = int((self.game.camera.offset_y / self.game.tilemap.tile_size) * pixel_size)
        rect_w = int((((config.SCREEN_WIDTH / zoom) / self.game.tilemap.tile_size) * pixel_size))
        rect_h = int((((config.SCREEN_HEIGHT / zoom) / self.game.tilemap.tile_size) * pixel_size))
        
        pygame.draw.rect(minimap_surf, (255, 0, 0), (rect_x, rect_y, rect_w, rect_h), max(1, int(pixel_size/2)))
        screen.blit(minimap_surf, (config.SCREEN_WIDTH - map_w - 20, 20))
        pygame.draw.rect(screen, (255, 255, 255), (config.SCREEN_WIDTH - map_w - 20, 20, map_w, map_h), 2)