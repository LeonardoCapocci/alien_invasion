import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from difficulty_button import DifficultyButton
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasian:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion - Leonardo Capocci")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.game_active = False

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")
        self.easy_button = DifficultyButton(self, "EASY")
        self.easy_button.position_button(0,0)
        self.medium_button = DifficultyButton(self, "MEDIUM")
        self.medium_button.position_button(self.medium_button.rect.width,0)
        self.hard_button = DifficultyButton(self, "HARD")
        self.hard_button.position_button(self.hard_button.rect.width*2,0)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active == True:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._check_bullet_alien_collisions()
            
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)                   
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)                 

    def _check_difficulty_buttons(self, mouse_pos):
        """Changes the difficulty when the player clicks a difficulty button."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.settings.bullets_allowed = 100
            self.settings.bullet_width = 50
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        if medium_button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if hard_button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.settings.alien_speed = 4.0


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset game stats.
            self.stats.reset_stats()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False 
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that are off-screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
    def _check_bullet_alien_collisions(self):
        """Respond to collisions between bullet and alien."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding alients until there's on room left.
        # Spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height * 0.2
        while current_y < (self.settings.screen_height - 3 * alien_height):  
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += alien_width * 2
            # Finished a row. Reset x value, increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _update_aliens(self):
        """Updates aliens' positioning"""
        self.aliens.update()
        self._check_fleet_edges()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(1)
        else:
            self.game_active = False
            # Hide the mouse cursor.
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
        
if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasian()
    ai.run_game()
