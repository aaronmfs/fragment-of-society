import pygame
# from fragment_of_society.systems.stats import Stats
from dataclasses import dataclass

@dataclass
class Stats:
    hp: int
    stamina: int
    attack: int
    defense: int
    speed: int
    agility: int

class Entity:
    def __init__(self,
                 stats: Stats,
                 x: float,
                 y: float
                 ) -> None:

        self.stats = stats
        self.pos = pygame.Vector2(x, y)

    def update(self, dt: float) -> None:
        pass
