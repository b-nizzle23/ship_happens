# triangle_ship.py
import pygame
import math
import time
from laser import Laser

class TriangleShip:
    def __init__(self, x, y, angle, color, rotation_speed, move_speed, size, contact_damage, attack_speed, bullet_speed,
                 bullet_range, bullet_damage, health):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.rotation_speed = rotation_speed
        self.move_speed = move_speed
        self.size = size
        self.contact_damage = contact_damage
        self.health = health
        self.max_health = health
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
        health_ratio = max(self.health / self.max_health, 0)
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 10
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def is_dead(self):
        return self.health <= 0
