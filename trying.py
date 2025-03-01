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

SHIP_TYPES = ["base", "sniper", "melee", "behemoth", "assassin", "minigun"]


def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Create ships with different health values

def show_menu():
    menu_font = pygame.font.Font(None, 50)
    instructions_font = pygame.font.Font(None, 30)
    screen.blit(BLACK, (0, 0))
    display_text("Ship Happens", menu_font, GREEN, WIDTH // 2, HEIGHT // 4)
    display_text("Press Enter to Start", instructions_font, WHITE, WIDTH // 2, HEIGHT // 2)
    display_text("Press ESC to Quit", instructions_font, WHITE, WIDTH // 2, HEIGHT // 2 + 40)
    pygame.display.flip()


def show_end_menu(winner):
    font = pygame.font.Font(None, 50)
    screen.blit(BLACK, (0, 0))
    display_text(f"{winner} wins! Play again?", font, WHITE, WIDTH // 2, HEIGHT // 3)

    options = ["Play Again", "Switch Characters", "Quit"]
    rects = []
    for i, option in enumerate(options):
        text_surface = font.render(option, True, WHITE)
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
        screen.blit(text_surface, rect)
        rects.append(rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        return options[i].lower().replace(" ", "_")
        pygame.time.Clock().tick(30)


def show_ship_selection(player_num):
    screen.blit(BLACK, (0, 0))
    font = pygame.font.Font(None, 50)
    display_text(f"Player {player_num} choose your ship:", font, WHITE, WIDTH // 2, HEIGHT // 4)

    ship_rects = []
    for i, ship_type in enumerate(SHIP_TYPES):
        ship_text = font.render(ship_type, True, WHITE)
        ship_rect = ship_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + i * 50))
        screen.blit(ship_text, ship_rect)
        ship_rects.append((ship_rect, ship_type))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, ship_type in ship_rects:
                    if rect.collidepoint(mouse_pos):
                        return ship_type


def show_confirmation(player_num, ship_type):
    screen.blit(BLACK, (0, 0))
    font = pygame.font.Font(None, 50)
    display_text(f"Player {player_num} chose: {ship_type}", font, WHITE, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.delay(1000)


def game_loop(ship1_type, ship2_type):
    ship1 = TriangleShip(WIDTH * .1, HEIGHT * .1, 270, ship1_type)
    ship2 = TriangleShip(WIDTH * .9, HEIGHT * .9, 270, ship2_type)

    asteroids = [
        Asteroid(random.randint(0, WIDTH // 3), HEIGHT * .3, 0, 5, 1, random.randint(10, 35), 100),
        Asteroid(random.randint(WIDTH // 3, 2 * WIDTH // 3), HEIGHT / 2, 0, 5, 1, random.randint(20, 70), 100),
        Asteroid(random.randint(2 * WIDTH // 3, WIDTH), -50, 0, 5, 1, random.randint(10, 35), 100)
    ]

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(BLACK, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]: ship1.rotate(1)
        if keys[pygame.K_a]: ship1.rotate(-1)
        if keys[pygame.K_w]: ship1.move_forward(WIDTH, HEIGHT)
        if keys[pygame.K_SPACE]: ship1.shoot()
        if keys[pygame.K_RIGHT]: ship2.rotate(1)
        if keys[pygame.K_LEFT]: ship2.rotate(-1)
        if keys[pygame.K_UP]: ship2.move_forward(WIDTH, HEIGHT)
        if keys[pygame.K_l]: ship2.shoot()

        for asteroid in asteroids:
            asteroid.move(WIDTH, HEIGHT)
            asteroid.rotate()

        ship1.handle_ship_collision(ship2)
        for asteroid in asteroids:
            ship1.handle_ship_asteroid_collision(asteroid)
            ship2.handle_ship_asteroid_collision(asteroid)

        ship1.update_lasers(screen, ship2)
        ship2.update_lasers(screen, ship1)

        # draw ships
        ship1.draw(screen)
        ship2.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)

        if ship1.is_dead() or ship2.is_dead():
            winner = "Player 2" if ship1.is_dead() else "Player 1"
            choice = show_end_menu(winner)
            if choice == "play_again":
                game_loop(ship1_type, ship2_type)
            elif choice == "switch_characters":
                main()
            elif choice == "quit":
                pygame.quit()
                quit()
            running = False

        pygame.display.flip()
        clock.tick(60)


def main():
    while True:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ship1_type = show_ship_selection(1)
                    show_confirmation(1, ship1_type)
                    ship2_type = show_ship_selection(2)
                    show_confirmation(2, ship2_type)
                    game_loop(ship1_type, ship2_type)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


main()