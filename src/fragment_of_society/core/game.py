import pygame

from fragment_of_society.core import config
from fragment_of_society.entities import Player
from fragment_of_society.rendering import Camera, HitboxRenderer
from fragment_of_society.inputs import InputManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Fragment of Society")
        self.clock = pygame.time.Clock()

        cx, cy = config.WORLD_WIDTH / 2, config.WORLD_HEIGHT / 2
        self.player = Player(x=cx, y=cy)
        self.camera = Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.camera.follow(self.player)
        self.hitbox_renderer = HitboxRenderer(self.screen)
        self.input_manager = InputManager.get_instance()

        self.running = True
        self.dt = 0.0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.input_manager.update()
        self.player.handle_input(self.input_manager)
        self.player.update(self.dt)
        self.camera.update()

    def draw(self):
        self.screen.fill((135, 206, 235))

        cx, cy = self.camera.offset_x, self.camera.offset_y
        self.player.draw(self.screen, cx, cy)

        if self.player.attack_hitbox:
            self.hitbox_renderer.render(self.player.attack_hitbox, (255, 255, 0), cx, cy)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
        pygame.quit()