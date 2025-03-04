# triangle_ship.py
import pygame
import math
import time
from laser import Laser
import pygame
from Beam import Beam



vec = pygame.math.Vector2
import random

class TriangleShip:
    def __init__(self, x, y, angle, name):
        # Dictionary that maps ship names to their parameters
        ship_data = {
            "base": {
                "image": pygame.image.load("Sprites/Ships/base.png").convert_alpha(),  # Tan
                "rotation_speed": 2.75,
                "move_speed": vec(0,0),
                "size": 30,
                "contact_damage": 100,
                "attack_speed": 2.5,
                "bullet_speed": 10,
                "bullet_range": 600,
                "bullet_damage": 250,
                "health": 1000,
                "bullet_size": "normal",
                "acceleration": .25,
                "max_speed": 4
            },
            "sniper": {
                "image": pygame.image.load("Sprites/Ships/sniper.png").convert_alpha(),
                "rotation_speed": 2.25,
                "move_speed": vec(0,0),
                "size": 20,
                "contact_damage": 100,
                "attack_speed": 1.25,
                "bullet_speed": 20,
                "bullet_range": 850,
                "bullet_damage": 500,
                "health": 750,
                "bullet_size": "small",
                "acceleration": .4,
                "max_speed": 3
            },
            "melee": {
                "angle": 180,
                "image": pygame.image.load("Sprites/Ships/melee.png").convert_alpha(),
                "rotation_speed": 2.5,
                "move_speed": vec(0,0),
                "size": 35,
                "contact_damage": 250,
                "attack_speed": 1.5,
                "bullet_speed": 10,
                "bullet_range": 600,
                "bullet_damage": 100,
                "health": 1000,
                "bullet_size": "normal",
                "acceleration": .4,
                "max_speed": 4.5
            },
            "behemoth": {
                "image": pygame.image.load("Sprites/Ships/behemoth.png").convert_alpha(),  # Blue
                "rotation_speed": 3,
                "move_speed": vec(0,0),
                "size": 45,
                "contact_damage": 100,
                "attack_speed": 1.25,
                "bullet_speed": 8,
                "bullet_range": 500,
                "bullet_damage": 750,
                "health": 1700,
                "bullet_size": "big",
                "acceleration": .15,
                "max_speed": 1.75
            },
            "assassin": {
                "image": pygame.image.load("Sprites/Ships/assassin.png").convert_alpha(),
                "rotation_speed": 3.5,
                "move_speed": vec(0,0),
                "size": 30,
                "contact_damage": 100,
                "attack_speed": .75,
                "bullet_speed": 10,
                "bullet_range": 500,
                "bullet_damage": 420,
                "health": 1000,
                "bullet_size": "small",
                "acceleration": .4,
                "max_speed": 4.25

            },
            "minigun": {
                "image": pygame.image.load("Sprites/Ships/minigun.png").convert_alpha(),
                "rotation_speed": 2,
                "move_speed": vec(0,0),
                "size": 30,
                "contact_damage": 100,
                "attack_speed": 4,
                "bullet_speed": 20,
                "bullet_range": 600,
                "bullet_damage": 100,
                "health": 1000,
                "bullet_size": "small",
                "acceleration": .25,
                "max_speed": 4
            },
            "beam": {
                "image": pygame.image.load("Sprites/Ships/beam.png").convert_alpha(),  # Tan
                "rotation_speed": 2.75,
                "move_speed": vec(0, 0),
                "size": 30,
                "contact_damage": 100,
                "attack_speed": 2.5,
                "bullet_speed": 10,
                "bullet_range": 400,
                "bullet_damage": 250,
                "health": 1000,
                "bullet_size": "beam",
                "acceleration": .25,
                "max_speed": 4
            },
        }

        # Get the data for the selected ship name
        if name in ship_data:
            data = ship_data[name]
        else:
            raise ValueError(f"Invalid ship name: {name}")

        # Assign values to the class properties
        self.x = x
        self.dead = False
        self.y = y
        self.angle = angle
        if self.dead:
            self.image = pygame.image.load("")
        else:
            self.image = data["image"]
        self.rotation_speed = data["rotation_speed"]
        self.move_speed = data["move_speed"]
        self.size = data["size"]
        self.contact_damage = data["contact_damage"]
        self.attack_speed = data["attack_speed"]
        self.bullet_speed = data["bullet_speed"]
        self.bullet_range = data["bullet_range"]
        self.bullet_damage = data["bullet_damage"]
        self.health = data["health"]
        self.max_health = data["health"]
        self.lasers = []
        self.last_shot_time = 0
        self.last_collision_time = 0
        self.bullet_Size = data["bullet_size"]
        self.vx = 0
        self.vy = 0
        self.thrust = data["acceleration"]
        self.topspeed = data["max_speed"]# Acceleration speed
        self.name = name
        self.n = 1
        self.j = 1
        self.explosion_sprites = [pygame.image.load(f"Sprites/Explode/explode{i}.png").convert_alpha() for i in
                                  range(2, 4)]
        self.explosion_frame = 0
        self.explosion_image = pygame.image.load("Sprites/Bullets/Bullet.png").convert_alpha()
        self.aniconter = 0
        self.explosion_loops = 0
        self.beam = Beam(self.x, self.y, self.angle, self.bullet_damage, self.bullet_range) if self.name == "beam" else None



    def rotate(self, direction):
        self.angle += self.rotation_speed * direction
    def thrust_ani(self):
        if not self.is_dead():
            self.n += 1
            if self.n == 10:  # After 9 frames, switch to the next sprite
                self.j += 1
                self.n = 1  # Reset n to 1 for the next animation cycle

            if self.j > 3:  # If j exceeds 3, reset it for the animation loop
                self.j = 1

            # Load the correct sprite based on the current animation frame
            self.image = pygame.image.load(f"Sprites/Ships/Thrust ani/{self.name}/{self.name}{self.j}.png").convert_alpha()
    def not_thrust(self):
        if not self.is_dead():
            self.image = pygame.image.load("Sprites/Ships/"+self.name+".png").convert_alpha()


    def apply_thrust(self):
        if not self.is_dead():

            # Accelerate or decelerate in the direction the ship is facing
            rad = math.radians(self.angle)  # Convert degrees to radians

            # Apply thrust in the x direction (forward/backward)
            self.vx += self.thrust * math.cos(rad)

            # Apply thrust in the y direction (forward/backward)
            self.vy += self.thrust * math.sin(rad)

            # Ensure the velocity does not exceed the max speed in any direction
            speed = math.hypot(self.vx, self.vy)  # Calculate current speed
            if speed > self.topspeed:
                # Normalize the velocity vector and apply max speed
                self.vx = (self.vx / speed) * self.topspeed
                self.vy = (self.vy / speed) * self.topspeed

    def update_position(self, width, height):
        if not self.is_dead():
            # Move ship based on velocity
            self.x += self.vx
            self.y += self.vy

            # Ensure the ship doesn't go beyond the screen boundaries
            if self.x < 0:
                self.x = 0  # Prevent moving beyond the left edge
            elif self.x > width:
                self.x = width  # Prevent moving beyond the right edge

            if self.y < 0:
                self.y = 0  # Prevent moving beyond the top edge
            elif self.y > height:
                self.y = height  # Prevent moving beyond the bottom edge




    def shoot(self):
        if not self.is_dead():
            current_time = time.time()
            if current_time - self.last_shot_time >= 1 / self.attack_speed:
                laser = Laser(self.x, self.y, self.angle, self.bullet_speed, self.bullet_damage, self.bullet_range, self.bullet_Size)
                self.lasers.append(laser)
                self.last_shot_time = current_time

    def toggle_beam(self):
        if self.beam:
            if self.beam.active:
                self.beam.deactivate()
            else:
                self.beam.activate()


    def update_lasers(self, screen, enemy):
        for laser in self.lasers[:]:
            laser.move()
            if laser.has_expired():
                self.lasers.remove(laser)
            else:
                laser.draw(screen)
                if self.check_collision(laser, enemy):
                    enemy.health -= laser.damage
                    if not laser.bullet_size == "shrapnel":
                        self.lasers.remove(laser)

    def update_beam(self, screen, enemy):
        if self.beam:
            self.beam.update(self.x, self.y, self.angle, self.size)
            self.beam.draw(screen)
            if self.check_collision(self.beam, enemy):
                enemy.health -= self.beam.damage
    def check_collision(self, laser, enemy):
        return math.hypot(laser.x - enemy.x, laser.y - enemy.y) < enemy.size

    def handle_ship_collision(self, enemy):
        distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
        min_distance = self.size + enemy.size
        overlap_margin = 5

        if distance < min_distance - overlap_margin:
            current_time = time.time()
            if current_time - self.last_collision_time >= 0.1:
                self.health -= enemy.contact_damage
                enemy.health -= self.contact_damage
                self.last_collision_time = current_time

            angle_between = math.atan2(self.y - enemy.y, self.x - enemy.x)
            overlap = (min_distance - overlap_margin) - distance
            push_factor = 0.5
            push_x = math.cos(angle_between) * (overlap * push_factor)
            push_y = math.sin(angle_between) * (overlap * push_factor)

            self.x += push_x
            self.y += push_y
            enemy.x -= push_x
            enemy.y -= push_y

    def handle_ship_asteroid_collision(self, asteroid):
        # Calculate distance between ship and asteroid centers
        distance = math.hypot(self.x - asteroid.x, self.y - asteroid.y)
        
        # Collision threshold is the sum of their sizes
        min_distance = self.size + asteroid.size
        
        if distance < min_distance:  # If they collide
            # Prevent ship from moving (can add push-back effect or stop movement here)
            overlap = min_distance - distance
            angle_between = math.atan2(self.y - asteroid.y, self.x - asteroid.x)
            push_factor = 0.5
            push_x = math.cos(angle_between) * overlap * push_factor
            push_y = math.sin(angle_between) * overlap * push_factor
            self.health -= asteroid.contact_damage
            
            self.x += push_x
            self.y += push_y


    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if not self.is_dead():
            bar_width = 50
            bar_height = 5
            health_ratio = max(self.health / self.max_health, 0)
            bar_x = self.x - bar_width // 2
            bar_y = self.y - self.size - 10
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def is_dead(self):
        return self.health <= 0

    def explode(self):
        if not self.dead:
            for i in range(random.randint(5, 6)):
                laser = Laser(self.x, self.y, random.randint(0, 360), random.uniform(.5, .75), 0, 100, 'shrapnel')
                self.lasers.append(laser)
                self.dead = True
            self.update_explosion_animation()



    def update_explosion_animation(self):
        if self.is_dead() and self.explosion_loops < 3:
            if self.name == "beam":
                self.beam.deactivate()
            if self.explosion_frame % 10 == 0:
                self.aniconter += 1
                self.image = self.explosion_sprites[self.aniconter % len(self.explosion_sprites)]
                if self.aniconter % len(self.explosion_sprites) == 0:
                    self.explosion_loops += 1
            self.explosion_frame += 1
        else:
            self.image = self.explosion_image
            self.contact_damage = 0
    def lasers_gone(self):
        if not self.lasers:
            return True



