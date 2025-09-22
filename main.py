import pygame
from constants import * 

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:

        clock = pygame.time.Clock()
        dt = 0


        # end loop when window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill('black')
        pygame.display.flip()


        dt = clock.tick(60) / 1000  # Amount of seconds between each loop.


if __name__ == "__main__":
    main()
