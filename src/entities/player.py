"""Player ship entity."""

import pygame
import math
from .shot import Shot
from .base import CircleShape
from ..game.constants import (
    PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_DRAG,
    PLAYER_MAX_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, SHOT_RADIUS
)
from ..utils.sound import play_sound
from ..utils.graphics_manager import graphics_manager


class Player(CircleShape):
    """Player ship class."""
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.acceleration = pygame.Vector2(0, 0)
        self.invulnerable_timer = 0  # Invulnerability period after respawn

    def triangle(self):
        """Calculate the triangle points for drawing the ship body."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def chevron(self):
        """Calculate the chevron/mouse cursor points for enhanced basic mode."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        
        # Main triangle points
        tip = self.position + forward * self.radius
        left = self.position - forward * self.radius - right
        right_point = self.position - forward * self.radius + right
        
        # Add indentation points for chevron shape
        indent_depth = self.radius * 0.3  # How deep the indentation goes
        left_indent = self.position - forward * (self.radius - indent_depth) - right * 0.3
        right_indent = self.position - forward * (self.radius - indent_depth) + right * 0.3
        
        return [tip, left, left_indent, right_indent, right_point]
    
    def engine_triangle(self):
        """Calculate the engine glow triangle points."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 3
        
        # Engine glow extends backwards from the ship
        back_point = self.position - forward * self.radius * 1.8
        left_point = self.position - forward * self.radius - right * 0.3
        right_point = self.position - forward * self.radius + right * 0.3
        
        return [back_point, left_point, right_point]
    
    def draw(self, screen):
        """Draw the player ship using current graphics mode."""
        # Determine if we should draw (for blinking effect)
        should_draw = True
        if self.invulnerable_timer > 0:
            # Blink effect - only draw every few frames
            should_draw = int(self.invulnerable_timer * 10) % 2 == 0
        
        if should_draw:
            # Check if currently accelerating to show engine glow
            keys = pygame.key.get_pressed()
            is_thrusting = (keys[pygame.K_w] or keys[pygame.K_UP] or 
                          keys[pygame.K_s] or keys[pygame.K_DOWN])
            
            # Get ship sprite from graphics manager
            ship_sprite = graphics_manager.get_ship_sprite()
            
            if ship_sprite and graphics_manager.should_use_sprites():
                self._draw_sprite(screen, ship_sprite, is_thrusting)
            else:
                self._draw_basic(screen, is_thrusting)
    
    def _draw_sprite(self, screen, sprite, is_thrusting):
        """Draw the ship using a sprite image."""
        # Scale down the sprite to be more reasonable size
        # Make it a bit larger - 4x the radius for better visibility
        target_size = int(self.radius * 4)  # Increased from 3x to 4x
        scaled_sprite = pygame.transform.scale(sprite, (target_size, target_size))
        
        # Rotate the sprite to match ship rotation
        # Adjust rotation to make ship face forward correctly
        # Add 180 degrees to make the ship face forward instead of backward
        corrected_rotation = -self.rotation + 180
        rotated_sprite = pygame.transform.rotate(scaled_sprite, corrected_rotation)
        
        # Get the rect for positioning
        sprite_rect = rotated_sprite.get_rect()
        sprite_rect.center = (int(self.position.x), int(self.position.y))
        
        # Draw engine glow first if thrusting
        if is_thrusting:
            engine_points = self.engine_triangle()
            # Engine glow with orange-red color
            pygame.draw.polygon(screen, (255, 100, 50), engine_points)
            # Add a brighter inner glow
            pygame.draw.polygon(screen, (255, 200, 100), engine_points, 2)
        
        # Draw the sprite
        screen.blit(rotated_sprite, sprite_rect)
    
    def _draw_basic(self, screen, is_thrusting):
        """Draw the ship using basic shapes (original style)."""
        # Get colors from graphics manager
        ship_color = graphics_manager.get_ship_color()
        outline_color = graphics_manager.get_ship_outline_color()
        is_wireframe = graphics_manager.is_wireframe_only()
        
        # Draw engine glow first (behind ship) if thrusting
        if is_thrusting:
            engine_points = self.engine_triangle()
            if is_wireframe:
                # Wireframe engine - just outline
                pygame.draw.polygon(screen, (255, 200, 100), engine_points, 2)
            else:
                # Filled engine glow
                pygame.draw.polygon(screen, (255, 100, 50), engine_points)
                pygame.draw.polygon(screen, (255, 200, 100), engine_points, 2)
        
        # Choose shape based on graphics mode
        if is_wireframe:
            # Minimal mode: simple triangle wireframe
            ship_points = self.triangle()
            pygame.draw.polygon(screen, ship_color, ship_points, 2)
        else:
            # Basic mode: enhanced chevron shape
            ship_points = self.chevron()
            pygame.draw.polygon(screen, ship_color, ship_points)
            pygame.draw.polygon(screen, outline_color, ship_points, 2)

    def rotate(self, dt):
        """Rotate the player ship."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        """Add acceleration in the forward direction."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.acceleration += forward * PLAYER_ACCELERATION * dt
        # Play thrust sound (only occasionally to avoid spam)
        if hasattr(self, '_thrust_sound_timer'):
            self._thrust_sound_timer -= dt
        else:
            self._thrust_sound_timer = 0
        
        if self._thrust_sound_timer <= 0:
            play_sound("thrust")
            self._thrust_sound_timer = 0.5  # Play thrust sound every 0.5 seconds while accelerating

    def apply_drag(self, dt):
        """Apply drag to gradually slow down the player when not accelerating."""
        self.velocity *= PLAYER_DRAG

    def shoot(self):
        """Create a new shot projectile."""
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN
        # Play shoot sound
        play_sound("shoot")
    
    def is_vulnerable(self):
        """Returns True if the player can be hit by asteroids."""
        return self.invulnerable_timer <= 0
    
    def make_invulnerable(self, duration=2.0):
        """Make the player invulnerable for a specified duration."""
        self.invulnerable_timer = duration

    def update(self, dt):
        """Update player state, handle input, and movement."""
        if self.timer > 0:
            self.timer -= dt
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt

        # Reset acceleration each frame
        self.acceleration = pygame.Vector2(0, 0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            # rotate left
            self.rotate(-dt)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            # rotate right
            self.rotate(dt)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            # accelerate forward
            self.accelerate(dt)

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # accelerate backward
            self.accelerate(-dt)

        # Apply drag when not accelerating
        self.apply_drag(dt)

        # Update velocity based on acceleration
        self.velocity += self.acceleration

        # Cap the velocity to maximum speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

        # Update position based on velocity
        self.position += self.velocity * dt

        # Add screen wrapping for player
        self.wrap_around_screen()

        if keys[pygame.K_SPACE]:
            # shoot
            if self.timer <= 0:
                self.shoot()
