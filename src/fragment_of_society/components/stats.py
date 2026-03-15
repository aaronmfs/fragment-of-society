from dataclasses import dataclass

@dataclass
class Stats:
    max_hp: int
    attack: int
    defense: int
    speed: int

@dataclass
class MageStats(Stats):
    mana: int
    magic_damage: int
