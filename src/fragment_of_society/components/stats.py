from dataclasses import dataclass

@dataclass
class Stats:
    max_hp: int
    attack: int
    defense: int
    speed: int

    def get_damageReduction(self, incoming: int) -> int:
        return max(1, incoming - self.defense)

    # def buff(self) -> int:
    #     return None

class MageStats(Stats):
    mana: int
    magic_damage: int
