import pygame
from fragment_of_society.game_engine import GameEngine
from fragment_of_society.renderers import HitboxRenderer, Camera


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Fragment of Society")
        self.clock = pygame.time.Clock()
        
        self.engine = GameEngine(1280, 720)
        self.camera = Camera(1280, 720)
        self.camera.follow(self.engine.player)
        self.hitbox_renderer = HitboxRenderer(self.screen)
        self.events = []
        self.keys = []
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)
        self.dt = 0.0

    def handle_events(self):
        self.events = pygame.event.get()
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.engine.running = False

    def update(self):
        self.engine.input_manager.update(self.keys, self.mouse_pos, self.mouse_buttons)
        self.engine.update(self.dt, (self.camera.offset_x, self.camera.offset_y))
        self.camera.update()

    def draw(self):
        self.screen.fill((135, 206, 235))
        
        cx, cy = self.camera.offset_x, self.camera.offset_y
        
        x, y = self.engine.player.x, self.engine.player.y
        px, py = round(x - cx), round(y - cy)
        pygame.draw.circle(self.screen, "red", (px, py), 40)
        self.hitbox_renderer.render(self.engine.player.hitbox, (0, 255, 0), cx, cy)

        if self.engine.player.attack_hitbox:
            self.hitbox_renderer.render(self.engine.player.attack_hitbox, (255, 255, 0), cx, cy)

        pygame.display.flip()

    def run(self):
        while self.engine.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
        pygame.quit()
