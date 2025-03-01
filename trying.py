# trying.py
import pygame
from triangle_ship import TriangleShip

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
BLACK = (0, 0, 0)

# Create ships with different health values
ship2 = TriangleShip(150,100,0,'base')
ship1 = TriangleShip(1000, 600,180,'behemoth')

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
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

    ship1.handle_ship_collision(ship2)
    ship1.update_lasers(screen, ship2)
    ship2.update_lasers(screen, ship1)
    ship1.draw(screen)
    ship2.draw(screen)

    if ship1.is_dead() or ship2.is_dead():
        print("Player 2 won!" if ship2.is_dead() else "Player 1 wins!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
