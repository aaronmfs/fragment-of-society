"""
Hitbox Module - AABB and OBB collision detection.
Framework-agnostic, works with any rendering library.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional, List, TYPE_CHECKING
from math import cos, sin, pi

if TYPE_CHECKING:
    pass


@dataclass
class Vector2:
    x: float
    y: float

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)

    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalized(self) -> Vector2:
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)

    def dot(self, other: Vector2) -> float:
        return self.x * other.x + self.y * other.y


class BoundingBox(ABC):
    @property
    @abstractmethod
    def position(self) -> Tuple[float, float]:
        pass

    @property
    @abstractmethod
    def bounds(self) -> Tuple[float, float, float, float]:
        pass

    @property
    @abstractmethod
    def center(self) -> Tuple[float, float]:
        pass

    @property
    @abstractmethod
    def center_vector(self) -> Vector2:
        pass

    @abstractmethod
    def contains_point(self, x: float, y: float) -> bool:
        pass

    @abstractmethod
    def update_position(self, x: float, y: float):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class AABB(BoundingBox):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        offset_x: float = 0,
        offset_y: float = 0
    ):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.offset_x = float(offset_x)
        self.offset_y = float(offset_y)

    @property
    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        return (self.x, self.y, self.width, self.height)

    @property
    def center(self) -> Tuple[float, float]:
        return (
            self.x + self.width / 2 + self.offset_x,
            self.y + self.height / 2 + self.offset_y
        )

    @property
    def center_vector(self) -> Vector2:
        cx, cy = self.center
        return Vector2(cx, cy)

    @property
    def offset(self) -> Tuple[float, float]:
        return (self.offset_x, self.offset_y)

    def update_position(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def update_center(self, cx: float, cy: float):
        self.x = float(cx - self.width / 2 - self.offset_x)
        self.y = float(cy - self.height / 2 - self.offset_y)

    def contains_point(self, x: float, y: float) -> bool:
        return (
            self.x <= x <= self.x + self.width and
            self.y <= y <= self.y + self.height
        )

    def to_dict(self) -> dict:
        return {
            "type": "AABB",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
        }

    @classmethod
    def from_dict(cls, data: dict) -> AABB:
        return cls(
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"],
            offset_x=data.get("offset_x", 0),
            offset_y=data.get("offset_y", 0),
        )


class OBB(BoundingBox):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rotation: float = 0,
        offset_x: float = 0,
        offset_y: float = 0
    ):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.rotation = float(rotation)
        self.offset_x = float(offset_x)
        self.offset_y = float(offset_y)

    @property
    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        return (self.x, self.y, self.width, self.height)

    @property
    def center(self) -> Tuple[float, float]:
        return (
            self.x + self.width / 2 + self.offset_x,
            self.y + self.height / 2 + self.offset_y
        )

    @property
    def center_vector(self) -> Vector2:
        cx, cy = self.center
        return Vector2(cx, cy)

    @property
    def offset(self) -> Tuple[float, float]:
        return (self.offset_x, self.offset_y)

    @property
    def corners(self) -> List[Vector2]:
        cx, cy = self.center
        hw = self.width / 2
        hh = self.height / 2
        cos_r = cos(self.rotation)
        sin_r = sin(self.rotation)

        local_corners = [
            Vector2(-hw, -hh),
            Vector2(hw, -hh),
            Vector2(hw, hh),
            Vector2(-hw, hh),
        ]

        return [
            Vector2(
                cx + corner.x * cos_r - corner.y * sin_r,
                cy + corner.x * sin_r + corner.y * cos_r
            )
            for corner in local_corners
        ]

    @property
    def axes(self) -> List[Vector2]:
        cos_r = cos(self.rotation)
        sin_r = sin(self.rotation)
        return [
            Vector2(cos_r, sin_r),
            Vector2(-sin_r, cos_r),
        ]

    def update_position(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def update_center(self, cx: float, cy: float):
        self.x = float(cx - self.width / 2 - self.offset_x)
        self.y = float(cy - self.height / 2 - self.offset_y)

    def update_rotation(self, rotation: float):
        self.rotation = float(rotation)

    def contains_point(self, x: float, y: float) -> bool:
        dx = x - self.center[0]
        dy = y - self.center[1]
        cos_r = cos(-self.rotation)
        sin_r = sin(-self.rotation)
        local_x = dx * cos_r - dy * sin_r
        local_y = dx * sin_r + dy * cos_r

        hw = self.width / 2
        hh = self.height / 2
        return (
            -hw <= local_x <= hw and
            -hh <= local_y <= hh
        )

    def project_onto_axis(self, axis: Vector2) -> Tuple[float, float]:
        corners = self.corners
        projections = [corner.dot(axis) for corner in corners]
        return (min(projections), max(projections))

    def to_dict(self) -> dict:
        return {
            "type": "OBB",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "rotation": self.rotation,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
        }

    @classmethod
    def from_dict(cls, data: dict) -> OBB:
        return cls(
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"],
            rotation=data.get("rotation", 0),
            offset_x=data.get("offset_x", 0),
            offset_y=data.get("offset_y", 0),
        )


class Hitbox(AABB):
    pass


class Collision:
    @staticmethod
    def check_collision(a: BoundingBox, b: BoundingBox) -> bool:
        if isinstance(a, AABB) and isinstance(b, AABB):
            return Collision._aabb_vs_aabb(a, b)
        elif isinstance(a, OBB) and isinstance(b, OBB):
            return Collision._obb_vs_obb(a, b)
        elif isinstance(a, AABB) and isinstance(b, OBB):
            return Collision._aabb_vs_obb(a, b)
        elif isinstance(a, OBB) and isinstance(b, AABB):
            return Collision._aabb_vs_obb(b, a)
        return False

    @staticmethod
    def _aabb_vs_aabb(a: AABB, b: AABB) -> bool:
        return (
            a.x < b.x + b.width and
            a.x + a.width > b.x and
            a.y < b.y + b.height and
            a.y + a.height > b.y
        )

    @staticmethod
    def _obb_vs_obb(a: OBB, b: OBB) -> bool:
        axes = a.axes + b.axes
        for axis in axes:
            proj_a = a.project_onto_axis(axis)
            proj_b = b.project_onto_axis(axis)
            if proj_a[1] < proj_b[0] or proj_b[1] < proj_a[0]:
                return False
        return True

    @staticmethod
    def _aabb_vs_obb(a: AABB, b: OBB) -> bool:
        obb_corners = b.corners
        for corner in obb_corners:
            if a.contains_point(corner.x, corner.y):
                return True

        aabb_corners = [
            Vector2(a.x, a.y),
            Vector2(a.x + a.width, a.y),
            Vector2(a.x + a.width, a.y + a.height),
            Vector2(a.x, a.y + a.height),
        ]
        for corner in aabb_corners:
            if b.contains_point(corner.x, corner.y):
                return True

        return Collision._obb_vs_obb(
            OBB(a.x, a.y, a.width, a.height),
            b
        )

    @staticmethod
    def get_penetration(a: BoundingBox, b: BoundingBox) -> Optional[Tuple[Vector2, float]]:
        if isinstance(a, AABB) and isinstance(b, AABB):
            return Collision._penetration_aabb_aabb(a, b)
        elif isinstance(a, OBB) and isinstance(b, OBB):
            return Collision._penetration_obb_obb(a, b)
        elif isinstance(a, AABB) and isinstance(b, OBB):
            result = Collision._penetration_obb_obb(
                OBB(a.x, a.y, a.width, a.height),
                b
            )
            if result:
                normal, depth = result
                return Vector2(-normal.x, -normal.y), depth
            return None
        elif isinstance(a, OBB) and isinstance(b, AABB):
            return Collision._penetration_obb_obb(
                a,
                OBB(b.x, b.y, b.width, b.height)
            )
        return None

    @staticmethod
    def _penetration_aabb_aabb(a: AABB, b: AABB) -> Optional[Tuple[Vector2, float]]:
        if not Collision._aabb_vs_aabb(a, b):
            return None

        overlap_x = min(a.x + a.width, b.x + b.width) - max(a.x, b.x)
        overlap_y = min(a.y + a.height, b.y + b.height) - max(a.y, b.y)

        if overlap_x < overlap_y:
            #FIXED: If A is left of B, push A left (-1). Otherwise push right (1).
            normal = Vector2(-1, 0) if a.center[0] < b.center[0] else Vector2(1, 0)
            return normal, overlap_x
        else:
            #FIXED: If A is above B, push A up (-1). Otherwise push down (1).
            normal = Vector2(0, -1) if a.center[1] < b.center[1] else Vector2(0, 1)
            return normal, overlap_y

    @staticmethod
    def _penetration_obb_obb(a: OBB, b: OBB) -> Optional[Tuple[Vector2, float]]:
        if not Collision._obb_vs_obb(a, b):
            return None

        axes = a.axes + b.axes
        min_overlap = float('inf')
        collision_axis: Optional[Vector2] = None

        for axis in axes:
            proj_a = a.project_onto_axis(axis)
            proj_b = b.project_onto_axis(axis)

            overlap = min(proj_a[1], proj_b[1]) - max(proj_a[0], proj_b[0])

            if overlap < min_overlap:
                min_overlap = overlap
                collision_axis = axis

        if collision_axis is None:
            return None

        if a.center[0] < b.center[0]:
            collision_axis = Vector2(-collision_axis.x, -collision_axis.y)

        return collision_axis, min_overlap

    @staticmethod
    def get_response(a: BoundingBox, b: BoundingBox) -> Optional[Vector2]:
        penetration = Collision.get_penetration(a, b)
        if penetration is None:
            return None
        normal, depth = penetration
        return Vector2(normal.x * depth, normal.y * depth)

    @staticmethod
    def get_overlap(a: BoundingBox, b: BoundingBox) -> Optional[Tuple[float, float, float, float]]:
        if not Collision.check_collision(a, b):
            return None

        if isinstance(a, AABB) and isinstance(b, AABB):
            x1 = max(a.x, b.x)
            y1 = max(a.y, b.y)
            x2 = min(a.x + a.width, b.x + b.width)
            y2 = min(a.y + a.height, b.y + b.height)
            return (x1, y1, x2 - x1, y2 - y1)
        return None

    @staticmethod
    def get_overlap_area(a: BoundingBox, b: BoundingBox) -> float:
        overlap = Collision.get_overlap(a, b)
        if overlap is None:
            return 0
        return overlap[2] * overlap[3]

    @staticmethod
    def get_distance(a: BoundingBox, b: BoundingBox) -> float:
        dx = a.center[0] - b.center[0]
        dy = a.center[1] - b.center[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    @staticmethod
    def is_within_range(a: BoundingBox, b: BoundingBox, radius: float) -> bool:
        return Collision.get_distance(a, b) <= radius


class HitboxManager:
    def __init__(self):
        self.hitboxes: List[BoundingBox] = []
        self._tags: dict[BoundingBox, set] = {}

    def add(self, hitbox: BoundingBox, tags: Optional[set] = None) -> BoundingBox:
        self.hitboxes.append(hitbox)
        if tags:
            self._tags[hitbox] = tags
        return hitbox

    def remove(self, hitbox: BoundingBox):
        if hitbox in self.hitboxes:
            self.hitboxes.remove(hitbox)
        if hitbox in self._tags:
            del self._tags[hitbox]

    def get_collisions(self, hitbox: BoundingBox) -> List[BoundingBox]:
        return [
            h for h in self.hitboxes
            if h != hitbox and Collision.check_collision(hitbox, h)
        ]

    def get_with_tag(self, tag: str) -> List[BoundingBox]:
        return [h for h, tags in self._tags.items() if tag in tags]

    def get_with_tags(self, *tags: str) -> List[BoundingBox]:
        return [h for h, htags in self._tags.items() if any(t in htags for t in tags)]

    def clear(self):
        self.hitboxes.clear()
        self._tags.clear()
