import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single enemy alien"""
    def __init__(self, game):
        """Initialize alien attributes and set starting position"""
        super().__init__()
        self.screen = game.screen

        # Load the alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

        