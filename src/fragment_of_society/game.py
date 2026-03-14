# import pygame
# from fragment_of_society.entities.player import Player
# from fragment_of_society.entities.enemy import Enemy
#
# class Game:
#     def __init__(self) -> None:
#         pygame.init()
#         self.screen = pygame.display.set_mode((1280, 720))
#         pygame.display.set_caption("Fragment of Society")
#         self.clock = pygame.time.Clock()
#         self.running = True
#         self.dt = 0.0
#
#         cx = self.screen.get_width() / 2
#         cy = self.screen.get_height() / 2
#         self.player = Player(cx, cy)
#         self.enemies: list[Enemy] = [Enemy(200, 200), Enemy(900, 400)]
#         self.entities = [self.player, *self.enemies]
#
#     def handle_events(self) -> None:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#
#     def update(self) -> None:
#         for entity in self.entities:
#             entity.update(self.dt)
#
#     def draw(self) -> None:
#         self.screen.fill("purple")
#         for entity in self.entities:
#             entity.draw(self.screen)
#         pygame.display.flip()
#
#     def run(self) -> None:
#         while self.running:
#             self.handle_events()
#             self.update()
#             self.draw()
#             self.dt = self.clock.tick(60) / 1000
#
#         pygame.quit()

# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
