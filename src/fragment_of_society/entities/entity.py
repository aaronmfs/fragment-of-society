import uuid
import pygame
from fragment_of_society.components import Stats, Hitbox, HitboxGroup

class Entity:
    def __init__(
            self,
            x: float,
            y: float,
            stats: Stats | None = None,
            hitbox: Hitbox | None = None
            ) -> None:

        if stats is None:
            stats = Stats(
                max_hp=10,
                attack=10,
                defense=10,
                speed=10
            )

        if hitbox is None:
            hitbox = Hitbox(
                width=32,
                height=32
            )

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
        damage = self.stats.get_damageReduction(amount)
        self.hp -= damage


    def heal(self, amount: int) -> None:
        self.hp += amount


    def is_alive(self) -> bool:
        return self.hp > 0


    def get_hitbox_rect(self) -> pygame.Rect | None:
        if self.hitbox:
            return self.hitbox.get_rect()
        return None


    def __repr__(self) -> str:
        return f"Entity(id={self.id}, hp={self.hp}/{self.stats.max_hp})"
