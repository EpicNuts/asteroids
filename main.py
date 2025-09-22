import pygame
from constants import * 
from player import Player

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000  # Amount of seconds between each loop.

        # end loop when window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Clear the screen
        screen.fill('black')

        # update the player
        player.update(dt)
        
        # render the player
        player.draw(screen)
        
        # 'flip' the display ?
        pygame.display.flip()

        # Cap the framerate at 60fps and get the delta time.


if __name__ == "__main__":
    main()
