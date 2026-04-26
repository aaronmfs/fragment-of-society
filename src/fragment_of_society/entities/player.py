import math
from typing import Optional, TYPE_CHECKING

import pygame

from fragment_of_society.entities.base import Entity
from fragment_of_society.entities.characters import Generic
from fragment_of_society.entities.states import StateMachine
from fragment_of_society.inputs import InputManager, GameAction
from fragment_of_society.rendering import SpriteRenderer

if TYPE_CHECKING:
    from fragment_of_society.components.skills import Skill


class Player(Entity):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        generic = Generic(x, y)
        super().__init__(
            x=generic.x,
            y=generic.y,
            stats=generic.stats,
            sprite_key=generic.sprite_key,
            animations=generic.animations
        )
        self.name = generic.name
        self.basic_attack = generic.basic_attack
        self.first_skill = generic.first_skill
        self.second_skill = generic.second_skill
        self.third_skill = generic.third_skill

        self.color = (255, 0, 0)
        self.radius = 40

        self.state_machine = StateMachine(self, self.animations, "idle")
        self.sprite_renderer = SpriteRenderer()
        self._animation_frame = 0
        self._animation_timer = 0.0
        self._frame_duration = 0.1
        self.persistent_effects: list = []

    def handle_input(self, input_manager: InputManager) -> None:
        x, y = 0.0, 0.0
        if input_manager.is_action_pressed(GameAction.MOVE_UP):
            y -= 1
        if input_manager.is_action_pressed(GameAction.MOVE_DOWN):
            y += 1
        if input_manager.is_action_pressed(GameAction.MOVE_LEFT):
            x -= 1
        if input_manager.is_action_pressed(GameAction.MOVE_RIGHT):
            x += 1

        length = (x * x + y * y) ** 0.5
        if length > 0:
            x /= length
            y /= length

        self.set_movement(x, y)

        if input_manager.is_action_just_pressed(GameAction.INTERACT):
            mouse_pos = input_manager.get_mouse_position()
            self._handle_attack(mouse_pos)

        if input_manager.is_action_just_pressed(GameAction.SKILL_1):
            self._handle_skill(self.first_skill, "skill1_timer", "skill1")
        if input_manager.is_action_just_pressed(GameAction.SKILL_2):
            self._handle_skill(self.second_skill, "skill2_timer", "skill2")
        if input_manager.is_action_just_pressed(GameAction.SKILL_3):
            self._handle_skill(self.third_skill, "skill3_timer", "skill3")

    def _handle_attack(self, mouse_pos: tuple[int, int]) -> None:
        if not self.basic_attack or not self.basic_attack.can_use(self):
            return

        dx = mouse_pos[0] - (self.x - self.camera_x)
        dy = mouse_pos[1] - (self.y - self.camera_y)
        attack_rotation = math.atan2(dy, dx)

        self._execute_skill(self.basic_attack, attack_rotation, "attack")

    def _handle_skill(self, skill: Optional["Skill"], timer_attr: str, state_key: str) -> None:
        if not skill or not skill.can_use(self):
            return

        self._execute_skill(skill, state_key=state_key)

        setattr(self, timer_attr, 0.3)

    def _execute_skill(self, skill: "Skill", attack_rotation: float = None, state_key: str = "attack") -> None:
        if not skill.can_use(self):
            return

        rotation = attack_rotation if attack_rotation is not None else self.rotation

        if self.state_machine:
            self.state_machine.set_state(state_key)

        skill.use(self, [])

        if skill.has_attack_hitbox:
            self.attack_hitbox = skill.create_attack_hitbox(
                self.x,
                self.y,
                rotation
            )
            self.attack_hitbox_timer = 0.15

        if skill.has_persistent_effect:
            effect = skill.create_persistent_effect(self, self.x, self.y)
            if effect:
                self.persistent_effects.append(effect)

    def draw(self, screen, camera_offset_x: float = 0, camera_offset_y: float = 0) -> None:
        self.camera_x = camera_offset_x
        self.camera_y = camera_offset_y

        sprite_rendered = False

        if self.state_machine:
            animation_key = self.state_machine.animation_key
            frame_key = f"{animation_key}_{self._animation_frame}"
            sprite = self.sprite_renderer.get_sprite(frame_key)
            if sprite:
                self.sprite_renderer.render_frame(
                    screen,
                    frame_key,
                    self.x,
                    self.y,
                    self.rotation,
                    (camera_offset_x, camera_offset_y)
                )
                sprite_rendered = True

        if not sprite_rendered:
            px = int(self.x - camera_offset_x)
            py = int(self.y - camera_offset_y)
            pygame.draw.circle(screen, self.color, (px, py), self.radius)

        self._draw_hitbox(screen, camera_offset_x, camera_offset_y)
        self._draw_persistent_effects(screen, camera_offset_x, camera_offset_y)

    def _draw_persistent_effects(self, screen, camera_offset_x: float, camera_offset_y: float) -> None:
        for effect in self.persistent_effects:
            px = int(effect.x - effect.aoe_radius - camera_offset_x)
            py = int(effect.y - effect.aoe_radius - camera_offset_y)
            size = int(effect.aoe_radius * 2)
            pygame.draw.rect(screen, (255, 165, 0), (px, py, size, size), 2)

    def _draw_hitbox(self, screen, camera_offset_x: float, camera_offset_y: float) -> None:
        hb = self.hitbox
        x = int(hb.x - camera_offset_x)
        y = int(hb.y - camera_offset_y)
        w = int(hb.width)
        h = int(hb.height)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, w, h), 1)

    def update(self, dt: float) -> None:
        super().update(dt)

        if self.basic_attack:
            self.basic_attack.update(dt)
        if self.first_skill:
            self.first_skill.update(dt)
        if self.second_skill:
            self.second_skill.update(dt)
        if self.third_skill:
            self.third_skill.update(dt)

        self.persistent_effects = [e for e in self.persistent_effects if e.alive]
        for effect in self.persistent_effects:
            effect.update(dt, [])

        if self.state_machine:
            self.state_machine.update(dt)

            self._animation_timer += dt
            if self._animation_timer >= self._frame_duration:
                self._animation_timer = 0.0
                self._animation_frame = (self._animation_frame + 1) % 4

            if self.skill1_timer <= 0 and self.skill2_timer <= 0 and self.skill3_timer <= 0 and self.attack_hitbox_timer <= 0:
                if self.movement_input[0] != 0 or self.movement_input[1] != 0:
                    self.state_machine.set_state("walk")
                else:
                    self.state_machine.set_state("idle")

