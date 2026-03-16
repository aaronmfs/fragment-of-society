# Player account - holds account data and active character
from fragment_of_society.player.character import Character
from fragment_of_society.input import KeyboardInput, MouseInput

class PlayerAccount:
    def __init__(self,
                 account_name: str,
                 coins: int,
                 active_character: Character
                 ) -> None:

        self.account_name = account_name
        self.coins = coins
        self.active_character = active_character
        self.keyboard = KeyboardInput()
        self.mouse = MouseInput()

    def update(self, events: list) -> None:
        self.keyboard.update()
        self.mouse.update(events)
