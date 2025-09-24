"""Loading screen for the asteroids game."""

import pygame
import math
import time
from typing import Optional

from ..game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from .asset_manager import asset_manager


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
        
        # Animation setup - better centered with original distance
        animation_width = 1000  # Wider animation area to restore original distance
        self.animation_start_x = (SCREEN_WIDTH - animation_width) // 2 + 50  # Start position with some margin
        self.animation_end_x = (SCREEN_WIDTH + animation_width) // 2 - 50    # End position with some margin
        self.animation_y = SCREEN_HEIGHT - 120
        self.asteroid_x = self.animation_end_x
        self.ship_size = 25  # Larger ship
        self.asteroid_size = 40  # Larger asteroid
        
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
        """Draw an enhanced ship sprite facing right (exactly matching game style)."""
        # Use the same triangle calculation as the game
        # For the loading screen, ship faces right (90° rotation from game's upward facing)
        rotation = -90  # Face right instead of up
        radius = self.ship_size
        
        # Calculate triangle points using the same method as the game
        import math
        forward = pygame.Vector2(0, 1)
        forward = forward.rotate(rotation)
        right = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
        
        position = pygame.Vector2(x, y)
        a = position + forward * radius  # Tip
        b = position - forward * radius - right  # Top back
        c = position - forward * radius + right  # Bottom back
        ship_points = [a, b, c]
        
        # Calculate engine glow triangle using the same method as the game
        right_engine = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 3
        back_point = position - forward * radius * 1.8
        left_point = position - forward * radius - right_engine * 0.3
        right_point = position - forward * radius + right_engine * 0.3
        engine_points = [back_point, left_point, right_point]
        
        # Draw engine glow first (behind ship) - always show for loading screen
        pygame.draw.polygon(self.screen, (255, 100, 50), engine_points)
        pygame.draw.polygon(self.screen, (255, 200, 100), engine_points, 2)
        
        # Draw ship body (exactly matching game colors)
        pygame.draw.polygon(self.screen, (150, 150, 255), ship_points)
        pygame.draw.polygon(self.screen, "white", ship_points, 2)
    
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
        # Larger shot to match the larger ship
        # Outer glow (larger, semi-transparent)
        pygame.draw.circle(self.screen, (255, 255, 150), (int(x), int(y)), 8, 1)
        # Inner bright core
        pygame.draw.circle(self.screen, (255, 255, 200), (int(x), int(y)), 5)
        # Bright center
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 3)
    
    def _draw_asset_progress(self) -> None:
        """Draw asset loading progress bar."""
        progress = asset_manager.get_loading_progress()
        
        if progress < 1.0:  # Only show if still loading
            # Progress bar position (bottom of screen, above message)
            bar_width = 400
            bar_height = 20
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            bar_y = SCREEN_HEIGHT - 150
            
            # Background bar
            pygame.draw.rect(self.screen, (40, 40, 40), 
                           (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (bar_x, bar_y, bar_width, bar_height), 2)
            
            # Progress fill
            fill_width = int(bar_width * progress)
            if fill_width > 0:
                pygame.draw.rect(self.screen, (100, 150, 255), 
                               (bar_x, bar_y, fill_width, bar_height))
            
            # Progress text
            try:
                progress_font = pygame.font.Font(None, 24)
                progress_text = f"Loading sprites... {int(progress * 100)}%"
                progress_surface = progress_font.render(progress_text, True, (200, 200, 200))
                progress_rect = progress_surface.get_rect(center=(SCREEN_WIDTH // 2, bar_y - 25))
                self.screen.blit(progress_surface, progress_rect)
            except:
                pass
    
    def _update_animation(self) -> float:
        """Update the ship/shot/asteroid animation and return progress (0.0 to 1.0)."""
        elapsed = time.time() - self.start_time
        
        # Fixed animation duration since no background generation
        total_animation_time = 3.0
        
        progress = min(1.0, elapsed / total_animation_time)
        
        # Phase 1: Shot travels to asteroid (0% to 95%)
        shot_travel_progress = min(1.0, progress / 0.95)
        
        if shot_travel_progress < 1.0:
            # Shot is traveling
            self.shot_fired = True
            distance = self.asteroid_x - self.animation_start_x - self.ship_size  # Use ship_size for accuracy
            self.shot_x = self.animation_start_x + self.ship_size + (distance * shot_travel_progress)
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
        # Check elapsed time
        elapsed = time.time() - self.start_time
        
        # Clear screen with Trifid Nebula background or deep space color
        loading_bg = self.background_manager.get_loading_background()
        if loading_bg:
            self.screen.blit(loading_bg, (0, 0))
        else:
            # Fallback to deep space color
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
        
        # Draw asset loading progress
        self._draw_asset_progress()
        
        # Show "Press SPACE to start" message after animation completes or 3 seconds
        # Also check if assets are loaded
        assets_ready = asset_manager.is_loading_complete()
        if (animation_progress >= 1.0 or elapsed >= 3.0) and assets_ready:
            try:
                message_font = pygame.font.Font(None, 48)
                message_text = "Press SPACE to start"
                message_surface = message_font.render(message_text, True, (255, 255, 255))
                message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                self.screen.blit(message_surface, message_rect)
            except:
                pass
        elif not assets_ready:
            # Show loading message
            try:
                message_font = pygame.font.Font(None, 48)
                message_text = "Loading assets..."
                message_surface = message_font.render(message_text, True, (200, 200, 200))
                message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                self.screen.blit(message_surface, message_rect)
            except:
                pass
        
        # Never auto-complete - wait for user input
        return False
