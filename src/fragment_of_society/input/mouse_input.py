# NOTE: MADE by AI
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass, field


BUTTON_LEFT = 1
BUTTON_RIGHT = 3
BUTTON_MIDDLE = 2
BUTTON_WHEELUP = 4
BUTTON_WHEELDOWN = 5
BUTTON_X1 = 4
BUTTON_X2 = 5

MOUSEMOTION = 0
MOUSEBUTTONDOWN = 1
MOUSEBUTTONUP = 2
MOUSEWHEEL = 3


@dataclass
class MouseButtonBinding:
    button: int
    action: str


class MouseInput:
    def __init__(self) -> None:
        self._button_bindings: Dict[str, MouseButtonBinding] = {}
        self._buttons_pressed: set = set()
        self._buttons_just_pressed: set = set()
        self._buttons_just_released: set = set()
        self._mouse_pos: Tuple[float, float] = (0, 0)
        self._mouse_delta: Tuple[float, float] = (0, 0)
        self._wheel_y: int = 0
        self._relative_mode: bool = False
        self._default_bindings()

    def _default_bindings(self) -> None:
        self.bind_button(BUTTON_LEFT, "attack")
        self.bind_button(BUTTON_RIGHT, "aim")
        self.bind_button(BUTTON_MIDDLE, "middle_click")
        self.bind_button(BUTTON_WHEELUP, "wheel_up")
        self.bind_button(BUTTON_WHEELDOWN, "wheel_down")
        self.bind_button(BUTTON_X1, "back")
        self.bind_button(BUTTON_X2, "forward")

    def bind_button(self, button: int, action: str) -> None:
        self._button_bindings[action] = MouseButtonBinding(button, action)

    def unbind_button(self, action: str) -> None:
        self._button_bindings.pop(action, None)

    def set_mouse_position(self, pos: Tuple[float, float]) -> None:
        self._mouse_pos = pos

    def set_mouse_delta(self, delta: Tuple[float, float]) -> None:
        self._mouse_delta = delta

    def update(self, event_list: Optional[list] = None) -> None:
        self._buttons_just_pressed.clear()
        self._buttons_just_released.clear()
        self._wheel_y = 0

        if event_list is None:
            return

        for event in event_list:
            if hasattr(event, 'type'):
                event_type = event.type
            else:
                continue

            if event_type == 4:
                pos = getattr(event, 'pos', (0, 0))
                rel = getattr(event, 'rel', (0, 0))
                self._mouse_pos = (pos[0], pos[1])
                self._mouse_delta = (rel[0], rel[1])
            elif event_type == 5:
                button = getattr(event, 'button', 1)
                action = self._get_action_for_button(button)
                if action and action not in self._buttons_pressed:
                    self._buttons_just_pressed.add(action)
                    self._buttons_pressed.add(action)
            elif event_type == 6:
                button = getattr(event, 'button', 1)
                action = self._get_action_for_button(button)
                if action:
                    self._buttons_pressed.discard(action)
                    self._buttons_just_released.add(action)
            elif event_type == 5:
                self._wheel_y = getattr(event, 'y', 0)

    def _get_action_for_button(self, button: int) -> Optional[str]:
        for action, binding in self._button_bindings.items():
            if binding.button == button:
                return action
        return None

    def is_held(self, action: str) -> bool:
        return action in self._buttons_pressed

    def is_pressed(self, action: str) -> bool:
        return action in self._buttons_just_pressed

    def is_released(self, action: str) -> bool:
        return action in self._buttons_just_released

    def get_position(self) -> Tuple[float, float]:
        return self._mouse_pos

    def get_delta(self) -> Tuple[float, float]:
        return self._mouse_delta

    def get_wheel_delta(self) -> int:
        return self._wheel_y

    def is_relative_mode(self) -> bool:
        return self._relative_mode
