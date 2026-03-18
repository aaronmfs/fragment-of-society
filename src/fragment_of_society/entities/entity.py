import uuid
from fragment_of_society.components import Stats, Hitbox

class Entity:
    def __init__(
            self,
            x: float,
            y: float,
            stats: Stats | None = None,
            ) -> None:

        if stats is None:
            stats = Stats(
                max_hp=10,
                attack=10,
                defense=10,
                speed=10
            )

        self.x = x
        self.y = y

        self.id = uuid.uuid4()
        self.stats = stats
        self._hp = self.stats.max_hp


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
