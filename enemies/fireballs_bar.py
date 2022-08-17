import pygame
import math

from enemies import Enemy
from import_assets import get_surfaces
import settings.screen
import settings.enemies
import settings.scores
import settings.tiles


surfaces = get_surfaces(folder="enemies", object_type="fireballsbar")


class FireballsBar(Enemy):
    def __init__(self, rect, degrees):
        self.state = "normal"
        self.type = "fireballsbar"
        self.rect = pygame.Rect((rect[0], rect[1], rect[2], rect[3]))
        self.center = pygame.Vector2(self.rect.center)
        self.fireball_width = settings.tiles.tile_size / 4
        self.fireball_r = self.fireball_width * 2
        self.fireballs = []
        self.counter = 0
        self.killed = False
        for i in range(6):
            self.fireballs.append(self.FireBall(self.center, i * self.fireball_r, int(degrees)))

    def update(self, tiles, current_floor, world_shift, enemies_group):
        for fireball in self.fireballs:
            fireball.update(self.counter, self.center)

        self.counter += 0.15
        if self.counter >= 24:
            self.counter = 0

    def draw(self, surface, world_shift, flip=False):
        for fireball in self.fireballs:
            fireball.draw(surface, world_shift)

    def activate(self, cause, dir, stomping_counter):
        return

    def on_screen(self, current_floor, world_shift):
        if self.rect.left <= -world_shift.x + settings.screen.screen_width:
            if self.rect.right < -world_shift.x:
                return False
            if (
                settings.screen.floor_height * current_floor - settings.screen.floor_height
                < self.rect.centery
                < settings.screen.floor_height * current_floor
            ):
                return True

        return False

    def is_colliding(self, rect):
        for fireball in self.fireballs:
            if fireball.rect.colliderect(rect):
                return True
        return False

    def kill(self, dir):
        pass  # da

    class FireBall(pygame.sprite.Sprite):
        def __init__(self, tile_center, r, degrees):
            self.r = r
            self.end = pygame.Vector2()
            self.end.x = r * math.sin(math.radians(degrees)) + tile_center.x
            self.end.y = -1 * r * math.cos(math.radians(degrees)) + tile_center.y

            self.images = surfaces
            self.image = self.images[0]
            self.rect = self.image.get_rect(center=self.end)
            self.index_images = 0

        def update(self, counter, center):
            self.end.x = self.r * math.sin(math.radians(int(counter) * 15)) + center.x
            self.end.y = -1 * self.r * math.cos(math.radians(int(counter) * 15)) + center.y
            self.rect.center = self.end
            self.animate()

        def draw(self, surface, world_shift):
            surface.blit(self.image, (self.rect.x + world_shift.x, self.rect.y + world_shift.y))

        def animate(self):

            self.index_images += settings.enemies.enemies_animation_settings["fireballsbar"]["animation_speed"]
            if self.index_images > 4:
                self.index_images = 0
            self.image = self.images[int(self.index_images)]
