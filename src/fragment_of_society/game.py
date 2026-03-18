import pygame
from fragment_of_society.game_engine import GameEngine
from fragment_of_society.input import KeyboardInput, MouseInput


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Fragment of Society")
        self.clock = pygame.time.Clock()
        
        self.engine = GameEngine(1280, 720)
        self.keyboard = KeyboardInput()
        self.mouse = MouseInput()
        self.events = []
        self.dt = 0.0

    def handle_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.engine.running = False

    def update(self):
        self.keyboard.set_keys_state(pygame.key.get_pressed())
        self.mouse.set_mouse_position(pygame.mouse.get_pos())
        self.engine.update(self.keyboard, self.mouse, self.events, self.dt)

    def draw(self):
        self.screen.fill("purple")
        x, y = self.engine.player.active_character.x, self.engine.player.active_character.y
        pygame.draw.circle(self.screen, "red", (int(x), int(y)), 40)
        pygame.display.flip()

    def run(self):
        while self.engine.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
        pygame.quit()
