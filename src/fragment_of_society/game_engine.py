from fragment_of_society.inputs import InputManager
from fragment_of_society.player import PlayerController
from fragment_of_society.player.characters import Generic


class GameEngine:
    def __init__(
            self,
            screen_width: int = 1280,
            screen_height: int = 720,
            world_width: int = 2560,
            world_height: int = 1440
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height

        cx, cy = world_width / 2, world_height / 2
        self.player = Generic(x=cx, y=cy)
        self.player_controller = PlayerController(self.player)
        self.input_manager = InputManager.get_instance()

        self.running = True

    @property
    def entities(self):
        return [self.player]

    def update(self, dt: float, camera_offset: tuple[float, float] = (0, 0)) -> None:
        self.player_controller.update(self.input_manager, dt, self.entities, camera_offset)
        self.player.update(dt)
