from triangle_ship import TriangleShip
from Asteroid import *
import random
from powerups import *
import time

# Initialize Pygame
pygame.init()

# Get full screen size
full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Set window size to 75% of full screen
WIDTH, HEIGHT = int(full_width * 0.9), int(full_height * 0.9)

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
    if winner == "Nobody":
        display_text(f"Its a Tie! Play again?", font, WHITE, WIDTH // 2, HEIGHT // 3)
    else:
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
    display_text(f"Player {player_num}: {ship_type}", font, WHITE, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.delay(1000)



def game_loop(ship1_type, ship2_type):
    ship1 = TriangleShip(WIDTH * .1, HEIGHT * .1, 270, ship1_type)
    ship2 = TriangleShip(WIDTH * .9, HEIGHT * .9, 270, ship2_type)
    health_boost = []
    boost_spawn_time = 4500
    last_spawn_time = pygame.time.get_ticks()
    asteroids = [
        Asteroid(random.randint(0, int(WIDTH / 3)), HEIGHT * .3, 0, 5, 1, random.randint(40, 70), 10,
                             pygame.image.load('Sprites/Asteriod/asteroid-done.png')),
        Asteroid(random.randint(int(WIDTH / 3), int(WIDTH / 3 * 2)), HEIGHT / 2, 0, 5, 1,
                         random.randint(40, 90), 10, pygame.image.load('Sprites/Asteriod/asteroid-done.png')),
        Asteroid(random.randint(int(WIDTH / 3 * 2), WIDTH), -50, 0, 5, 1, random.randint(40, 70), 10,
                         pygame.image.load('Sprites/Asteriod/asteroid-done.png'))
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
        if keys[pygame.K_w]:
            ship1.apply_thrust()
            ship1.thrust_ani()
        else:
            if not ship1.is_dead():
                ship1.not_thrust()




        # Move in facing direction

        if keys[pygame.K_SPACE]: ship1.shoot()

        # Ship 2 Controls
        if keys[pygame.K_RIGHT]: ship2.rotate(1)
        if keys[pygame.K_LEFT]: ship2.rotate(-1)
        if keys[pygame.K_UP]:
            ship2.apply_thrust()
            ship2.thrust_ani()
        else:
            if not ship2.is_dead():
                ship2.not_thrust()  # Move in facing direction
        if keys[pygame.K_l]: ship2.shoot()

        # Update ship positions
        ship1.update_position(WIDTH, HEIGHT)
        ship2.update_position(WIDTH, HEIGHT)

        for asteroid in asteroids:
            asteroid.move(WIDTH, HEIGHT)
            asteroid.rotate()

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > boost_spawn_time:
            health_boost.append(Heal(random.randint(int(WIDTH * .1), int(WIDTH * .9)), random.randint(int(HEIGHT*.1), int(HEIGHT*.9)),pygame.image.load('Sprites/Powerups/heal_fin.png')))
            last_spawn_time = current_time

        for recharge in health_boost:
            recharge.draw(screen)
            recharge.handle_collision(ship1)
            recharge.handle_collision(ship2)

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
            done = False
            if ship1.is_dead():
                ship1.explode()
                ship1.update_explosion_animation()
                done = ship1.lasers_gone()
            else:
                ship2.explode()
                ship2.update_explosion_animation()
                done = ship2.lasers_gone()



            if done:
                if ship1.is_dead() and ship2.is_dead():
                    winner = "Nobody"
                else:
                    winner = "Player 2" if ship1.is_dead() else "Player 1"
                choice = show_end_menu(winner)
                if choice == "play_again":
                    game_loop(ship1_type, ship2_type)
                elif choice == "switch_characters":
                    ship1_type = show_ship_selection(1)
                    show_confirmation(1, ship1_type)
                    ship2_type = show_ship_selection(2)
                    show_confirmation(2, ship2_type)
                    game_loop(ship1_type, ship2_type)
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