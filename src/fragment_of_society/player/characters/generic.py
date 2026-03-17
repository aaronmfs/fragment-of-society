from fragment_of_society.player.character import Character
from fragment_of_society.components import Stats, Hitbox

class Generic(Character):
    def __init__(
            self,
            x: float,
            y: float,
            name: str = "Generic"
            ) -> None:

        # Intentional
        stats = Stats(
            max_hp=10,
            attack=10,
            defense=10,
            speed=10
        )

        # Intentional
        hitbox = Hitbox(
            50,
            50
        )

        super().__init__(name=name, stats=stats, hitbox=hitbox, x=x, y=y)
