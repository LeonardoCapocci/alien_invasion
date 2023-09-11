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
        self.alien_points = 50
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 5
        self.bullet_speed = 5
        self.alien_speed = 2.0
        self.bullet_width = 2
        self.bullets_allowed = 7

        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= self.speedup_scale