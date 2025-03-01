import pygame
import math

class PlayerShip:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.health = 100
        self.max_health = 100
        self.shooting_cooldown = 0.3  # Time between shots
        self.current_cooldown = 0
        self.firing_direction = 0  # Angle in radians
        self.max_speed = 5
        self.invulnerable = False
        self.invulnerability_timer = 0

    def move(self, direction):
        """Updates velocity based on player input (direction as a Vector2)."""
        self.velocity += direction
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, delta_time):
        """Updates the position and cooldowns."""
        self.position += self.velocity * delta_time
        self.current_cooldown = max(0, self.current_cooldown - delta_time)
        if self.invulnerable:
            self.invulnerability_timer -= delta_time
            if self.invulnerability_timer <= 0:
                self.invulnerable = False

    def shoot(self):
        """Returns a projectile if the cooldown allows shooting."""
        if self.current_cooldown == 0:
            self.current_cooldown = self.shooting_cooldown
            return Projectile(self.position.x, self.position.y, self.firing_direction)
        return None

    def take_damage(self, amount):
        """Reduces health and applies invulnerability if needed."""
        if not self.invulnerable:
            self.health -= amount
            if self.health <= 0:
                self.health = 0  # Handle destruction elsewhere
            self.invulnerable = True
            self.invulnerability_timer = 1.5  # 1.5 seconds of invulnerability

    def draw(self, screen):
        """Draws the player on the screen."""
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), 10)

    def is_destroyed(self):
        return self.health <= 0
