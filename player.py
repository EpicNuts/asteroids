import pygame
from shot import Shot
from circleshape import CircleShape
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.acceleration = pygame.Vector2(0, 0)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.acceleration += forward * PLAYER_ACCELERATION * dt

    def apply_drag(self, dt):
        # Apply drag to gradually slow down the player when not accelerating
        self.velocity *= PLAYER_DRAG

    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

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