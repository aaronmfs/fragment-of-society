from __future__ import annotations

import uuid
from typing import Optional, Dict
from enum import Enum, auto

from fragment_of_society.components import Stats, Hitbox


class EntityType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    NPC = auto()
    OBJECT = auto()


class Entity:
    def __init__(
            self,
            x: float,
            y: float,
            stats: Optional[Stats] = None,
            entity_type: Optional[EntityType] = None,
            sprite_key: str = "player",
            animations: Optional[Dict[str, str]] = None,
    ) -> None:
        if stats is None:
            stats = Stats()

        self.x = x
        self.y = y
        self.rotation = 0.0

        self.name: str = "Unnamed"
        self.target_x: float = x
        self.target_y: float = y

        self.id = uuid.uuid4()
        self.stats = stats

        self.entity_type = entity_type
        self.sprite_key = sprite_key
        self.animations = animations or {"idle": "player_idle", "walk": "player_walk", "attack": "player_attack"}

        self._hitbox_width = 35
        self._hitbox_height = 35
        self._hitbox = Hitbox(self.x, self.y, self._hitbox_width, self._hitbox_height)

        self._movement_input: tuple[float, float] = (0.0, 0.0)
        self.base_speed: float = 650

        self.basic_attack = None
        self.first_skill = None
        self.second_skill = None
        self.third_skill = None

        self.attack_hitbox = None
        self.attack_hitbox_timer = 0.0

    @property
    def hitbox(self):
        self._hitbox.update_center(self.x, self.y)
        return self._hitbox

    def set_movement(self, x: float, y: float):
        self._movement_input = (x, y)

    def set_rotation(self, rotation: float):
        self.rotation = float(rotation)

    def apply_movements(self, dt: float):
        final_speed = 650 * ( 1 + self.stats.speed / 100 )
        self.x += self._movement_input[0] * final_speed * dt
        self.y += self._movement_input[1] * final_speed * dt

        if self.attack_hitbox_timer > 0:
            self.attack_hitbox_timer -= dt
            if self.attack_hitbox_timer <= 0:
                self.attack_hitbox = None

    def update(self, dt: float) -> None:
        self.apply_movements(dt)

