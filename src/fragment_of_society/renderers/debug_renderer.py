from __future__ import annotations
from typing import List

import pygame

from fragment_of_society.components import Hitbox, OBB, AABB


class DebugRenderer:
    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface
        self.enabled = False

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def render_hitbox(self, hitbox: Hitbox, color: tuple[int, int, int]) -> None:
        if isinstance(hitbox, OBB):
            self._render_obb(hitbox, color)
        elif isinstance(hitbox, AABB):
            x, y, width, height = hitbox.bounds
            rect = pygame.Rect(int(x), int(y), int(width), int(height))
            pygame.draw.rect(self._surface, color, rect, 1)

    def _render_obb(self, obb: OBB, color: tuple[int, int, int]) -> None:
        corners = obb.corners
        points = [(int(c.x), int(c.y)) for c in corners]
        pygame.draw.polygon(self._surface, color, points, 1)

    def render_hitboxes(self, hitboxes: List[Hitbox], color: tuple[int, int, int]) -> None:
        for hitbox in hitboxes:
            self.render_hitbox(hitbox, color)
