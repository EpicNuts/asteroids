"""Game state management."""

import pygame
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_LIVES


class GameState:
    """Game state enumeration."""
    PLAYING = "playing"
    GAME_OVER = "game_over"


def reset_game(player, asteroidfield, shots, asteroids):
    """Reset the game state - player position and clear asteroids/shots."""
    # Reset player position and velocity
    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.velocity = pygame.Vector2(0, 0)
    player.rotation = 0
    player.make_invulnerable(2.0)  # 2 seconds of invulnerability
    
    # Clear all asteroids and shots
    for asteroid in asteroids:
        asteroid.kill()
    for shot in shots:
        shot.kill()
    
    # Reset asteroid field
    asteroidfield.__init__()


def draw_lives(screen, lives, font):
    """Draw the lives counter in the top left corner."""
    lives_text = font.render(f"Lives: {lives}", True, "white")
    screen.blit(lives_text, (20, 20))


def draw_game_over(screen, font):
    """Draw the game over screen."""
    game_over_text = font.render("GAME OVER", True, "white")
    restart_text = font.render("Press SPACE to restart", True, "white")
    
    # Center the text on screen
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
