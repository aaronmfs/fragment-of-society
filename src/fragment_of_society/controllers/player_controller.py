from fragment_of_society.player.player_account import PlayerAccount

class PlayerController:
    def __init__(self, player: PlayerAccount) -> None:
        self.player = player
        self.character = player.active_character

    def update(self, dt: float) -> None:
        keyboard = self.player.keyboard
        # mouse = self.player.mouse

        final_speed = 650 * ( 1 + self.character.stats.speed / 100 )

        move_vec = keyboard.get_movement_vector()

        if move_vec.length_squared() > 0:
            self.character.pos += move_vec * final_speed * dt
