import pygame
from fragment_of_society.enemies.generic_enemy import GenericEnemy
from fragment_of_society.player.player_account import PlayerAccount
from fragment_of_society.player.characters import Generic
from fragment_of_society.renderer import DebugRenderer

pygame.init()

# ================================================================
# ===================== GAME CLASS DEFINITION ====================
# ================================================================
# This class contains the entire game structure.
# It stores the screen, clock, game objects, and the main loop.
# ================================================================
class Game:
    def __init__(self):
        # ===================== DISPLAY SETUP =====================
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Fragment of Society")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.0

        #################################################################
        # ===================== GAME OBJECT CREATION ====================
        #################################################################
        # Create all game objects here.
        # Example: player, enemies, NPCs, UI elements, etc.
        #################################################################
        self.create_entity()
        self.events = []




    def create_entity(self):
        cx = self.screen.get_width() / 2
        cy = self.screen.get_height() / 2

        self.debug_renderer = DebugRenderer(self.screen)

        self.player = PlayerAccount("Sinay", 0, active_character=Generic(cx, cy))

        self.enemy = GenericEnemy(x=cx, y=cy)

    def check_collision(self):
        if self.enemy.hitbox and self.player.active_character.hitboxes.collides_with(self.enemy.hitbox):
            print(f"Collision! with {self.enemy.name}")

    def draw_debug_hitbox(self):
        self.debug_renderer.draw_all_hitboxes([self.player.active_character, self.enemy])

    def draw_entities(self):
        pygame.draw.circle(self.screen, "red", self.player.active_character.pos, 40)
        pygame.draw.circle(self.screen, "blue", self.enemy.pos, 40)





    # ================================================================
    # ========================= EVENT HANDLER ========================
    # ================================================================
    # Responsible for reading player input and system events.
    # Example: keyboard input, mouse input, closing the window.
    # ================================================================
    def handle_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False


    # ================================================================
    # ========================== GAME UPDATE =========================
    # ================================================================
    # Update game logic here.
    # Example: movement, physics, AI, cooldown timers.
    # ================================================================
    def update(self):
        self.player.update(self.events, self.dt)
        self.check_collision()


    # ================================================================
    # =========================== DRAWING ============================
    # ================================================================
    # All rendering happens here.
    # Clear the screen, draw objects, then update the display.
    # ================================================================
    def draw(self):
        self.screen.fill("purple")
        self.draw_entities()
        self.draw_debug_hitbox()
        pygame.display.flip()


    # ================================================================
    # =========================== MAIN LOOP ==========================
    # ================================================================
    # This runs the game forever until self.running becomes False.
    # Order:
    # 1. Handle input
    # 2. Update game logic
    # 3. Draw everything
    # ================================================================
    def run(self):
        print(self.player.active_character)

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
