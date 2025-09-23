"""Shot projectile entity."""

import pygame
from ..game.constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from .base import CircleShape


class Shot(CircleShape):
    """Shot projectile class."""
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, SHOT_RADIUS)
        # Shot specific stuff here

    def draw(self, screen):
        """Draw the shot as a white circle."""
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        """Update shot position and remove if off-screen."""
        self.position += self.velocity * dt
        
        # Remove shots that go off-screen (no wrapping for shots)
        if (self.position.x < -self.radius or self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()
