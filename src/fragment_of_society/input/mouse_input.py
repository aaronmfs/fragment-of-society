# NOTE: MADE by AI
import pygame
from typing import Dict, Callable, Optional, Tuple
from dataclasses import dataclass


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
        self._mouse_pos: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self._mouse_delta: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self._wheel_y: int = 0
        self._relative_mode: bool = False
        self._default_bindings()

    def _default_bindings(self) -> None:
        self.bind_button(pygame.BUTTON_LEFT, "attack")
        self.bind_button(pygame.BUTTON_RIGHT, "aim")
        self.bind_button(pygame.BUTTON_MIDDLE, "middle_click")
        self.bind_button(pygame.BUTTON_WHEELUP, "wheel_up")
        self.bind_button(pygame.BUTTON_WHEELDOWN, "wheel_down")
        self.bind_button(pygame.BUTTON_X1, "back")
        self.bind_button(pygame.BUTTON_X2, "forward")

    def bind_button(self, button: int, action: str) -> None:
        self._button_bindings[action] = MouseButtonBinding(button, action)

    def unbind_button(self, action: str) -> None:
        self._button_bindings.pop(action, None)

    def update(self, event_list: Optional[list] = None) -> None:
        self._buttons_just_pressed.clear()
        self._buttons_just_released.clear()
        self._wheel_y = 0

        self._mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

        if event_list is None:
            event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                self._mouse_delta = pygame.math.Vector2(event.rel)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = self._get_action_for_button(event.button)
                if action and action not in self._buttons_pressed:
                    self._buttons_just_pressed.add(action)
                    self._buttons_pressed.add(action)
            elif event.type == pygame.MOUSEBUTTONUP:
                action = self._get_action_for_button(event.button)
                if action:
                    self._buttons_pressed.discard(action)
                    self._buttons_just_released.add(action)
            elif event.type == pygame.MOUSEWHEEL:
                self._wheel_y = event.y

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

    def get_position(self) -> pygame.math.Vector2:
        return self._mouse_pos

    def get_delta(self) -> pygame.math.Vector2:
        return self._mouse_delta

    def get_wheel_delta(self) -> int:
        return self._wheel_y

    def set_relative_mode(self, enabled: bool) -> None:
        self._relative_mode = enabled
        pygame.mouse.set_visible(not enabled)
        pygame.event.set_grab(enabled)

    def is_relative_mode(self) -> bool:
        return self._relative_mode

    def hide_cursor(self) -> None:
        pygame.mouse.set_visible(False)

    def show_cursor(self) -> None:
        pygame.mouse.set_visible(True)

    def get_world_position(self, camera_offset: pygame.math.Vector2, zoom: float = 1.0) -> pygame.math.Vector2:
        return (self._mouse_pos / zoom) + camera_offset
