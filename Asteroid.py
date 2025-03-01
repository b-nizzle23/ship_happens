import pygame
import random

class Asteroid:
    def __init__(self, x, y, angle, rotation_speed, move_speed, size, contact_damage, sprite):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotation_speed = rotation_speed
        self.move_speed = move_speed
        self.size = size
        self.contact_damage = contact_damage
        self.image = sprite
        self.image = pygame.transform.scale(self.image, (size,size))

    def rotate(self):
        self.angle += 1

    def move(self, WIDTH, HEIGHT):
        self.x += random.randint(0,1)
        self.y += random.randint(1,3)
        if self.y > HEIGHT:
            self.x = random.randint(0, WIDTH)
            self.y = -50

    def check_collision(self):
        return

    def handle_collision(self):
        return

    def draw(self, screen):
        #pygame.draw.circle(screen, (120, 100, 90), (int(self.x), int(self.y)), self.size)
        screen.blit(self.image, (self.x,self.y))