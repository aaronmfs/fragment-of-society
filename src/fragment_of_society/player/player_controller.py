from typing import Optional, List

from fragment_of_society.mixins import MovementMixin
from fragment_of_society.player import Character
from fragment_of_society.inputs import InputManager, GameAction
from fragment_of_society.components import Collision


class PlayerController:
    def __init__(self, character: Optional[Character] = None) -> None:
        self.character = character
        self._last_attack_hitboxes: List = []

    def handle_movements(self, input_manager: InputManager, dt: float, camera_offset: tuple[float, float] = (0, 0)):
        x, y = MovementMixin.get_movement_vector(
            up = input_manager.is_action_pressed(GameAction.MOVE_UP),
            down = input_manager.is_action_pressed(GameAction.MOVE_DOWN),
            left = input_manager.is_action_pressed(GameAction.MOVE_LEFT),
            right = input_manager.is_action_pressed(GameAction.MOVE_RIGHT),
        )

        if self.character:
            self.character.set_movement(x, y)

    def get_attack_rotation(self, input_manager: InputManager, camera_offset: tuple[float, float]) -> float:
        mouse_x, mouse_y = input_manager.get_mouse_position()
        if self.character:
            world_mouse_x = mouse_x + camera_offset[0]
            world_mouse_y = mouse_y + camera_offset[1]
            dx = world_mouse_x - self.character.x
            dy = world_mouse_y - self.character.y
            from math import atan2
            return atan2(dy, dx)
        return 0.0

    def handle_attacks(self, input_manager: InputManager, entities: List, camera_offset: tuple[float, float] = (0, 0)):
        if input_manager.is_action_just_pressed(GameAction.INTERACT):
            if self.character and self.character.basic_attack:
                attack_rotation = self.get_attack_rotation(input_manager, camera_offset)
                self._execute_skill(self.character.basic_attack, entities or [], attack_rotation)

    def _execute_skill(self, skill, entities: List, attack_rotation: float = None):
        if not skill.can_use(self.character):
            return

        targets = [e for e in entities if e != self.character]
        result = skill.use(self.character, targets)

        if not result.success:
            return

        rotation = attack_rotation if attack_rotation is not None else self.character.rotation

        if skill.has_attack_hitbox:
            attack_hitbox = skill.create_attack_hitbox(
                self.character.x,
                self.character.y,
                rotation
            )
            self.character.attack_hitbox = attack_hitbox
            self.character.attack_hitbox_timer = 0.15

    def update(self, input_manager: InputManager, dt: float, entities: Optional[List] = None, camera_offset: tuple[float, float] = (0, 0)):
        self.handle_movements(input_manager, dt, camera_offset)
        self.handle_attacks(input_manager, entities or [], camera_offset)
        
        if input_manager.is_action_just_pressed(GameAction.SKILL_1):
            if self.character and self.character.first_skill:
                attack_rotation = self.get_attack_rotation(input_manager, camera_offset)
                self._execute_skill(self.character.first_skill, entities or [], attack_rotation)

        if self.character:
            for skill in [self.character.basic_attack, self.character.first_skill]:
                if skill:
                    skill.update(dt)
