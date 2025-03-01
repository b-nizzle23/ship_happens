import pygame
import random

class Asteroid:
    def __init__(self, x, y, angle, rotation_speed, move_speed, size, contact_damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotation_speed = rotation_speed
        self.move_speed = move_speed
        self.size = size
        self.contact_damage = contact_damage

    def rotate(self):
        self.angle += 1

    def move(self):
        self.x += random.randint(0,3)
        self.y += random.randint(2,5)

    def check_collision(self):
        return

    def handle_collision(self):
        return

    def draw(self, screen):
        pygame.draw.circle(screen, (120, 100, 90), (int(self.x), int(self.y)), self.size)