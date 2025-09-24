"""Asteroid entity."""

import pygame
import random
import math
import os
from .base import CircleShape
from ..game.constants import ASTEROID_MIN_RADIUS
from ..utils.sound import play_sound
from ..utils.asset_manager import asset_manager
from ..utils.graphics_manager import graphics_manager


class AnimatedAsteroid(CircleShape):
    """Animated asteroid class using sprite sheets."""
    
    # Class-level sprite cache to avoid reloading images
    _sprite_cache = {}
    
    # Size definitions matching the AppGameKit code structure
    SIZE_LARGE = "large"
    SIZE_MEDIUM = "medium" 
    SIZE_SMALL = "small"
    
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
        # Get available variants from asset manager
        available_variants = asset_manager.get_available_variants(size)
        self.variant = variant or random.choice(available_variants) if available_variants else "a1"
        
        # Animation properties
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 3  # frames per second (slower rotation for more natural look)
        self.frame_timer = 0
        self.frame_duration = 1000 / self.animation_speed  # milliseconds per frame
        
        # Load animation frames
        self._load_animation_frames()
        
        # Generate static polygon points for basic mode (cached to avoid regeneration each frame)
        self._polygon_points = None
        
        # Velocity for movement
        self.velocity = pygame.Vector2(0, 0)
    
    def _load_animation_frames(self):
        """Load all animation frames for this asteroid from asset manager."""
        self.frames = asset_manager.get_asteroid_frames(self.size, self.variant)
    
    def _generate_polygon_points(self):
        """Generate irregular polygon points for basic mode rendering (cached)."""
        if self._polygon_points is None:
            num_sides = random.randint(5, 7)  # 5-7 sided polygon
            self._polygon_points = []
            
            # Create points around a circle with random radius variations
            # Store as relative offsets from center
            for i in range(num_sides):
                angle = (2 * math.pi * i) / num_sides
                # Add some randomness to the radius (70% to 100% of full radius)
                radius_variation = random.uniform(0.7, 1.0)
                point_radius = self.radius * radius_variation
                
                # Store as offset from center
                offset_x = point_radius * math.cos(angle)
                offset_y = point_radius * math.sin(angle)
                self._polygon_points.append((offset_x, offset_y))
        
        # Convert cached relative points to absolute screen coordinates
        absolute_points = []
        for offset_x, offset_y in self._polygon_points:
            x = self.position.x + offset_x
            y = self.position.y + offset_y
            absolute_points.append((x, y))
        
        return absolute_points
    
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
        """Draw the asteroid using current graphics mode."""
        if graphics_manager.should_use_sprites() and self.frames:
            self._draw_sprite(surface)
        else:
            self._draw_basic(surface)
    
    def _draw_sprite(self, surface):
        """Draw the asteroid using sprite animation."""
        if self.frames:
            frame = self.frames[self.current_frame]
            rect = frame.get_rect()
            rect.center = (int(self.position.x), int(self.position.y))
            surface.blit(frame, rect)
        else:
            # Fallback to basic drawing
            self._draw_basic(surface)
    
    def _draw_basic(self, surface):
        """Draw the asteroid using basic shapes."""
        # Get colors from graphics manager
        asteroid_color = graphics_manager.get_asteroid_color()
        outline_color = graphics_manager.get_asteroid_outline_color()
        is_wireframe = graphics_manager.is_wireframe_only()
        
        if is_wireframe:
            # Minimal mode: simple circle wireframe
            pygame.draw.circle(surface, asteroid_color, 
                            (int(self.position.x), int(self.position.y)), 
                            int(self.radius), 2)
        else:
            # Basic mode: irregular polygon shape
            polygon_points = self._generate_polygon_points()
            pygame.draw.polygon(surface, asteroid_color, polygon_points)
            pygame.draw.polygon(surface, outline_color, polygon_points, 2)
    
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
        """Draw the asteroid as an irregular polygon using current graphics mode."""
        points = self.get_asteroid_points()
        
        # Get colors from graphics manager
        asteroid_color = graphics_manager.get_asteroid_color()
        outline_color = graphics_manager.get_asteroid_outline_color()
        is_wireframe = graphics_manager.is_wireframe_only()
        
        if is_wireframe:
            # Wireframe only - just the outline
            pygame.draw.polygon(screen, asteroid_color, points, 2)
        else:
            # Filled polygon with outline
            pygame.draw.polygon(screen, asteroid_color, points)
            pygame.draw.polygon(screen, outline_color, points, 2)
    
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
