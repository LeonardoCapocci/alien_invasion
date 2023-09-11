import pygame.font

class Lives:
    """A class to report lives information."""
    def __init__(self, game):
        """Initialize livekeeping attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.lives = game.stats.ships_left

        # Font settings for lives information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial lives image.
        self.prep_lives()

    def prep_lives(self):
        """Turn the lives into a rendered image."""
        self.lives = self.stats.ships_left
        self.lives_str = (f"Lives: {self.lives}")
        self.lives_image = self.font.render(self.lives_str, True,
                self.text_color, self.settings.bg_color)
        
        # Display the lives at the top left of the screen.
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.topleft = self.screen_rect.topleft
    
    def show_lives(self):
        """Draw the lives to the screen."""
        self.screen.blit(self.lives_image, self.lives_rect)