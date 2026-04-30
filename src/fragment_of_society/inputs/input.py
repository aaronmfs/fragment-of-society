"""
Input Module - Pygame input handling.
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Tuple, Callable, Optional, List, Any
from abc import ABC, abstractmethod

import pygame


class GameAction(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    ATTACK = auto()
    SKILL_1 = auto()
    SKILL_2 = auto()
    SKILL_3 = auto()
    SKILL_4 = auto()
    SKILL_5 = auto()
    INTERACT = auto()
    PAUSE = auto()
    MENU = auto()
    CONFIRM = auto()
    CANCEL = auto()
    DEBUG_TOGGLE = auto()
    EDITOR_TOGGLE = auto()
    EDITOR_SAVE = auto()
    EDITOR_LOAD = auto()
    EDITOR_NEXT_TILE = auto()

@dataclass
class InputConfig:
    key_map: Dict[int, GameAction] = field(default_factory=lambda: {
        1073741906: GameAction.MOVE_UP,
        1073741905: GameAction.MOVE_DOWN,
        1073741904: GameAction.MOVE_LEFT,
        1073741903: GameAction.MOVE_RIGHT,
        119: GameAction.MOVE_UP,
        115: GameAction.MOVE_DOWN,
        97: GameAction.MOVE_LEFT,
        100: GameAction.MOVE_RIGHT,
        49: GameAction.SKILL_1,
        50: GameAction.SKILL_2,
        51: GameAction.SKILL_3,
        52: GameAction.SKILL_4,
        53: GameAction.SKILL_5,
        101: GameAction.INTERACT,
        27: GameAction.PAUSE,
        13: GameAction.CONFIRM,
        8: GameAction.CANCEL,
        106: GameAction.DEBUG_TOGGLE,
    })
    mouse_button_map: Dict[int, GameAction] = field(default_factory=lambda: {
        1: GameAction.INTERACT,
    })


class InputSource(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def is_action_pressed(self, action: GameAction) -> bool:
        pass

    @abstractmethod
    def is_action_just_pressed(self, action: GameAction) -> bool:
        pass


class KeyboardInput(InputSource):
    def __init__(self, config: Optional[InputConfig] = None):
        self.config = config or InputConfig()
        self._pressed: Dict[GameAction, bool] = {a: False for a in GameAction}
        self._just_pressed: Dict[GameAction, bool] = {a: False for a in GameAction}

    def update(self, dt: float):
        self._just_pressed = {a: False for a in GameAction}

    def update_keys(self, keys: List[bool]):
        for key_code, action in self.config.key_map.items():
            was_pressed = self._pressed[action]
            is_pressed = bool(keys[key_code]) if key_code < len(keys) else False
            self._pressed[action] = is_pressed
            if is_pressed and not was_pressed:
                self._just_pressed[action] = True

    def is_action_pressed(self, action: GameAction) -> bool:
        return self._pressed.get(action, False)

    def is_action_just_pressed(self, action: GameAction) -> bool:
        return self._just_pressed.get(action, False)


class MouseInput(InputSource):
    def __init__(self, config: Optional[InputConfig] = None):
        self.config = config or InputConfig()
        self._position: Tuple[float, float] = (0, 0)
        self._pressed: Dict[GameAction, bool] = {a: False for a in GameAction}
        self._just_pressed: Dict[GameAction, bool] = {a: False for a in GameAction}

    def update(self, dt: float):
        self._just_pressed = {a: False for a in GameAction}

    def update_mouse(self, position: Tuple[int, int], buttons: Tuple[bool, bool, bool]) -> None:
        self._position = position
        for i, btn in enumerate(buttons):
            action = self.config.mouse_button_map.get(i + 1)
            if action:
                was_pressed = self._pressed[action]
                self._pressed[action] = btn
                if btn and not was_pressed:
                    self._just_pressed[action] = True

    def is_action_pressed(self, action: GameAction) -> bool:
        return self._pressed.get(action, False)

    def is_action_just_pressed(self, action: GameAction) -> bool:
        return self._just_pressed.get(action, False)

    def get_position(self) -> Tuple[float, float]:
        return self._position


class InputManager:
    _instance: Optional[InputManager] = None

    def __new__(cls, config: Optional[InputConfig] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[InputConfig] = None):
        if self._initialized:
            return
        self.config = config or InputConfig()
        self.keyboard = KeyboardInput(self.config)
        self.mouse = MouseInput(self.config)
        self._gamepads: List[Any] = []
        self._action_callbacks: Dict[GameAction, List[Callable]] = {}
        self._just_pressed_callbacks: Dict[GameAction, List[Callable]] = {}
        self._initialized = True

    def update(self) -> None:
        self.keyboard.update(0)
        keys = pygame.key.get_pressed()
        self.keyboard.update_keys(keys)

        self.mouse.update(0)
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        self.mouse.update_mouse(mouse_pos, mouse_buttons)

        self._dispatch_callbacks()

    def _dispatch_callbacks(self):
        for action in GameAction:
            if self.is_action_just_pressed(action):
                for callback in self._just_pressed_callbacks.get(action, []):
                    callback()
            if self.is_action_pressed(action):
                for callback in self._action_callbacks.get(action, []):
                    callback()

    def is_action_pressed(self, action: GameAction) -> bool:
        return self.keyboard.is_action_pressed(action) or self.mouse.is_action_pressed(action)

    def is_action_just_pressed(self, action: GameAction) -> bool:
        return self.keyboard.is_action_just_pressed(action) or self.mouse.is_action_just_pressed(action)

    def get_mouse_position(self) -> Tuple[float, float]:
        return self.mouse.get_position()

    def on_action(self, action: GameAction, callback: Callable):
        if action not in self._action_callbacks:
            self._action_callbacks[action] = []
        self._action_callbacks[action].append(callback)

    def on_action_just_pressed(self, action: GameAction, callback: Callable):
        if action not in self._just_pressed_callbacks:
            self._just_pressed_callbacks[action] = []
        self._just_pressed_callbacks[action].append(callback)

    def map_key(self, key_code: int, action: GameAction):
        self.config.key_map[key_code] = action
        self.keyboard.config = self.config

    def map_mouse_button(self, button: int, action: GameAction):
        self.config.mouse_button_map[button] = action
        self.mouse.config = self.config

    def reset(self):
        for action in GameAction:
            self._action_callbacks[action] = []
            self._just_pressed_callbacks[action] = []

    @classmethod
    def get_instance(cls) -> InputManager:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        cls._instance = None
