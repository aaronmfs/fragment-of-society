import pygame
from fragment_of_society.entities.character import Character

class Controller:
    def __init__(self, character: Character) -> None:
        self.character = character

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        final_speed = self.character.speed * ( 1 + self.character.stats.speed / 100 )

        if keys[pygame.K_w]:
            self.character.pos.y -= final_speed * dt
        if keys[pygame.K_s]:
            self.character.pos.y += final_speed * dt
        if keys[pygame.K_a]:
            self.character.pos.x -= final_speed * dt
        if keys[pygame.K_d]:
            self.character.pos.x += final_speed * dt
