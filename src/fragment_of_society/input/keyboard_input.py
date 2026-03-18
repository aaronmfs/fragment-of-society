# NOTE: MADE by AI
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


K_w = 119
K_s = 115
K_a = 97
K_d = 100
K_ESCAPE = 27
K_e = 101
K_1 = 49
K_2 = 50
K_3 = 51
K_4 = 52
K_SPACE = 32


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
        self._keys_state: Dict[int, bool] = {}
        self._default_bindings()

    def _default_bindings(self) -> None:
        self.bind_key(K_w, "move_up", holdable=True)
        self.bind_key(K_s, "move_down", holdable=True)
        self.bind_key(K_a, "move_left", holdable=True)
        self.bind_key(K_d, "move_right", holdable=True)
        self.bind_key(K_ESCAPE, "pause", holdable=False)
        self.bind_key(K_e, "interact", holdable=False)
        self.bind_key(K_1, "slot_1", holdable=False)
        self.bind_key(K_2, "slot_2", holdable=False)
        self.bind_key(K_3, "slot_3", holdable=False)

    def bind_key(self, key: int, action: str, holdable: bool = False) -> None:
        self._bindings[action] = KeyBinding(key, action, holdable)

    def unbind_key(self, action: str) -> None:
        self._bindings.pop(action, None)

    def set_keys_state(self, keys_state) -> None:
        self._keys_state = {i: keys_state[i] for i in range(len(keys_state))}

    def update(self) -> None:
        self._actions_just_pressed.clear()
        self._actions_just_released.clear()

        for action, binding in self._bindings.items():
            is_pressed = self._keys_state.get(binding.key, False)
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

    def get_movement_vector(self) -> Tuple[float, float]:
        x = 0.0
        y = 0.0
        if self.is_held("move_up"):
            y -= 1
        if self.is_held("move_down"):
            y += 1
        if self.is_held("move_left"):
            x -= 1
        if self.is_held("move_right"):
            x += 1

        length = (x * x + y * y) ** 0.5
        if length > 0:
            x /= length
            y /= length
        return (x, y)
