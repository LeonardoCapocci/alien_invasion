class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 5
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 5
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (150, 0, 0)
        self.bullets_allowed = 7

        # Alien settings
        self.alien_speed = 2
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1