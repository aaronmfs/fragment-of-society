# NOTE: MADE by AI
import pygame
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Hitbox:
    width: float
    height: float
    offset_x: float = 0
    offset_y: float = 0
    
    _parent_pos: Optional[pygame.Vector2] = field(default=None, repr=False)

    def set_parent(self, pos: pygame.Vector2) -> None:
        self._parent_pos = pos

    def get_rect(self) -> Optional[pygame.Rect]:
        if self._parent_pos is None:
            return None
        return pygame.Rect(
            self._parent_pos.x + self.offset_x - self.width / 2,
            self._parent_pos.y + self.offset_y - self.height / 2,
            self.width,
            self.height
        )

    def get_center(self) -> Optional[pygame.Vector2]:
        if self._parent_pos is None:
            return None
        return pygame.Vector2(
            self._parent_pos.x + self.offset_x,
            self._parent_pos.y + self.offset_y
        )

    def move(self, dx: float, dy: float) -> None:
        if self._parent_pos:
            self._parent_pos.x += dx
            self._parent_pos.y += dy

    def collides_with(self, other: "Hitbox") -> bool:
        self_rect = self.get_rect()
        other_rect = other.get_rect()
        if self_rect and other_rect:
            return self_rect.colliderect(other_rect)
        return False

    def contains_point(self, x: float, y: float) -> bool:
        rect = self.get_rect()
        if rect:
            return rect.collidepoint(x, y)
        return False

    def draw(self, surface: pygame.Surface, color: str = "green", width: int = 1) -> None:
        rect = self.get_rect()
        if rect:
            pygame.draw.rect(surface, color, rect, width)


class HitboxGroup:
    def __init__(self) -> None:
        self.hitboxes: List[Hitbox] = []

    def add(self, hitbox: Hitbox) -> None:
        self.hitboxes.append(hitbox)

    def remove(self, hitbox: Hitbox) -> None:
        if hitbox in self.hitboxes:
            self.hitboxes.remove(hitbox)

    def clear(self) -> None:
        self.hitboxes.clear()

    def get_rects(self) -> List[Optional[pygame.Rect]]:
        return [hb.get_rect() for hb in self.hitboxes if hb.get_rect()]

    def collides_with(self, other: Hitbox) -> bool:
        for hb in self.hitboxes:
            if hb.collides_with(other):
                return True
        return False

    def collides_with_group(self, other_group: "HitboxGroup") -> bool:
        for hb_self in self.hitboxes:
            for hb_other in other_group.hitboxes:
                if hb_self.collides_with(hb_other):
                    return True
        return False

    def draw(self, surface: pygame.Surface, color: str = "green", width: int = 1) -> None:
        for hb in self.hitboxes:
            hb.draw(surface, color, width)


class AttackHitbox(Hitbox):
    def __init__(
        self,
        width: float,
        height: float,
        offset_x: float = 0,
        offset_y: float = 0,
        duration: float = 0,
        damage: int = 0,
        knockback: float = 0
    ) -> None:
        super().__init__(width, height, offset_x, offset_y)
        self.duration = duration
        self.damage = damage
        self.knockback = knockback
        self.elapsed_time: float = 0
        self._active: bool = False

    def activate(self) -> None:
        self._active = True
        self.elapsed_time = 0

    def deactivate(self) -> None:
        self._active = False

    def update(self, dt: float) -> bool:
        if not self._active:
            return False
        self.elapsed_time += dt
        if self.duration > 0 and self.elapsed_time >= self.duration:
            self.deactivate()
            return False
        return True

    def is_active(self) -> bool:
        return self._active

    def draw(self, surface: pygame.Surface, color: str = "red", width: int = 1) -> None:
        if self._active:
            super().draw(surface, color, width)
