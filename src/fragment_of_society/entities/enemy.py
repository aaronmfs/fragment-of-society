import math
import pygame

from fragment_of_society.entities.base import Entity

class Enemy(Entity):
    def __init__(self, x: float, y: float, target: Entity = None):
        super().__init__(x=x, y=y, sprite_key="enemy")
        self.name = "Slime"
        self.target = target
        self.color = (255, 50, 50)
        self.radius = 30
        self.base_speed = 180 
        self.aggro_range = 400

        # Health Stats
        self.hp = 30
        self.max_hp = 30
        self.is_dead = False

    # Damage Method
    def take_damage(self, amount: float):
        self.hp -= amount
        print(f"{self.name} took {amount} damage! HP: {self.hp}/{self.max_hp}")
        
        self.color = (255, 255, 255) 
        
        if self.hp <= 0:
            self.is_dead = True
            print(f"{self.name} has been defeated!")

    def update(self, dt: float) -> None:
        if self.color == (255, 255, 255):
            self.color = (255, 50, 50)

    def update(self, dt: float) -> None:
        # Basic AI: Chase the target if they are within range
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if 0 < dist < self.aggro_range:
                # Normalize the vector to move at a consistent speed
                self.set_movement(dx/dist, dy/dist)
                self.set_rotation(math.atan2(dy, dx))
            else:
                self.set_movement(0, 0)
        
        # Call base entity update for timers and state machine
        super().update(dt)

    def draw(self, screen, camera_offset_x: float = 0, camera_offset_y: float = 0) -> None:
        self.camera_x = camera_offset_x
        self.camera_y = camera_offset_y
        
        # Fallback circle rendering
        px = int(self.x - camera_offset_x)
        py = int(self.y - camera_offset_y)
        pygame.draw.circle(screen, self.color, (px, py), self.radius)
        
        # Draw hitbox
        hb = self.hitbox
        x = int(hb.x - camera_offset_x)
        y = int(hb.y - camera_offset_y)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, int(hb.width), int(hb.height)), 1)

        # Enemy Health Bar UI
        bar_width = 40
        bar_height = 6
        hp_ratio = max(0.0, self.hp / self.max_hp)
        
        # Draw position (centered above the enemy's head)
        bar_x = int(self.x - camera_offset_x - bar_width / 2)
        bar_y = int(self.y - camera_offset_y - self.radius - 15)
        
        # Draw Red Background
        pygame.draw.rect(screen, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Draw Green Foreground
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))