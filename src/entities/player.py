"""Player ship entity."""

import pygame
from .shot import Shot
from .base import CircleShape
from ..game.constants import (
    PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_DRAG,
    PLAYER_MAX_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, SHOT_RADIUS
)
from ..utils.sound import play_sound


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
        """Draw the enhanced player ship with engine glow."""
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
            
            # Draw engine glow first (behind ship) if thrusting
            if is_thrusting:
                engine_points = self.engine_triangle()
                # Engine glow with orange-red color
                pygame.draw.polygon(screen, (255, 100, 50), engine_points)
                # Add a brighter inner glow
                pygame.draw.polygon(screen, (255, 200, 100), engine_points, 2)
            
            # Draw main ship body
            ship_points = self.triangle()
            # Ship body with light blue color
            pygame.draw.polygon(screen, (150, 150, 255), ship_points)
            # Ship outline in white
            pygame.draw.polygon(screen, "white", ship_points, 2)

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
