from __future__ import annotations
from typing import Dict, List, Callable, Any, Optional

import pygame

from fragment_of_society.components import Hitbox, OBB


class HitboxRenderer:
    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface

    def render(
        self,
        hitbox: Hitbox,
        color: tuple[int, int, int],
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> None:
        if isinstance(hitbox, OBB):
            self._render_obb(hitbox, color, offset_x, offset_y)
        else:
            x, y, width, height = hitbox.bounds
            rect = pygame.Rect(int(x - offset_x), int(y - offset_y), int(width), int(height))
            pygame.draw.rect(self._surface, color, rect, 1)

    def _render_obb(
        self,
        obb: OBB,
        color: tuple[int, int, int],
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> None:
        corners = obb.corners
        points = [(int(c.x - offset_x), int(c.y - offset_y)) for c in corners]
        pygame.draw.polygon(self._surface, color, points, 1)

    def render_all(
        self,
        hitboxes: List[Hitbox],
        color: tuple[int, int, int],
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> None:
        for hitbox in hitboxes:
            self.render(hitbox, color, offset_x, offset_y)

    def render_with_tags(
        self,
        hitboxes: Dict[Any, Hitbox],
        color_func: Callable[[Any], tuple[int, int, int]],
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> None:
        for tag, hitbox in hitboxes.items():
            self.render(hitbox, color_func(tag), offset_x, offset_y)
