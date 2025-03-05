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
        self.rotated_image = pygame.transform.rotate(self.image,-self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))
        self.offset_x = beam_length / 2 * math.cos(math.radians(self.angle))
        self.offset_y = beam_length / 2 * math.sin(math.radians(self.angle))

    def update(self, ship_x, ship_y, ship_angle):
        rad_angle = math.radians(ship_angle)

        self.x = ship_x + (self.range / 2) * math.cos(rad_angle)
        self.y = ship_y + (self.range / 2) * math.sin(rad_angle)
        self.angle = ship_angle
        self.update_beam_size()


    def draw(self, screen):
        if self.active:
            screen.blit(self.rotated_image, self.rect.topleft)
            self.draw_hitbox(screen)

    def draw_hitbox(self, screen):
        if self.active:
            # Calculate the four corners of the hitbox
            rad_angle = math.radians(self.angle)
            beam_start = pygame.Vector2(self.x - (self.range / 2) * math.cos(rad_angle),  self.y - (self.range / 2) * math.sin(rad_angle))
            beam_end = pygame.Vector2(
                self.x + (self.range / 2) * math.cos(rad_angle),
                self.y + (self.range / 2) * math.sin(rad_angle)
            )
            width = 10  # Beam's width
            perpendicular = pygame.Vector2(-math.sin(rad_angle), math.cos(rad_angle)) * width / 2

            points = [
                beam_start + perpendicular,
                beam_start - perpendicular,
                beam_end - perpendicular,
                beam_end + perpendicular
            ]

            pygame.draw.polygon(screen, (255, 0, 0), points, 2)
    def check_collision(self, enemy):
        if self.active:
            # Calculate the four corners of the hitbox
            rad_angle = math.radians(self.angle)
            beam_start = pygame.Vector2(self.x - (self.range / 2) * math.cos(rad_angle),  self.y - (self.range / 2) * math.sin(rad_angle))
            beam_end = pygame.Vector2(
                self.x + (self.range / 2) * math.cos(rad_angle),
                self.y + (self.range / 2) * math.sin(rad_angle)
            )
            width = 10  # Beam's width
            perpendicular = pygame.Vector2(-math.sin(rad_angle), math.cos(rad_angle)) * width / 2

            points = [
                beam_start + perpendicular,
                beam_start - perpendicular,
                beam_end - perpendicular,
                beam_end + perpendicular
            ]

            # Create a polygon for the beam hitbox
            beam_hitbox = pygame.Rect(min(p.x for p in points), min(p.y for p in points),
                                      max(p.x for p in points) - min(p.x for p in points),
                                      max(p.y for p in points) - min(p.y for p in points))

            # Create a polygon for the enemy hitbox
            enemy_hitbox = pygame.Rect(enemy.x - enemy.size // 2, enemy.y - enemy.size // 2, enemy.size, enemy.size)

            return beam_hitbox.colliderect(enemy_hitbox)
        return False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False