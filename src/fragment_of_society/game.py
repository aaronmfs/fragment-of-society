import pygame
from fragment_of_society.entities.generic import Generic
from fragment_of_society.controllers.player_controller import PlayerController

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
        cx = self.screen.get_width() / 2
        cy = self.screen.get_height() / 2
        self.character = Generic(x=cx, y=cy)
        self.player_controller = PlayerController(self.character)
        self.events = []


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
        self.player_controller.update(dt=self.dt, events=self.events)


    # ================================================================
    # =========================== DRAWING ============================
    # ================================================================
    # All rendering happens here.
    # Clear the screen, draw objects, then update the display.
    # ================================================================
    def draw(self):
        self.screen.fill("purple")
        pygame.draw.circle(self.screen, "red", self.character.pos, 40)
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
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
