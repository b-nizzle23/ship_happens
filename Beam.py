import pygame
import math

class Beam:
    def __init__(self, x, y, angle, damage, range_):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.range = range_
        self.active = False  # Beam starts off
        self.image = pygame.image.load("Sprites/Bullets/Beam.png").convert_alpha()
        self.update_beam_size()

    def update_beam_size(self):
        # Adjust beam length based on the range
        beam_length = self.range
        self.image = pygame.transform.scale(self.image, (beam_length, 10))  # Adjust size as needed
        self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))
        self.offset_x = beam_length / 2 * -math.cos(math.radians(self.angle))
        self.offset_y = beam_length / 2 * -math.sin(math.radians(self.angle))

    def update(self, ship_x, ship_y, ship_angle, ship_size):
        rad = math.radians(ship_angle)
        self.x = ship_x + (ship_size + self.offset_x) * math.cos(rad)
        self.y = ship_y + (ship_size + self.offset_y) * math.sin(rad)
        self.angle = ship_angle
        self.update_beam_size()

    def draw(self, screen):
        if self.active:
            screen.blit(self.rotated_image, self.rect.topleft)

    def check_collision(self, enemy):
        if self.active:
            # Create a line segment representing the beam
            beam_start = pygame.Vector2(self.x, self.y)
            beam_end = pygame.Vector2(
                self.x + self.range * math.cos(math.radians(self.angle)),
                self.y + self.range * math.sin(math.radians(self.angle))
            )
            enemy_pos = pygame.Vector2(enemy.x, enemy.y)
            distance = enemy_pos.distance_to(beam_start) + enemy_pos.distance_to(beam_end)
            beam_length = beam_start.distance_to(beam_end)

            # Check if the distance from the enemy to the beam is within the beam's length
            if distance <= beam_length + enemy.size:
                return True
        return False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False