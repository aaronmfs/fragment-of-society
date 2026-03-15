import pygame
from fragment_of_society.systems.stats import Stats

class Entity:
    def __init__(self, stats: Stats, x: float, y: float) -> None:
        self.stats = stats
        self.pos = pygame.Vector2(x, y)

    def update(self, dt: float) -> None:
        pass
