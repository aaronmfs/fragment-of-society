import pygame
from fragment_of_society.entities.character import Character

class PlayerController:
    def __init__(self, character: Character) -> None:
        self.character = character

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        final_speed = self.character.speed * ( 1 + self.character.stats.speed / 100 )

        move_vec = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]:
            move_vec.y -= 1
        if keys[pygame.K_s]:
            move_vec.y += 1
        if keys[pygame.K_a]:
            move_vec.x -= 1
        if keys[pygame.K_d]:
            move_vec.x += 1

        if move_vec.length_squared() > 0:
            move_vec.normalize_ip()

        self.character.pos += move_vec * final_speed * dt
