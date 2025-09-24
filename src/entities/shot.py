"""Shot projectile entity."""

import pygame
from ..game.constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from .base import CircleShape
from ..utils.graphics_manager import graphics_manager


class Shot(CircleShape):
    """Shot projectile class."""
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, SHOT_RADIUS)
        # Shot specific stuff here

    def draw(self, screen):
        """Draw the shot using current graphics mode."""
        shot_color = graphics_manager.get_shot_color()
        mode = graphics_manager.get_current_mode()
        is_wireframe = graphics_manager.is_wireframe_only()
        
        if mode.value == 'sprites':
            # Enhanced shot with glow effect
            # Outer glow (larger, semi-transparent)
            pygame.draw.circle(screen, (255, 255, 150), self.position, self.radius + 2, 1)
            # Inner bright core
            pygame.draw.circle(screen, (255, 255, 200), self.position, self.radius)
            # Bright center
            pygame.draw.circle(screen, (255, 255, 255), self.position, max(1, self.radius - 1))
        elif is_wireframe:
            # Minimal wireframe - just outline
            pygame.draw.circle(screen, shot_color, self.position, self.radius, 2)
            # Add a small center dot for visibility
            pygame.draw.circle(screen, shot_color, self.position, 1)
        else:
            # Basic filled circle
            pygame.draw.circle(screen, shot_color, self.position, self.radius)

    def update(self, dt):
        """Update shot position and remove if off-screen."""
        self.position += self.velocity * dt
        
        # Remove shots that go off-screen (no wrapping for shots)
        if (self.position.x < -self.radius or self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()
