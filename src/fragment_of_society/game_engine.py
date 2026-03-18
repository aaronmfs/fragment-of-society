from fragment_of_society.player.player_account import PlayerAccount
from fragment_of_society.player.characters import Generic


class GameEngine:
    def __init__(self, screen_width: int = 1280, screen_height: int = 720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        cx, cy = screen_width / 2, screen_height / 2
        self.player = PlayerAccount("Sinay", 0, Generic(cx, cy))

        self.running = True

    def update(self, keyboard, mouse, events, dt: float) -> None:
        self.player.update(keyboard, mouse, events, dt)

    def get_state(self) -> dict:
        return {
            "player_x": self.player.active_character.x,
            "player_y": self.player.active_character.y,
            "player_hp": self.player.active_character.hp,
            "player_max_hp": self.player.active_character.stats.max_hp,
        }
