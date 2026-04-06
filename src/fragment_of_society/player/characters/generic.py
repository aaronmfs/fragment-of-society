from fragment_of_society.components import Stats, SkillBuilder
from fragment_of_society.player import Character

class Generic(Character):
    def __init__(self, x: float = 0, y: float = 0) -> None:

        stats = Stats(
            max_hp=10,
            attack=10,
            defence=10,
            speed=10
        )

        super().__init__(x, y, stats)
        self.name = "Generic"

        self.basic_attack = SkillBuilder.damage(
            name="Basic Attack",
            base_damage=10.0,
            cost=0,
            cooldown=2.0,
            scaling_stat="attack",
            attack_width=200,
            attack_height=225,
            attack_offset_x=100
        )

        self.first_skill = SkillBuilder.damage(
            name="AoE Blast",
            base_damage=20.0,
            cost=0,
            cooldown=2,
            scaling_stat="attack",
            aoe_radius=150,
        )
