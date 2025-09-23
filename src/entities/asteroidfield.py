"""Asteroid field spawner."""

import pygame
import random
from .asteroid import Asteroid, AnimatedAsteroid
from ..game.constants import (
    ASTEROID_MAX_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_SPAWN_RATE,
    ASTEROID_KINDS, ASTEROID_MIN_RADIUS
)


class AsteroidField(pygame.sprite.Sprite):
    """Manages spawning of asteroids at screen edges."""
    
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        """Spawn a new asteroid with given parameters."""
        # Determine size based on radius
        if radius >= 35:
            size = AnimatedAsteroid.SIZE_LARGE
        elif radius >= 20:
            size = AnimatedAsteroid.SIZE_MEDIUM
        else:
            size = AnimatedAsteroid.SIZE_SMALL
            
        # Use AnimatedAsteroid instead of basic Asteroid
        asteroid = AnimatedAsteroid(position.x, position.y, size)
        asteroid.velocity = velocity

    def update(self, dt):
        """Update the spawn timer and spawn new asteroids."""
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
