import pygame
from fragment_of_society.entities.character import Character
from fragment_of_society.input import KeyboardInput, MouseInput

class PlayerController:
    def __init__(self, character: Character) -> None:
        self.character = character
        self.keyboard = KeyboardInput()
        self.mouse = MouseInput()

    def update(self, dt: float) -> None:
        final_speed = self.character.speed * ( 1 + self.character.stats.speed / 100 )

        move_vec = pygame.math.Vector2(0, 0)
        if self.keyboard.is_held("move_up"):
            move_vec.y -= 1
        if self.keyboard.is_held("move_down"):
            move_vec.y += 1
        if self.keyboard.is_held("move_left"):
            move_vec.x -= 1
        if self.keyboard.is_held("move_right"):
            move_vec.x += 1

        if move_vec.length_squared() > 0:
            move_vec.normalize_ip()

        self.character.pos += move_vec * final_speed * dt
