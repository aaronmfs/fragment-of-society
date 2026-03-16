from fragment_of_society.player.character import Character
from fragment_of_society.components import Stats, Hitbox

class Generic(Character):
    def __init__(self,
                 x,
                 y,
                 name = "Generic",
                 stats = None,
                 hitbox = None
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
                50,
                50
            )

        super().__init__(name, stats, x=x, y=y, hitbox=hitbox)
