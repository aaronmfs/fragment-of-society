# TODO: Player class
from fragment_of_society.entities.character import Character
from fragment_of_society.input import KeyboardInput, MouseInput

class Player:
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
