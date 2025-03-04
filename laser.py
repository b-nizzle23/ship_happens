# laser.py
import math
import pygame
import random

class Laser:
    def __init__(self, x, y, angle, speed, damage, range_, bullet_Size):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.range = range_
        self.distance_traveled = 0
        self.active = True
        self.bullet_size = bullet_Size

        if bullet_Size == "big":
            self.image = pygame.image.load("Sprites/Bullets/Big Bullet.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (30, 30))  # Resize if needed
        elif bullet_Size == "normal":
            self.image = pygame.image.load("Sprites/Bullets/Bullet.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (15, 15))  # Resize if needed
        elif bullet_Size == "small":
            self.image = pygame.image.load("Sprites/Bullets/SmallBullet.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (7, 3.5))  # Resize if needed
        elif bullet_Size == "shrapnel":
            self.image = pygame.image.load("Sprites/Bullets/shrapnel.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (random.randint(10,15), random.randint(10,15)))
        # Rotate to match the shooting direction
        self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.distance_traveled += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        if self.active:
            screen.blit(self.rotated_image, self.rect.topleft)
        # Draw the laser image

    def has_expired(self):
        return self.distance_traveled >= self.range or not self.active

    def handle_laser_asteroid_collision(self, asteroid):
        # Check if the laser has collided with the asteroid
        if math.hypot(self.x - asteroid.x, self.y - asteroid.y) < asteroid.size:
            self.active = False  # Deactivate the laser
