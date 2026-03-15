from fragment_of_society.entities.character import Character
from fragment_of_society.components.stats import Stats

class Generic(Character):
    def __init__(self,
                 x,
                 y,
                 name = "Generic",
                 stats: Stats = Stats(10, 10, 10, 30)
                 ) -> None:

        super().__init__(name, stats, x, y)
