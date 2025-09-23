"""Asteroid entity."""

import pygame
import random
from .base import CircleShape
from ..game.constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    """Asteroid class."""
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Asteroid specific stuff here

    def split(self):
        """Split the asteroid into smaller pieces."""
        # Logic to split the asteroid into smaller pieces
        self.kill()  # Remove the current asteroid for now
        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Don't split if it's already the smallest size
        
        random_angle = random.uniform(20, 50)

        new_vector_1 = self.velocity.rotate(random_angle)
        new_vector_2 = self.velocity.rotate(-random_angle)

        asteroid1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        asteroid2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)

        asteroid1.velocity = new_vector_1 * 1.2
        asteroid2.velocity = new_vector_2 * 1.2

    def draw(self, screen):
        """Draw the asteroid as a white circle."""
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        """Update asteroid position and wrap around screen."""
        self.position += self.velocity * dt
        # Add screen wrapping for asteroids
        self.wrap_around_screen()
