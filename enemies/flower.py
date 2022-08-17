import pygame

from enemies import Enemy
from import_assets import get_surfaces
import sound.sound
import sound.channels
import events.custom_events as custom_events

import settings.enemies
import settings.scores


surfaces = get_surfaces("enemies", "flower")


class Flower(Enemy):
    """Flower enemy class.

    Args:
        pygame.sprite.Sprite (class): Inheritance
    """

    def __init__(self, world_type, pos):
        self.images_dict = surfaces[world_type]
        super().__init__("flower", world_type, self.images_dict[0], pos)
        self.state = "normal"
        self.connected_tube = None
        self.staying_counter = 0

    def update(self, tiles, current_floor, world_shift, enemies_group):
        if self.staying_counter == 0:
            self.update_pos()
            self.check_movement()
        else:
            if self.connected_tube.player_colliding:
                self.staying_counter = settings.enemies.enemies_animation_settings["flower"]["staying_time"] / 2
            else:
                self.staying_counter -= 1
                if self.staying_counter <= 0:
                    self.staying_counter = 0

        self.animate()

    def update_pos(self):
        self.rect.y -= self.dir * self.velocities.y

    def check_movement(self):
        def stop_moving_handling():
            self.reverse_direction()
            self.staying_counter = settings.enemies.enemies_animation_settings["flower"]["staying_time"]

        if self.rect.bottom <= self.connected_tube.rect.top:
            self.rect.bottom = self.connected_tube.rect.top
            stop_moving_handling()

        elif self.rect.top >= self.connected_tube.rect.top:
            self.rect.top = self.connected_tube.rect.top
            stop_moving_handling()

    def animate(self):
        """The main function of the flower animation."""
        self.index_images += settings.enemies.enemies_animation_settings[self.type]["animation_speed"]
        if self.index_images > len(self.images_dict):
            self.index_images = 0
        self.image = self.images_dict[int(self.index_images)]

    def activate(self, cause, dir, stomping_counter):
        return

    def kill(self, dir):
        """Make the enemy dead.

        Args:
            dir (int): the direction for death animation.
        """
        sound.sound.play_sound(sound.channels.ChannelsID.enemies, "kick")
        custom_events.post_event(event_id=custom_events.EventID.ADD_SCORE, score=settings.scores.stomping_scores[0])
        custom_events.post_event(
            event_id=custom_events.EventID.ADD_PARTICLE,
            particle_type="score",
            particle_pos=self.rect.topleft,
            score=settings.scores.stomping_scores[0],
        )
        self.killed = True

    def draw(self, surface, world_shift, flip=False):
        super().draw(surface, world_shift)
        self.connected_tube.asinc_draw(surface, world_shift)
