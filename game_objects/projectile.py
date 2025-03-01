class Projectile:
    def __init__(self, x, y, direction, speed=10, lifetime=2):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(math.cos(direction), math.sin(direction)) * speed
        self.lifetime = lifetime  # Seconds before disappearing

    def update(self, delta_time):
        """Updates projectile position and lifetime."""
        self.position += self.velocity * delta_time
        self.lifetime -= delta_time
        return self.lifetime > 0

    def draw(self, screen):
        """Draws the projectile on the screen."""
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)
