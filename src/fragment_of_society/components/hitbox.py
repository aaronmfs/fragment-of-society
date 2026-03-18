class Hitbox:
    def __init__(
            self,
            width: int,
            height: int,
            offset_x: float = 0,
            offset_y: float = 0
            ) -> None:

        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x: float = 0
        self.y: float = 0

    def __repr__(self) -> str:
        return f"Hitbox(w={self.width}, h={self.height}, pos=({self.x:.1f}, {self.y:.1f}))"

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y

    def sync_with_entity(self, entity):
        self.x = entity.x + self.offset_x
        self.y = entity.y + self.offset_y

    def get_bounds(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return ((self.x, self.y), (self.x + self.width, self.y + self.height))

    def collides_with(self, other) -> bool:
        self_left = self.x
        self_right = self.x + self.width
        self_top = self.y
        self_bottom = self.y + self.height

        other_left = other.x
        other_right = other.x + other.width
        other_top = other.y
        other_bottom = other.y + other.height

        return (self_left < other_right and
                self_right > other_left and
                self_top < other_bottom and
                self_bottom > other_top)


class AttackHitbox(Hitbox):
    def __init__(
            self,
            width: int,
            height: int,
            offset_x: float,
            offset_y: float,
            owner,
            damage: int,
            duration: float
            ) -> None:

        super().__init__(width, height, offset_x, offset_y)
        self.owner = owner
        self.damage = damage
        self.duration = duration
        self.elapse_time: float = 0

    def update(self, dt: float) -> None:
        self.elapse_time += dt

    def __repr__(self) -> str:
        return f"AttackHitbox(dmg={self.damage}, time={self.elapse_time:.2f}/{self.duration})"

    def is_expired(self) -> bool:
        return self.elapse_time >= self.duration
