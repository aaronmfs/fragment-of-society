from fragment_of_society.entities.entity import Entity, Stats

class Character(Entity):
    def __init__(self,
                 name:str,
                 stats: Stats = Stats(10, 10, 10, 10,10, 0),
                 speed: float = 650,
                 x: float = 0,
                 y: float = 0
                 ) -> None:

        super().__init__(stats, x, y)
        self.name = name
        self.speed = speed
