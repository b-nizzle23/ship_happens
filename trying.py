# trying.py
import pygame
from triangle_ship import TriangleShip
from Asteroid import *
import random

# Initialize Pygame
pygame.init()

# Get full screen size
full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Set window size to 75% of full screen
WIDTH, HEIGHT = int(full_width * 0.75), int(full_height * 0.75)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangle Ship Game")

# Colors
BLACK = pygame.image.load("Sprites/Background/Background.png")
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Create ships with different health values

def show_menu():
    menu_font = pygame.font.Font(None, 50)
    instructions_font = pygame.font.Font(None, 30)

    # GAME TITLE
    display_text("Ship Happens", menu_font, GREEN, WIDTH //4, HEIGHT //4)

    # Instructions
    display_text("Press Enter to Start", instructions_font, WHITE, WIDTH // 3.5, HEIGHT // 2)
    display_text("Press ESC to Quit", instructions_font, WHITE, WIDTH // 3.5, HEIGHT // 2 + 40)

    pygame.display.flip()

def game_loop():
    # Create ships with different health values
    ship2 = TriangleShip(WIDTH * .1, HEIGHT * .1, 270, 'minigun')
    ship1 = TriangleShip(WIDTH * .9, HEIGHT * .9, 270, 'base')
    # Create asteroids
    asteroid1 = Asteroid(random.randint(0, int(WIDTH/3)), -50, 0, 5, 1, random.randint(30, 100), 100)
    asteroid2 = Asteroid(random.randint(int(WIDTH/3), int(WIDTH/3*2)), HEIGHT/2, 0, 5, 1, random.randint(30, 100), 100)
    asteroid3 = Asteroid(random.randint(int(WIDTH/3*2), WIDTH), -50, 0, 5, 1, random.randint(30, 100), 100)

    # Game loop
    running = True
    clock = pygame.time.Clock()

while running:
    screen.blit(BLACK,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            ship1.rotate(1)
        if keys[pygame.K_LEFT]:
            ship1.rotate(-1)
        if keys[pygame.K_UP]:
            ship1.move_forward(WIDTH, HEIGHT)
        if keys[pygame.K_l]:
            ship1.shoot()
        if keys[pygame.K_d]:
            ship2.rotate(1)
        if keys[pygame.K_a]:
            ship2.rotate(-1)
        if keys[pygame.K_w]:
            ship2.move_forward(WIDTH, HEIGHT)
        if keys[pygame.K_SPACE]:
            ship2.shoot()

        # move asteroids
        asteroid1.move()
        asteroid1.rotate()
        asteroid2.move()
        asteroid2.rotate()
        asteroid3.move()
        asteroid3.rotate()

        ship1.handle_ship_collision(ship2)
        ship1.update_lasers(screen, ship2)
        ship2.update_lasers(screen, ship1)

        # draw ships
        ship1.draw(screen)
        ship2.draw(screen)

        # draw asteroids
        asteroid1.draw(screen)
        asteroid2.draw(screen)
        asteroid3.draw(screen)

        if ship1.is_dead() or ship2.is_dead():
            print("Player 2 won!" if ship2.is_dead() else "Player 1 wins!")
            running = False

        pygame.display.flip()
        clock.tick(60)

def main():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        show_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    menu_running = False
                    pygame.quit()
                    quit()
    pygame.quit()


main()