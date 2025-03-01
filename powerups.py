import pygame

class Heal:
    def __init__(self, x, y, sprite, size=35):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 125, 0)  # Light blue
        self.active = True  # To track if the power-up is still available
        self.image = sprite
        self.image = pygame.transform.scale(self.image, (size, size))

    def check_collision(self, ship):
        """Check if the ship collides with the power-up (distance-based)."""
        distance = ((self.x - ship.x) ** 2 + (self.y - ship.y) ** 2) ** 0.5
        return distance < (self.size + ship.size) / 2  # Simple circle collision

    def handle_collision(self, ship):
        """If there's a collision, heal the ship and deactivate power-up."""
        if self.check_collision(ship) and self.active:
            if ship.health + 500 > ship.max_health:
                ship.health = ship.max_health
            else:
                ship.health += 500
            self.active = False  # Remove the power-up after use

    def draw(self, screen):
        """Draw the power-up if it's still active."""
        if self.active:
            screen.blit(self.image, (self.x,self.y))

