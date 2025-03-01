# laser.py
import math
import pygame

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
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

    def has_expired(self):
        return self.distance_traveled >= self.range
