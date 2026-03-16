import uuid
import pygame
from fragment_of_society.components import Stats, Hitbox, HitboxGroup

class Entity:
    def __init__(self,
                 stats: Stats,
                 x: float,
                 y: float,
                 hitbox: Hitbox = None
                 ) -> None:

        self.id = uuid.uuid4()
        self.stats = stats
        self.pos = pygame.Vector2(x, y)
        self._hp = self.stats.max_hp
        self.hitbox = hitbox
        self.hitboxes = HitboxGroup()

        if self.hitbox:
            self.hitbox.set_parent(self.pos)
            self.hitboxes.add(self.hitbox)

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.stats.max_hp))

    def update(self, dt: float) -> None:
        pass

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def heal(self, amount: int) -> None:
        self.hp += amount

    def is_alive(self) -> bool:
        return self.hp > 0

    def get_hitbox_rect(self) -> pygame.Rect:
        if self.hitbox:
            return self.hitbox.get_rect()
        return None

    def __repr__(self) -> str:
        return f"Entity(id={self.id}, hp={self.hp}/{self.stats.max_hp})"
