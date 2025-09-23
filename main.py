import pygame
import sys
from constants import * 
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    # initialize pygame
    pygame.init()

    # create the game window
    GAMESCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # set the sprite groups to the class containers
    Player.containers = updatable, drawable
    Shot.containers = updatable, drawable, shots
    
    Asteroid.containers = updatable, drawable, asteroids
    AsteroidField.containers = updatable

    # create the game objects
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    clock = pygame.time.Clock()

    # main game loop
    RUNGAME = True
    while RUNGAME:
        # end loop when window closed or escape key pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNGAME = False

        dt = clock.tick(60) / 1000  # Amount of seconds between each loop.
        
        # clear the screen
        GAMESCREEN.fill('black')

        # update the player
        updatable.update(dt)
        
        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game Over!")
                sys.exit(0)
        
        for shot in shots:
            for asteroid in asteroids:
                if shot.collision(asteroid):
                    shot.kill()
                    asteroid.split()
                    break 

        # render the player
        for sprite in drawable: 
            sprite.draw(GAMESCREEN)

        # 'flip' the display ?
        pygame.display.flip()

        # Cap the framerate at 60fps and get the delta time.


if __name__ == "__main__":
    main()
