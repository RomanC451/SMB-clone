from enemies import Enemy
import import_assets
import events.custom_events as custom_events
import sound.sound
import sound.channels

import settings.screen
import settings.enemies
import settings.scores


surfaces = import_assets.get_surfaces(folder="enemies", object_type="goomba")


class Goomba(Enemy):
    """Goomba enemy type class.

    Args:
        Enemy (class): Inheritance
    """

    def __init__(self, world_type, pos):
        self.images_dict = surfaces[world_type]
        super().__init__(
            "goomba",
            world_type,
            self.images_dict["move"][0],
            (pos[0], pos[1] - 1 * settings.enemies.pixel_multiplicator),
        )

        self.state = "move"
        self.frames = {"disappear_frame": 0}

    def update(self, tiles, current_floor, world_shift, enemies_group):
        """The main update function of Goomba class.

        Args:
            tiles (SritesGroup): The group with all tiles
            current_floor (Str): The current floor of the level
            world_shift (int): The offset of the map
            enemies_group (SpritesGrouo): The group with all enemies
        """

        if self.state == "move":
            super().update(tiles, current_floor, world_shift, enemies_group)
        elif self.state == "dead":
            self.dead_update()
        elif self.state == "stomped":
            self.frames["disappear_frame"] += settings.enemies.enemies_animation_settings["goomba"]["disappear_time"]
            if self.frames["disappear_frame"] >= 1:
                self.killed = True

    def activate(self, cause, dir, stomping_counter):
        """Activate function triggerd when the enemy gets hit from above.

        Args:
            cause (Str): Who called thi method.
            dir (int): Direction in case of animation
        """
        if cause == "player":
            custom_events.post_event(
                event_id=custom_events.EventID.ADD_SCORE, score=settings.scores.stomping_scores[stomping_counter]
            )
            custom_events.post_event(
                event_id=custom_events.EventID.ADD_PARTICLE_SCORE,
                particle_pos=self.rect.topleft,
                score=settings.scores.stomping_scores[stomping_counter],
            )
            sound.sound.play_sound(channel=sound.channels.ChannelsID.enemies, sound_name="stomp")
            self.velocities.x = 0
            self.state = "stomped"
            self.image = self.images_dict[self.state]

    def enemy_horizontal_collision_handling(self, enemy):
        """Handle thehorizontal collision with an enemy.

        Args:
            enemy (enemy): The colliding enemy.
        """
        if enemy.state == "turn":
            enemy.turning_counter += 1
            custom_events.post_event(
                event_id=custom_events.EventID.ADD_SCORE, score=settings.scores.turning_scores[enemy.turning_counter]
            )
            custom_events.post_event(
                event_id=custom_events.EventID.ADD_PARTICLE_SCORE,
                particle_pos=self.rect.topleft,
                score=settings.scores.turning_scores[enemy.turning_counter],
            )
            self.kill(enemy.dir)
        else:

            self.turn_back(enemy, object_type="enemy")
