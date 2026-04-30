import pygame
import json

from fragment_of_society.components import Hitbox 

class TileMap:
    def __init__(self):
        self.tile_size = 64
        self.width = 6
        self.height = 5

        self.tiles = [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1],
        ]

    def draw(self, screen, cam_x, cam_y, edit_mode=False):
        for row in range(self.height):
            for col in range(self.width):
                tile = self.tiles[row][col]

                world_x = col * self.tile_size
                world_y = row * self.tile_size
                screen_x = world_x - cam_x
                screen_y = world_y - cam_y
                
                # 1. Draw the Base Environment
                if tile == 1:
                    pygame.draw.rect(screen, (50, 50, 50), (screen_x, screen_y, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(screen, (100, 200, 100), (screen_x, screen_y, self.tile_size, self.tile_size), 0)
                
                # 2. Draw Editor Overlays (Only visible when editing)
                if edit_mode:
                    pygame.draw.rect(screen, (255, 255, 0), (screen_x, screen_y, self.tile_size, self.tile_size), 1)
                    
                    center_x = screen_x + self.tile_size // 2
                    center_y = screen_y + self.tile_size // 2
                    radius = self.tile_size // 3
                    
                    if tile == 99: # Player Spawn (Blue)
                        pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), radius)
                    elif tile == 50: # Enemy Spawn (Red)
                        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), radius)

    def get_entity_spawns(self, entity_id: int):
        spawns = []
        for row in range(self.height):
            for col in range(self.width):
                if self.tiles[row][col] == entity_id:
                    # Calculate the absolute center of the tile in world coordinates
                    x = col * self.tile_size + self.tile_size // 2
                    y = row * self.tile_size + self.tile_size // 2
                    spawns.append((x, y))
        return spawns

    def get_wall_hitboxes(self):
        hitboxes = []
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col] == 1:  # wall
                    x = col * self.tile_size
                    y = row * self.tile_size
                    hitboxes.append(Hitbox(x, y, self.tile_size, self.tile_size))
        return hitboxes
    
    def get_tile(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.tiles[row][col]
        return 1  # treat out-of-bounds as wall

    def set_tile(self, row, col, value):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.tiles[row][col] = value
    
    def world_to_tile(self, x, y):
        col = int(x // self.tile_size)
        row = int(y // self.tile_size)
        return row, col
    
    def save(self, filename="map.json"):
        with open(filename, "w") as f:
            json.dump(self.tiles, f)

    def load(self, filename="map.json"):
        with open(filename, "r") as f:
            self.tiles = json.load(f)
            self.height = len(self.tiles)
            self.width = len(self.tiles[0])

    def resize(self, new_width: int, new_height: int):
        new_tiles = []
        for row in range(new_height):
            new_row = []
            for col in range(new_width):
                # Copy existing tiles if within old bounds
                if row < self.height and col < self.width:
                    new_row.append(self.tiles[row][col])
                else:
                    new_row.append(0) # Fill new space with floors
            new_tiles.append(new_row)
            
        self.width = new_width
        self.height = new_height
        self.tiles = new_tiles
    