from fragment_of_society.player.character import Character
from fragment_of_society.input import KeyboardInput, MouseInput

class PlayerController:
    def __init__(self, character: Character) -> None:
        self.character = character

    def handle_movement(self, keyboard: KeyboardInput, dt: float):
        final_speed = 650 * ( 1 + self.character.stats.speed / 100 )

        move_vec = keyboard.get_movement_vector()

        self.character.x += move_vec[0] * final_speed * dt
        self.character.y += move_vec[1] * final_speed * dt

    def update(self, keyboard: KeyboardInput, mouse: MouseInput, events: list, dt: float) -> None:
        keyboard.update()
        mouse.update(events)

        self.handle_movement(keyboard, dt)
