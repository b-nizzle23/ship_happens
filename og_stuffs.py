import pygame
import math
import time
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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Laser:
    def __init__(self, x, y, angle, speed, damage, range_):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.range = range_
        self.distance_traveled = 0

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.distance_traveled += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 3)

    def has_expired(self):
        return self.distance_traveled >= self.range


class TriangleShip:
    def __init__(self, x, y, angle, color, rotation_speed, move_speed, size, contact_damage, attack_speed, bullet_speed,
                 bullet_range, bullet_damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.rotation_speed = rotation_speed
        self.move_speed = move_speed
        self.size = size
        self.contact_damage = contact_damage
        self.health = 1000
        self.attack_speed = attack_speed
        self.bullet_speed = bullet_speed
        self.bullet_range = bullet_range
        self.lasers = []
        self.last_shot_time = 0
        self.last_collision_time = 0
        self.bullet_damage = bullet_damage

    def rotate(self, direction):
        self.angle += self.rotation_speed * direction

    def move_forward(self):
        new_x = self.x + self.move_speed * math.cos(math.radians(self.angle))
        new_y = self.y + self.move_speed * math.sin(math.radians(self.angle))
        half_size = self.size / 2
        if half_size <= new_x <= WIDTH - half_size:
            self.x = new_x
        if half_size <= new_y <= HEIGHT - half_size:
            self.y = new_y

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= 1 / self.attack_speed:
            laser = Laser(self.x, self.y, self.angle, self.bullet_speed, self.bullet_damage, self.bullet_range)
            self.lasers.append(laser)
            self.last_shot_time = current_time

    def update_lasers(self, screen, enemy):
        for laser in self.lasers[:]:
            laser.move()
            if laser.has_expired():
                self.lasers.remove(laser)
            else:
                laser.draw(screen)
                if self.check_collision(laser, enemy):
                    enemy.health -= laser.damage
                    self.lasers.remove(laser)

    def check_collision(self, laser, enemy):
        return math.hypot(laser.x - enemy.x, laser.y - enemy.y) < enemy.size

    def handle_ship_collision(self, enemy):
        distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
        min_distance = self.size + enemy.size
        overlap_margin = 5

        if distance < min_distance - overlap_margin:
            current_time = time.time()
            if current_time - self.last_collision_time >= 0.1:
                self.health -= enemy.contact_damage
                enemy.health -= self.contact_damage
                self.last_collision_time = current_time

            angle_between = math.atan2(self.y - enemy.y, self.x - enemy.x)
            overlap = (min_distance - overlap_margin) - distance
            push_factor = 0.5
            push_x = math.cos(angle_between) * (overlap * push_factor)
            push_y = math.sin(angle_between) * (overlap * push_factor)

            self.x += push_x
            self.y += push_y
            enemy.x -= push_x
            enemy.y -= push_y

    def draw(self, screen):
        points = [
            (self.x + self.size * math.cos(math.radians(self.angle)),
             self.y + self.size * math.sin(math.radians(self.angle))),
            (self.x + self.size * math.cos(math.radians(self.angle + 130)),
             self.y + self.size * math.sin(math.radians(self.angle + 130))),
            (self.x + self.size * math.cos(math.radians(self.angle - 130)),
             self.y + self.size * math.sin(math.radians(self.angle - 130))),
        ]
        pygame.draw.polygon(screen, self.color, points)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        health_ratio = max(self.health / 1000, 0)
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 10
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def is_dead(self):
        return self.health <= 0

# Asteroids
class Asteroid:
    def __init__(self, x, y, angle, rotation_speed, move_speed, size, contact_damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotation_speed = rotation_speed
        self.move_speed = move_speed
        self.size = size
        self.contact_damage = contact_damage

    def rotate(self, direction):
        self.angle += self.rotation_speed * direction

# Create ships
ship1 = TriangleShip(200, 200, 0, (255, 255, 0), 2.5, 3, 50, 40, 1, 20, 600, 500)
ship2 = TriangleShip(600, 600, 180, (255, 0, 0), 4, 5, 40, 7, 2, 9, 350, 250)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship1.rotate(1)
    if keys[pygame.K_RIGHT]:
        ship1.rotate(-1)
    if keys[pygame.K_l]:
        ship1.move_forward()
    if keys[pygame.K_SPACE]:
        ship1.shoot()
    if keys[pygame.K_a]:
        ship2.rotate(1)
    if keys[pygame.K_d]:
        ship2.rotate(-1)
    if keys[pygame.K_f]:
        ship2.move_forward()
    if keys[pygame.K_RETURN]:
        ship2.shoot()

    ship1.handle_ship_collision(ship2)
    ship1.update_lasers(screen, ship2)
    ship2.update_lasers(screen, ship1)
    ship1.draw(screen)
    ship2.draw(screen)

    if ship1.is_dead() or ship2.is_dead():
        print("Yellow Ship Wins!" if ship2.is_dead() else "Red Ship Wins!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
