from triangle_ship import TriangleShip
from Asteroid import *
import random

# Initialize Pygame
pygame.init()

# Get full screen size
full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Set window size to 75% of full screenl
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
    ship2 = TriangleShip(150,100,0,'base')
    ship1 = TriangleShip(1000, 600,180,'behemoth')

    # Create asteroids
    asteroid1 = Asteroid(random.randint(0, int(WIDTH/3)), HEIGHT*.3, 0, 5, 1, random.randint(10, 35), 100)
    asteroid2 = Asteroid(random.randint(int(WIDTH/3), int(WIDTH/3*2)), HEIGHT/2, 0, 5, 1, random.randint(20, 70), 100)
    asteroid3 = Asteroid(random.randint(int(WIDTH/3*2), WIDTH), -50, 0, 5, 1, random.randint(10, 35), 100)

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(BLACK,(0,0))



        # move asteroids
        asteroid1.move(WIDTH, HEIGHT)
        asteroid1.rotate()
        asteroid2.move(WIDTH, HEIGHT)
        asteroid2.rotate()
        asteroid3.move(WIDTH, HEIGHT)
        asteroid3.rotate()
        
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

        # In the game loop after handling ship movement
        for asteroid in [asteroid1, asteroid2, asteroid3]:
            ship1.handle_ship_asteroid_collision(asteroid)
            ship2.handle_ship_asteroid_collision(asteroid)
            ship1.handle_laser_asteroid_collision(asteroid)
            ship2.handle_laser_asteroid_collision(asteroid)

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
                if ship1.is_dead():
                    winner = "Player 1"
                else:
                    winner = "Player 2"
                #show_end_menu(screen,winner)
                # if show_end_menu(screen,winner) == 'play_again':

            pygame.display.flip()
            clock.tick(60)

def main():
    menu_running = True
    while menu_running:
        screen.blit(BLACK, (0,0))
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

# SHIP_TYPES = ["base", "sniper", "melee", "behemoth", "assassin", "minigun"]
#
# def show_end_menu(screen, winner):
#     font = pygame.font.Font(None, 36)
#     text = font.render(f"{winner} wins! Play again?", True, WHITE)
#     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
#
#     play_again_text = font.render("Play Again", True, WHITE)
#     play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#
#     switch_chars_text = font.render("Switch Characters", True, WHITE)
#     switch_chars_rect = switch_chars_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
#
#     quit_text = font.render("Quit", True, WHITE)
#     quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
#
#     screen.blit(text, text_rect)
#     screen.blit(play_again_text, play_again_rect)
#     screen.blit(switch_chars_text, switch_chars_rect)
#     screen.blit(quit_text, quit_rect)
#     pygame.display.flip()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return "quit"
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = pygame.mouse.get_pos()
#                 if play_again_rect.collidepoint(mouse_pos):
#                     return "play_again"
#                 elif switch_chars_rect.collidepoint(mouse_pos):
#                     return "switch_chars"
#                 elif quit_rect.collidepoint(mouse_pos):
#                     return "quit"
#
# def show_ship_selection(screen, player_num):
#     screen.fill(BLACK)
#     font = pygame.font.Font(None, 36)
#     text = font.render(f"Player {player_num}, choose your ship:", True, WHITE)
#     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
#     screen.blit(text, text_rect)
#
#     ship_rects = []
#     for i, ship_type in enumerate(SHIP_TYPES):
#         ship_text = font.render(ship_type, True, WHITE)
#         ship_rect = ship_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + i * 50))
#         screen.blit(ship_text, ship_rect)
#         ship_rects.append(ship_rect)
#
#     pygame.display.flip()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return None
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = pygame.mouse.get_pos()
#                 for i, rect in enumerate(ship_rects):
#                     if rect.collidepoint(mouse_pos):
#                         return SHIP_TYPES[i]
#         pygame.time.Clock().tick(30)
#
# def show_confirmation(screen, player_num, ship_type):
#     screen.fill(BLACK)
#     font = pygame.font.Font(None, 36)
#     text = font.render(f"Player {player_num} chose: {ship_type}", True, WHITE)
#     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(text, text_rect)
#     pygame.display.flip()
#
#     delay_timer = pygame.time.get_ticks()
#     delay_duration = 1000
#     while pygame.time.get_ticks() - delay_timer < delay_duration:
#         pygame.event.pump()
#         pygame.time.Clock().tick(30)

main()
