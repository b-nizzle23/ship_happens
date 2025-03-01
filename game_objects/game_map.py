class GameMap:
    def __init__(self, width, height, cell_size=50, boundary_behavior="wrap"):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.boundary_behavior = boundary_behavior
        self.objects = []  # Stores all game objects
        self.player_ship = None

    def add_object(self, obj):
        """Adds an object to the game map."""
        self.objects.append(obj)

    def remove_object(self, obj):
        """Removes an object from the game map."""
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self, delta_time):
        """Updates all objects and handles collisions."""
        for obj in self.objects:
            obj.update(delta_time)

        # Handle boundary conditions
        for obj in self.objects:
            obj.position.x, obj.position.y = self.handle_boundaries(obj.position.x, obj.position.y)

        # Collision detection
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                if self.objects[i].collide_with(self.objects[j]):
                    self.handle_collision(self.objects[i], self.objects[j])

    def handle_collision(self, obj1, obj2):
        """Handles collisions between objects."""
        if isinstance(obj1, PlayerShip) and isinstance(obj2, Asteroid):
            obj1.take_damage(10)
            if obj2 in self.objects:
                self.objects.remove(obj2)
                self.objects.extend(obj2.split())

        elif isinstance(obj1, Asteroid) and isinstance(obj2, PlayerShip):
            obj2.take_damage(10)
            if obj1 in self.objects:
                self.objects.remove(obj1)
                self.objects.extend(obj1.split())

    def handle_boundaries(self, x, y):
        """Handles object wrapping or clamping based on the boundary behavior."""
        if self.boundary_behavior == "wrap":
            x %= self.width
            y %= self.height
        elif self.boundary_behavior == "clamp":
            x = max(0, min(x, self.width))
            y = max(0, min(y, self.height))
        return x, y

    def draw(self, screen):
        """Draws all objects."""
        for obj in self.objects:
            obj.draw(screen)
