"""Asteroid entity."""

import pygame
import random
import math
import os
from .base import CircleShape
from ..game.constants import ASTEROID_MIN_RADIUS
from ..utils.sound import play_sound


class AnimatedAsteroid(CircleShape):
    """Animated asteroid class using sprite sheets."""
    
    # Class-level sprite cache to avoid reloading images
    _sprite_cache = {}
    
    # Size definitions matching the AppGameKit code structure
    SIZE_LARGE = "large"
    SIZE_MEDIUM = "medium" 
    SIZE_SMALL = "small"
    
    # Asteroid variants (letters and numbers from the folder structure)
    VARIANTS = {
        "large": ["a1", "a3", "b1", "b3", "c1", "c3", "c4"],
        "medium": ["a1", "a3", "a4", "b4", "c1", "c3", "c4", "d1", "d3", "d4"],
        "small": ["a1", "a3", "a4", "b1", "b3", "b4"]
    }
    
    def __init__(self, x, y, size=SIZE_LARGE, variant=None):
        # Set radius based on size
        radius_map = {
            self.SIZE_LARGE: 40,
            self.SIZE_MEDIUM: 25, 
            self.SIZE_SMALL: 15
        }
        radius = radius_map.get(size, 40)
        
        super().__init__(x, y, radius)
        
        self.size = size
        self.variant = variant or random.choice(self.VARIANTS[size])
        
        # Animation properties
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 3  # frames per second (slower rotation for more natural look)
        self.frame_timer = 0
        self.frame_duration = 1000 / self.animation_speed  # milliseconds per frame
        
        # Load animation frames
        self._load_animation_frames()
        
        # Velocity for movement
        self.velocity = pygame.Vector2(0, 0)
    
    def _load_animation_frames(self):
        """Load all animation frames for this asteroid."""
        cache_key = f"{self.size}_{self.variant}"
        
        if cache_key in self._sprite_cache:
            self.frames = self._sprite_cache[cache_key]
            return
        
        frames = []
        base_path = os.path.join("assets", "asteroids", self.size)
        
        # Load frames 0-15 (16 frames total, matching AppGameKit)
        for i in range(16):
            filename = f"{self.variant}{i:04d}.png"
            filepath = os.path.join(base_path, filename)
            
            try:
                if os.path.exists(filepath):
                    frame = pygame.image.load(filepath).convert_alpha()
                    frames.append(frame)
                else:
                    print(f"Warning: Frame not found: {filepath}")
            except Exception as e:
                print(f"Error loading frame {filepath}: {e}")
        
        if frames:
            self.frames = frames
            self._sprite_cache[cache_key] = frames
        else:
            print(f"No frames loaded for {cache_key}, using fallback")
            # Create a simple fallback frame
            fallback = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(fallback, (150, 100, 80), (self.radius, self.radius), self.radius)
            self.frames = [fallback]
    
    def update(self, dt):
        """Update asteroid position and animation."""
        # Update position
        self.position += self.velocity * dt
        
        # Screen wrapping (matching AppGameKit bounds scaled to our screen)
        from ..game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        
        margin = 50  # Wrap margin
        if self.position.x < -margin:
            self.position.x = SCREEN_WIDTH + margin
        elif self.position.x > SCREEN_WIDTH + margin:
            self.position.x = -margin
            
        if self.position.y < -margin:
            self.position.y = SCREEN_HEIGHT + margin
        elif self.position.y > SCREEN_HEIGHT + margin:
            self.position.y = -margin
        
        # Update animation
        self.frame_timer += dt * 1000  # Convert to milliseconds
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def draw(self, surface):
        """Draw the animated asteroid."""
        if self.frames:
            frame = self.frames[self.current_frame]
            
            # Center the sprite on the asteroid position
            rect = frame.get_rect()
            rect.center = (int(self.position.x), int(self.position.y))
            surface.blit(frame, rect)
        else:
            # Fallback: draw a simple circle
            pygame.draw.circle(surface, (150, 100, 80), 
                            (int(self.position.x), int(self.position.y)), 
                            int(self.radius), 2)
    
    def set_random_velocity(self, min_speed=1.0, max_speed=3.0):
        """Set random velocity (matching AppGameKit random movement)."""
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(min_speed, max_speed)
        self.velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed) * 60  # Scale for pixels per second

    def split(self):
        """Split the asteroid into smaller pieces."""
        # Play explosion sound
        play_sound("explosion")
        
        # Return smaller asteroids based on current size
        smaller_asteroids = []
        
        if self.size == self.SIZE_LARGE:
            # Large splits into 3 medium asteroids
            for i in range(3):
                new_asteroid = AnimatedAsteroid(
                    self.position.x + random.uniform(-30, 30),
                    self.position.y + random.uniform(-30, 30),
                    self.SIZE_MEDIUM
                )
                new_asteroid.set_random_velocity(1.0, 2.0)
                smaller_asteroids.append(new_asteroid)
                
        elif self.size == self.SIZE_MEDIUM:
            # Medium splits into 2 small asteroids
            for i in range(2):
                new_asteroid = AnimatedAsteroid(
                    self.position.x + random.uniform(-20, 20),
                    self.position.y + random.uniform(-20, 20),
                    self.SIZE_SMALL
                )
                new_asteroid.set_random_velocity(1.5, 3.0)
                smaller_asteroids.append(new_asteroid)
        
        # Small asteroids don't split further
        self.kill()  # Remove the current asteroid
        return smaller_asteroids


# Keep the old Asteroid class for backward compatibility during transition
class Asteroid(AnimatedAsteroid):
    """Backward compatibility wrapper for the old Asteroid class."""
    
    def __init__(self, x, y, radius):
        # Map radius to size
        if radius >= 35:
            size = self.SIZE_LARGE
        elif radius >= 20:
            size = self.SIZE_MEDIUM
        else:
            size = self.SIZE_SMALL
            
        super().__init__(x, y, size)
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
