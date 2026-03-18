from fragment_of_society.player.character import Character
from fragment_of_society.components import Stats

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
            speed=30
        )

        super().__init__(name=name, stats=stats, x=x, y=y)
