from fragment_of_society.player.character import Character

class PlayerController:
    def __init__(self, character: Character) -> None:
        self.character = character

    def update(self, events: list, dt: float, keyboard, mouse) -> None:
        keyboard.update()
        mouse.update(events)

        final_speed = 650 * ( 1 + self.character.stats.speed / 100 )

        move_vec = keyboard.get_movement_vector()

        if move_vec.length_squared() > 0:
            self.character.pos += move_vec * final_speed * dt
