from enemies import Enemy
from import_assets import get_surfaces, get_sounds
import events.custom_events as custom_events
import sound.sound
import sound.channels

import settings.screen
import settings.enemies
import settings.scores

import settings.tiles


surfaces = get_surfaces(folder="enemies", object_type="koopa")


class Koopa(Enemy):
    """Koopa enemy type class.

    Args:
        Enemy (class): Inheritance
    """

    def __init__(self, koopa_type, world_type, pos):
        if koopa_type == "normal":
            self.state = "move"
        else:
            self.state = "fly"
        self.images_dict = surfaces[world_type]

        super().__init__(
            "koopa",
            world_type,
            self.images_dict[self.state][0],
            (pos[0], pos[1] - 10 * settings.screen.pixel_multiplicator),
        )

        self.turn_velocity = self.velocities.x * 4
        self.turning_counter = 0
        self.image_dir = -1
        self.y_dir = 1
        self.original_rect = self.rect.copy()
        self.moving_distance = 6 * settings.tiles.tile_size

    def update(self, tiles, current_floor, world_shift, enemies_group):
        """The main update function of Goomba class.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """

        if self.state in ("move", "turn", "hide"):
            super().update(tiles, current_floor, world_shift, enemies_group)
            if self.world_type == "general" and self.state == "move" and self.colliding_bot:
                self.prevent_falling(tiles, current_floor)
        elif self.state == "fly":
            self.fly_update()
            self.animate()
        elif self.state == "dead":
            self.dead_update()

    def fly_update(self):
        self.rect.y += self.y_dir * self.velocities.y
        self.reverse_y_direction()

    def reverse_y_direction(self):
        if self.rect.top < self.original_rect.top or self.rect.top > self.original_rect.top + self.moving_distance:
            self.y_dir *= -1

    def draw(self, surface, world_shift, flip=False):

        if self.state == "move" and self.dir == 1:
            flip = True

        super().draw(surface, world_shift, flip)

    def activate(self, cause, dir, stomping_counter=0):
        """Activate function triggerd when the enemy gets hit from above.

        Args:
            cause (Str): Who called thi method.
            dir (int): Direction in case of animation
        """
        score = 0
        sound.sound.play_sound(sound.channels.ChannelsID.enemies, "kick")
        if self.state == "fly":
            self.velocities.y = 0
            self.state = "move"
        elif self.state == "move":
            score = settings.scores.stomping_scores[stomping_counter]
            self.velocities.x = 0
            self.state = "hide"
        elif self.state == "hide":
            score = settings.scores.kicking_scores[min([stomping_counter, 1])]
            self.state = "turn"
            self.velocities.x = self.turn_velocity
            self.dir = dir
        elif self.state == "turn":
            score = settings.scores.stomping_scores[stomping_counter]
            self.state = "hide"
            self.velocities.x = 0

        if score == 0:
            return

        custom_events.post_event(event_id=custom_events.EventID.ADD_SCORE, score=score)
        custom_events.post_event(
            event_id=custom_events.EventID.ADD_PARTICLE_SCORE,
            particle_pos=self.rect.topleft,
            score=score,
        )

    def enemy_horizontal_collision_handling(self, enemy):
        """Handle thehorizontal collision with an enemy.

        Args:
            enemy (enemy): The colliding enemy.
        """
        score = 0
        if self.state == "turn":
            self.turning_counter += 1
            enemy.kill(self.dir)
            score = settings.scores.turning_scores[self.turning_counter]
        elif enemy.state == "turn":
            enemy.turning_counter += 1
            self.kill(enemy.dir)
            score = settings.scores.turning_scores[enemy.turning_counter]
        else:
            self.turn_back(enemy, object_type="enemy")

        if score == 0:
            return

        custom_events.post_event(event_id=custom_events.EventID.ADD_SCORE, score=score)
        custom_events.post_event(
            event_id=custom_events.EventID.ADD_PARTICLE_SCORE,
            particle_pos=self.rect.topleft,
            score=score,
        )

    def reverse_direction(self):
        """Revese the current direction."""
        if self.state != "hide":
            super().reverse_direction()

    def prevent_falling(self, tiles, current_floor):
        copy_rect = self.rect.copy()

        copy_rect.x += self.dir * self.rect.width
        copy_rect.y += 10

        for tile in tiles.tiles_from_collide_area(current_floor, copy_rect.x):
            if copy_rect.colliderect(tile.rect):
                break
        else:
            self.reverse_direction()

    def to_delete(self, current_floor, world_shift):
        return super().to_delete(current_floor, world_shift) or (
            self.state == "turn" and self.rect.x > -world_shift.x + settings.screen.screen_width
        )
