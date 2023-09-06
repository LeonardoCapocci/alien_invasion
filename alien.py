import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single enemy alien"""
    def __init__(self, game):
        """Initialize alien attributes and set starting position"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the aliens to the right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

        