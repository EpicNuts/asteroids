"""Loading screen for the asteroids game."""

import pygame
import math
import time
from typing import Optional

from ..game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LOADING_SCREEN_TIMEOUT
)


class LoadingScreen:
    """Manages the loading screen display while background generation happens."""
    
    def __init__(self, screen: pygame.Surface, background_manager):
        """
        Initialize the loading screen.
        
        Args:
            screen: The pygame surface to draw on
            background_manager: The background manager instance
        """
        self.screen = screen
        self.background_manager = background_manager
        self.start_time = time.time()
        
        # Initialize fonts
        try:
            self.title_font = pygame.font.Font(None, 160)  # Larger title
        except:
            self.title_font = pygame.font.Font(None, 140)
        
        # Animation variables
        self.pulse_time = 0.0
        
        # Colors
        self.title_color = (255, 255, 255)
        self.ship_color = (150, 150, 255)
        self.shot_color = (255, 255, 100)
        self.asteroid_color = (150, 100, 80)
        
        # Animation setup
        self.animation_start_x = 100
        self.animation_end_x = SCREEN_WIDTH - 200
        self.animation_y = SCREEN_HEIGHT - 80
        self.asteroid_x = self.animation_end_x
        self.ship_size = 15
        self.asteroid_size = 25
        
        # Animation state
        self.shot_fired = False
        self.shot_x = self.animation_start_x
        self.collision_happened = False
        self.split_animation_progress = 0.0
    
    def _draw_starfield(self) -> None:
        """Draw a simple animated starfield background."""
        num_stars = 100
        current_time = time.time() - self.start_time
        
        for i in range(num_stars):
            # Pseudo-random star positions
            x = (i * 123 + int(current_time * 10)) % SCREEN_WIDTH
            y = (i * 456 + int(current_time * 5)) % SCREEN_HEIGHT
            brightness = 100 + (i % 156)
            
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)
    
    def _draw_ship(self, x: int, y: int) -> None:
        """Draw an enhanced ship sprite facing right (matching game style)."""
        # Ship body (triangle pointing right)
        points = [
            (x + self.ship_size, y),  # Tip
            (x - self.ship_size, y - self.ship_size//2),  # Top back
            (x - self.ship_size//2, y),  # Middle back
            (x - self.ship_size, y + self.ship_size//2),  # Bottom back
        ]
        
        # Engine glow (always show for loading screen ship)
        engine_points = [
            (x - self.ship_size, y - 3),
            (x - self.ship_size - 10, y),  # Longer engine glow
            (x - self.ship_size, y + 3),
        ]
        
        # Draw engine glow first (behind ship)
        pygame.draw.polygon(self.screen, (255, 100, 50), engine_points)
        pygame.draw.polygon(self.screen, (255, 200, 100), engine_points, 2)
        
        # Draw ship body
        pygame.draw.polygon(self.screen, (150, 150, 255), points)
        pygame.draw.polygon(self.screen, (255, 255, 255), points, 2)
    
    def _draw_asteroid(self, x: int, y: int, size: int = None, offset: tuple = (0, 0)) -> None:
        """Draw an irregular asteroid sprite (matching game style)."""
        if size is None:
            size = self.asteroid_size
        
        # Draw irregular asteroid shape
        center_x, center_y = x + offset[0], y + offset[1]
        points = []
        for i in range(8):
            angle = (i / 8.0) * 2 * math.pi
            # Vary radius for irregular shape (consistent with game)
            radius_variation = 0.7 + 0.3 * math.sin(i * 1.7)
            radius = size * radius_variation
            px = center_x + math.cos(angle) * radius
            py = center_y + math.sin(angle) * radius
            points.append((px, py))
        
        # Draw filled asteroid with brownish color (matching game)
        pygame.draw.polygon(self.screen, (120, 80, 60), points)
        # Draw outline in lighter brown  
        pygame.draw.polygon(self.screen, (180, 120, 90), points, 2)
    
    def _draw_shot(self, x: int, y: int) -> None:
        """Draw an enhanced shot sprite (matching game style)."""
        # Outer glow (larger, semi-transparent)
        pygame.draw.circle(self.screen, (255, 255, 150), (int(x), int(y)), 5, 1)
        # Inner bright core
        pygame.draw.circle(self.screen, (255, 255, 200), (int(x), int(y)), 3)
        # Bright center
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 2)
    
    def _update_animation(self) -> float:
        """Update the ship/shot/asteroid animation and return progress (0.0 to 1.0)."""
        elapsed = time.time() - self.start_time
        
        # Animation should complete in 90% of loading time, leaving 10% buffer
        total_animation_time = LOADING_SCREEN_TIMEOUT * 0.9
        progress = min(1.0, elapsed / total_animation_time)
        
        # Phase 1: Shot travels to asteroid (0% to 95%)
        shot_travel_progress = min(1.0, progress / 0.95)
        
        if shot_travel_progress < 1.0:
            # Shot is traveling
            self.shot_fired = True
            distance = self.asteroid_x - self.animation_start_x - 30  # 30 = ship length
            self.shot_x = self.animation_start_x + 30 + (distance * shot_travel_progress)
            self.collision_happened = False
        else:
            # Phase 2: Asteroid splits (95% to 100%)
            if not self.collision_happened:
                self.collision_happened = True
                print("Shot hit asteroid!")
            
            # Split animation progress (0.0 to 1.0)
            split_progress = (progress - 0.95) / 0.05
            self.split_animation_progress = min(1.0, split_progress)
        
        return progress
    
    def _draw_animation(self) -> float:
        """Draw the ship shooting asteroid animation and return progress."""
        progress = self._update_animation()
        
        # Draw ship
        self._draw_ship(self.animation_start_x, self.animation_y)
        
        # Draw shot if fired
        if self.shot_fired and not self.collision_happened:
            self._draw_shot(self.shot_x, self.animation_y)
        
        # Draw asteroid(s)
        if not self.collision_happened:
            # Intact asteroid
            self._draw_asteroid(self.asteroid_x, self.animation_y)
        else:
            # Split asteroids
            split_distance = self.split_animation_progress * 40
            split_size = int(self.asteroid_size * 0.7)
            
            # Two smaller asteroids moving apart
            self._draw_asteroid(self.asteroid_x, self.animation_y, split_size, (-split_distance, -split_distance//2))
            self._draw_asteroid(self.asteroid_x, self.animation_y, split_size, (split_distance, split_distance//2))
            
            # Add some particle effects
            if self.split_animation_progress < 0.5:
                for i in range(5):
                    particle_x = self.asteroid_x + (i - 2) * 8
                    particle_y = self.animation_y + (i - 2) * 4
                    pygame.draw.circle(self.screen, (255, 200, 100), (particle_x, particle_y), 2)
        
        return progress

    def update_and_draw(self) -> bool:
        """
        Update and draw the loading screen.
        
        Returns:
            True if loading is complete, False if still loading
        """
        # Check if background generation is complete
        if self.background_manager.is_generation_complete():
            return True
        
        # Check for timeout
        elapsed = time.time() - self.start_time
        if elapsed > LOADING_SCREEN_TIMEOUT:
            print("Loading timeout reached, proceeding with fallback background")
            return True
        
        # Clear screen with deep space color
        self.screen.fill((5, 5, 15))
        
        # Draw animated starfield
        self._draw_starfield()
        
        # Calculate title position (higher up and larger)
        center_x = SCREEN_WIDTH // 2
        title_y = SCREEN_HEIGHT // 3  # Higher on screen
        
        # Draw title with pulse effect
        pulse = 1.0 + 0.1 * math.sin((time.time() - self.start_time) * 3)
        title_text = "ASTEROIDS"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        
        # Scale for pulse effect
        scaled_width = int(title_surface.get_width() * pulse)
        scaled_height = int(title_surface.get_height() * pulse)
        title_surface = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
        
        title_rect = title_surface.get_rect(center=(center_x, title_y))
        self.screen.blit(title_surface, title_rect)
        
        # Draw the ship shooting asteroid animation
        animation_progress = self._draw_animation()
        
        # Check if animation is complete (means loading should be done soon)
        if animation_progress >= 1.0:
            return True
        
        return False
