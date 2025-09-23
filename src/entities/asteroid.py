"""Asteroid entity."""

import pygame
import random
import math
from .base import CircleShape
from ..game.constants import ASTEROID_MIN_RADIUS
from ..utils.sound import play_sound


class Asteroid(CircleShape):
    """Asteroid class."""
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Generate random asteroid shape variations for visual interest
        self.shape_seed = random.randint(0, 1000)
        self.rotation_speed = random.uniform(-2, 2)  # Random rotation
        self.current_rotation = 0
    
    def get_asteroid_points(self):
        """Generate irregular asteroid shape points."""
        points = []
        num_points = 8  # 8-sided irregular shape
        
        for i in range(num_points):
            # Base angle for this point
            angle = (i / num_points) * 2 * math.pi + self.current_rotation
            
            # Use shape_seed to make consistent random variations
            random.seed(self.shape_seed + i)
            radius_variation = 0.7 + 0.3 * random.random()  # 70% to 100% of radius
            
            # Calculate point position
            point_radius = self.radius * radius_variation
            x = self.position.x + math.cos(angle) * point_radius
            y = self.position.y + math.sin(angle) * point_radius
            points.append((x, y))
        
        # Reset random seed
        random.seed()
        return points

    def split(self):
        """Split the asteroid into smaller pieces."""
        # Play explosion sound
        play_sound("explosion")
        
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
        """Draw the asteroid as an irregular polygon."""
        points = self.get_asteroid_points()
        # Draw filled asteroid with brownish color
        pygame.draw.polygon(screen, (120, 80, 60), points)
        # Draw outline in lighter brown
        pygame.draw.polygon(screen, (180, 120, 90), points, 2)
    
    def update(self, dt):
        """Update asteroid position and rotation."""
        super().update(dt)
        # Rotate the asteroid slowly
        self.current_rotation += self.rotation_speed * dt

    def update(self, dt):
        """Update asteroid position and wrap around screen."""
        self.position += self.velocity * dt
        # Add screen wrapping for asteroids
        self.wrap_around_screen()
