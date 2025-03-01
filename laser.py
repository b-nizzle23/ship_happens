# laser.py
import math
import pygame

class Laser:
    def __init__(self, x, y, angle, speed, damage, range_, bullet_Size):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.range = range_
        self.distance_traveled = 0

        if bullet_Size == "big":
            self.image = pygame.image.load("Sprites/Bullets/Big Bullet.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (22, 22))  # Resize if needed
        elif bullet_Size == "normal":
            self.image = pygame.image.load("Sprites/Bullets/Bullet.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (15, 15))  # Resize if needed
        elif bullet_Size == "small":
            self.image = pygame.image.load("Sprites/Bullets/SmallBullet.png").convert_alpha()  # Ensure transparency
            self.image = pygame.transform.scale(self.image, (7, 3.5))  # Resize if needed

        # Rotate to match the shooting direction
        self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.distance_traveled += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect.topleft)  # Draw the laser image

    def has_expired(self):
        return self.distance_traveled >= self.range
