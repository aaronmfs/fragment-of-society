import pygame
from typing import Dict, Callable, Optional
from dataclasses import dataclass, field


@dataclass
class KeyBinding:
    key: int
    action: str
    holdable: bool = False


class KeyboardInput:
    def __init__(self) -> None:
        self._bindings: Dict[str, KeyBinding] = {}
        self._actions_pressed: set = set()
        self._actions_just_pressed: set = set()
        self._actions_just_released: set = set()
        self._default_bindings()

    def _default_bindings(self) -> None:
        self.bind_key(pygame.K_w, "move_up", holdable=True)
        self.bind_key(pygame.K_s, "move_down", holdable=True)
        self.bind_key(pygame.K_a, "move_left", holdable=True)
        self.bind_key(pygame.K_d, "move_right", holdable=True)
        self.bind_key(pygame.K_SPACE, "jump", holdable=False)
        self.bind_key(pygame.K_ESCAPE, "pause", holdable=False)
        self.bind_key(pygame.K_e, "interact", holdable=False)
        self.bind_key(pygame.K_1, "slot_1", holdable=False)
        self.bind_key(pygame.K_2, "slot_2", holdable=False)
        self.bind_key(pygame.K_3, "slot_3", holdable=False)
        self.bind_key(pygame.K_4, "slot_4", holdable=False)
        self.bind_key(pygame.K_i, "inventory", holdable=False)
        self.bind_key(pygame.K_TAB, "map", holdable=False)

    def bind_key(self, key: int, action: str, holdable: bool = False) -> None:
        self._bindings[action] = KeyBinding(key, action, holdable)

    def unbind_key(self, action: str) -> None:
        self._bindings.pop(action, None)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        self._actions_just_pressed.clear()
        self._actions_just_released.clear()

        for action, binding in self._bindings.items():
            is_pressed = keys[binding.key]
            was_pressed = action in self._actions_pressed

            if is_pressed and not was_pressed:
                self._actions_just_pressed.add(action)
            elif not is_pressed and was_pressed:
                self._actions_just_released.add(action)

            if is_pressed:
                self._actions_pressed.add(action)
            else:
                self._actions_pressed.discard(action)

    def is_held(self, action: str) -> bool:
        return action in self._actions_pressed

    def is_pressed(self, action: str) -> bool:
        return action in self._actions_just_pressed

    def is_released(self, action: str) -> bool:
        return action in self._actions_just_released

    def get_movement_vector(self) -> pygame.math.Vector2:
        move_vec = pygame.math.Vector2(0, 0)
        if self.is_held("move_up"):
            move_vec.y -= 1
        if self.is_held("move_down"):
            move_vec.y += 1
        if self.is_held("move_left"):
            move_vec.x -= 1
        if self.is_held("move_right"):
            move_vec.x += 1

        if move_vec.length_squared() > 0:
            move_vec.normalize_ip()
        return move_vec
