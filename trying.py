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
WHITE = (255, 255, 255)

SHIP_TYPES = ["base", "sniper", "melee", "behemoth", "assassin", "minigun"]

def show_menu(screen, winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"{winner} wins! Play again?", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    play_again_text = font.render("Play Again", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    switch_chars_text = font.render("Switch Characters", True, WHITE)
    switch_chars_rect = switch_chars_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    quit_text = font.render("Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    screen.blit(text, text_rect)
    screen.blit(play_again_text, play_again_rect)
    screen.blit(switch_chars_text, switch_chars_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    return "play_again"
                elif switch_chars_rect.collidepoint(mouse_pos):
                    return "switch_chars"
                elif quit_rect.collidepoint(mouse_pos):
                    return "quit"

def show_ship_selection(screen, player_num):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {player_num}, choose your ship:", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(text, text_rect)

    ship_rects = []
    for i, ship_type in enumerate(SHIP_TYPES):
        ship_text = font.render(ship_type, True, WHITE)
        ship_rect = ship_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + i * 50))
        screen.blit(ship_text, ship_rect)
        ship_rects.append(ship_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(ship_rects):
                    if rect.collidepoint(mouse_pos):
                        return SHIP_TYPES[i]
        pygame.time.Clock().tick(30)

def show_confirmation(screen, player_num, ship_type):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {player_num} chose: {ship_type}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    delay_timer = pygame.time.get_ticks()
    delay_duration = 1000
    while pygame.time.get_ticks() - delay_timer < delay_duration:
        pygame.event.pump()
        pygame.time.Clock().tick(30)

def run_game(ship1_name, ship2_name):
    ship2 = TriangleShip(WIDTH * .9, HEIGHT * .9, 180, ship2_name)
    ship1 = TriangleShip(WIDTH * .1, HEIGHT * .1, 0, ship1_name)
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            ship2.rotate(1)
        if keys[pygame.K_LEFT]:
            ship2.rotate(-1)
        if keys[pygame.K_UP]:
            ship2.move_forward(WIDTH, HEIGHT)
        if keys[pygame.K_l]:
            ship2.shoot()
        if keys[pygame.K_d]:
            ship1.rotate(1)
        if keys[pygame.K_a]:
            ship1.rotate(-1)
        if keys[pygame.K_w]:
            ship1.move_forward(WIDTH, HEIGHT)
        if keys[pygame.K_SPACE]:
            ship1.shoot()

        ship1.handle_ship_collision(ship2)
        ship1.update_lasers(screen, ship2)
        ship2.update_lasers(screen, ship1)
        ship1.draw(screen)
        ship2.draw(screen)

        if ship1.is_dead() or ship2.is_dead():
            winner = "Player 1" if ship2.is_dead() else "Player 2"
            result = show_menu(screen, winner)
            return result

        pygame.display.flip()
        clock.tick(60)

    return "quit"

ship1_name = 'behemoth'
ship2_name = 'base'

while True:
    result = run_game(ship1_name, ship2_name)
    if result == "quit":
        break
    elif result == "switch_chars":
        new_ship1_name = show_ship_selection(screen, 1)
        if new_ship1_name:
            show_confirmation(screen, 1, new_ship1_name)
            new_ship2_name = show_ship_selection(screen, 2)
            if new_ship2_name:
                show_confirmation(screen, 2, new_ship2_name)
                ship1_name = new_ship1_name
                ship2_name = new_ship2_name