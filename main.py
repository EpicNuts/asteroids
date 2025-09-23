"""Asteroids Game - Main Entry Point."""

import pygame
import sys
from src.game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_LIVES, MASTER_VOLUME, SHOW_LOADING_SCREEN,
    SOUND_PATH_SHOOT, SOUND_PATH_EXPLOSION, SOUND_PATH_THRUST, SOUND_PATH_COLLISION,
    SOUND_VOLUME_SHOOT, SOUND_VOLUME_EXPLOSION, SOUND_VOLUME_THRUST, SOUND_VOLUME_COLLISION
)
from src.game.states import GameState, reset_game, draw_lives, draw_game_over
from src.entities.player import Player
from src.entities.asteroid import Asteroid
from src.entities.asteroidfield import AsteroidField
from src.entities.shot import Shot
from src.utils.sound import get_sound_manager
from src.utils.background import BackgroundManager
from src.utils.loading import LoadingScreen


def main():
    """Main game function."""
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # Initialize pygame
    pygame.init()
    
    # Create the game window
    GAMESCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    
    # Initialize sound system
    sound_manager = get_sound_manager()
    sound_manager.set_master_volume(MASTER_VOLUME)
    
    # Initialize background system (starts generation in background)
    background_manager = BackgroundManager()
    background_manager.initialize()
    
    # Show loading screen if enabled
    if SHOW_LOADING_SCREEN:
        loading_screen = LoadingScreen(GAMESCREEN, background_manager)
        clock = pygame.time.Clock()
        
        print("Showing loading screen...")
        
        # Loading screen loop
        while True:
            # Handle events during loading
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Loading skipped by user")
                        background_manager.use_fallback()
                        break
            
            # Update and draw loading screen
            loading_complete = loading_screen.update_and_draw()
            
            pygame.display.flip()
            clock.tick(60)
            
            if loading_complete:
                break
        
        print("Loading complete, starting game!")
    
    # Load sound effects
    sound_manager.load_sound("shoot", SOUND_PATH_SHOOT, SOUND_VOLUME_SHOOT)
    sound_manager.load_sound("explosion", SOUND_PATH_EXPLOSION, SOUND_VOLUME_EXPLOSION)
    sound_manager.load_sound("thrust", SOUND_PATH_THRUST, SOUND_VOLUME_THRUST)
    sound_manager.load_sound("collision", SOUND_PATH_COLLISION, SOUND_VOLUME_COLLISION)
    
    # Initialize font
    pygame.font.init()
    font = pygame.font.Font(None, 74)  # Large font for game over
    ui_font = pygame.font.Font(None, 36)  # Smaller font for UI

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Set the sprite groups to the class containers
    Player.containers = updatable, drawable
    Shot.containers = updatable, drawable, shots
    Asteroid.containers = updatable, drawable, asteroids
    AsteroidField.containers = updatable

    # Create the game objects
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    clock = pygame.time.Clock()
    
    # Game state variables
    game_state = GameState.PLAYING
    lives = PLAYER_LIVES

    # Main game loop
    RUNGAME = True
    while RUNGAME:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNGAME = False
                elif event.key == pygame.K_SPACE and game_state == GameState.GAME_OVER:
                    # Restart the game
                    game_state = GameState.PLAYING
                    lives = PLAYER_LIVES
                    reset_game(player, asteroidfield, shots, asteroids)

        dt = clock.tick(60) / 1000  # Amount of seconds between each loop
        
        # Render background
        background_manager.render(GAMESCREEN)
        
        if game_state == GameState.PLAYING:
            # Update the game objects
            updatable.update(dt)
            
            # Check for player-asteroid collision
            for asteroid in asteroids:
                if player.is_vulnerable() and player.collision(asteroid):
                    # Play collision sound
                    from src.utils.sound import play_sound
                    play_sound("collision")
                    
                    lives -= 1
                    if lives <= 0:
                        game_state = GameState.GAME_OVER
                    else:
                        # Reset game but keep lives
                        reset_game(player, asteroidfield, shots, asteroids)
                    break
            
            # Check for shot-asteroid collision
            for shot in shots:
                for asteroid in asteroids:
                    if shot.collision(asteroid):
                        shot.kill()
                        asteroid.split()
                        break 

            # Render the sprites
            for sprite in drawable: 
                sprite.draw(GAMESCREEN)
            
            # Draw UI elements
            draw_lives(GAMESCREEN, lives, ui_font)
            
        elif game_state == GameState.GAME_OVER:
            # Draw game over screen
            draw_game_over(GAMESCREEN, font)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
