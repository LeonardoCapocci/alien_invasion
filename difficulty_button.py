import pygame.font

class DifficultyButton:
    """A class to build buttons for the game."""
    def __init__(self, game, msg):
        """Initialize button attributes"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the buttons rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = self.screen_rect.midtop

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def position_button(self, x_position, y_position):
        """Positions the button and text at desired location."""
        self.rect.x, self.rect.y = x_position, y_position
        self.msg_image_rect.center = self.rect.center

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)