import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0,0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collision(self, other):
        return pygame.math.Vector2.distance_to(self.position, other.position) < self.radius + other.radius
    
    def wrap_around_screen(self):
        """Wraps the object around screen edges"""
        # Left edge
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        # Right edge  
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        
        # Top edge
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        # Bottom edge
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
    
