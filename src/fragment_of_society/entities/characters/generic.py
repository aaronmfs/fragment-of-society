from fragment_of_society.components import Stats, SkillBuilder
from fragment_of_society.entities.base import Entity


class Generic(Entity):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        stats = Stats(
            max_hp=10,
            attack=10,
            defence=10,
            speed=10
        )

        animations = {
            "idle": "warrior_idle",
            "walk": "warrior_walk",
            "attack": "warrior_attack",
            "skill1": "warrior_skill1",
            "skill2": "warrior_skill2",
            "skill3": "warrior_skill3"
        }

        super().__init__(x, y, stats, sprite_key="warrior", animations=animations)
        self.name = "Generic"

        self.basic_attack = SkillBuilder.damage(
            name="Basic Attack",
            base_damage=10.0,
            cost=0,
            cooldown=1,
            scaling_stat="attack",
            attack_width=200,
            attack_height=225,
            attack_offset_x=100
        )

        self.first_skill = SkillBuilder.damage(
            name="AoE Blast",
            base_damage=20.0,
            cost=0,
            cooldown=5,
            scaling_stat="attack",
            aoe_radius=150,
            alive_duration=5.0,
            tick_interval=0.5,
            tick_value=5.0,
            follows_owner=True,
        )

        self.second_skill = SkillBuilder.damage(
            name="AoE Blast",
            base_damage=20.0,
            cost=0,
            cooldown=5,
            scaling_stat="attack",
            aoe_radius=150,
            alive_duration=5.0,
            tick_interval=0.5,
            tick_value=5.0,
        )

        self.third_skill = SkillBuilder.damage(
            name="AoE Blast",
            base_damage=20.0,
            cost=0,
            cooldown=5,
            scaling_stat="attack",
            aoe_radius=150,
            alive_duration=5.0,
            tick_interval=0.5,
            tick_value=5.0,
        )
