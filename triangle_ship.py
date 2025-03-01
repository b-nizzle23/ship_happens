# triangle_ship.py
import pygame
import math
import time
from laser import Laser
import pygame

class TriangleShip:
    def __init__(self, x, y, angle, name):
        # Dictionary that maps ship names to their parameters
        ship_data = {
            "base": {
                "color": (210, 180, 140),  # Tan
                "rotation_speed": 2.75,
                "move_speed": 4,
                "size": 30,
                "contact_damage": 100,
                "attack_speed": 1.5,
                "bullet_speed": 10,
                "bullet_range": 600,
                "bullet_damage": 250,
                "health": 1000
            },
            "sniper": {
                "color": (255, 255, 255),  # White
                "rotation_speed": 2.25,
                "move_speed": 3,
                "size": 20,
                "contact_damage": 100,
                "attack_speed": 1.25,
                "bullet_speed": 20,
                "bullet_range": 850,
                "bullet_damage": 500,
                "health": 750
            },
            "melee": {
                "angle": 180,
                "color": (255, 0, 0),  # Red
                "rotation_speed": 2.5,
                "move_speed": 4.5,
                "size": 35,
                "contact_damage": 250,
                "attack_speed": 1.5,
                "bullet_speed": 10,
                "bullet_range": 600,
                "bullet_damage": 100,
                "health": 1000
            },
            "behemoth": {
                "color": (0, 0, 255 ),  # Blue
                "rotation_speed": 3,
                "move_speed": 2.5,
                "size": 45,
                "contact_damage": 100,
                "attack_speed": 1.25,
                "bullet_speed": 8,
                "bullet_range": 500,
                "bullet_damage": 750,
                "health": 1200
            },
            "assassin": {
                "color": (128, 128, 128),  # Grey
                "rotation_speed": 3.5,
                "move_speed": 4.25,
                "size": 30,
                "contact_damage": 100,
                "attack_speed": .75,
                "bullet_speed": 10,
                "bullet_range": 500,
                "bullet_damage": 420,
                "health": 750
            },
            "minigun": {
                "color": (128, 0, 128),  # Purple
                "rotation_speed": 2,
                "move_speed": 4,
                "size": 30,
                "contact_damage": 100,
                "attack_speed": 4,
                "bullet_speed": 20,
                "bullet_range": 600,
                "bullet_damage": 100,
                "health": 1000
            }
        }

        # Get the data for the selected ship name
        if name in ship_data:
            data = ship_data[name]
        else:
            raise ValueError(f"Invalid ship name: {name}")

        # Assign values to the class properties
        self.x = x
        self.y = y
        self.angle = angle
        self.color = data["color"]
        self.rotation_speed = data["rotation_speed"]
        self.move_speed = data["move_speed"]
        self.size = data["size"]
        self.contact_damage = data["contact_damage"]
        self.attack_speed = data["attack_speed"]
        self.bullet_speed = data["bullet_speed"]
        self.bullet_range = data["bullet_range"]
        self.bullet_damage = data["bullet_damage"]
        self.health = data["health"]
        self.max_health = data["health"]
        self.lasers = []
        self.last_shot_time = 0
        self.last_collision_time = 0


    def rotate(self, direction):
        self.angle += self.rotation_speed * direction


    def move_forward(self, WIDTH, HEIGHT):

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

    def handle_ship_asteroid_collision(self, asteroid):
        # Calculate distance between ship and asteroid centers
        distance = math.hypot(self.x - asteroid.x, self.y - asteroid.y)
        
        # Collision threshold is the sum of their sizes
        min_distance = self.size + asteroid.size
        
        if distance < min_distance:  # If they collide
            # Prevent ship from moving (can add push-back effect or stop movement here)
            overlap = min_distance - distance
            angle_between = math.atan2(self.y - asteroid.y, self.x - asteroid.x)
            push_factor = 0.5
            push_x = math.cos(angle_between) * overlap * push_factor
            push_y = math.sin(angle_between) * overlap * push_factor
            
            self.x += push_x
            self.y += push_y


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
