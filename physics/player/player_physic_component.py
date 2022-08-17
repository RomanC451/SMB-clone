import math
import pygame

import physics


import player
from .player_horizontal_velocities import PlayerHorizontalVelocitiesGroup
from .player_vertical_velocities import PlayerVerticalVelocitiesGroup
from .collisions import PlayerCollisionComponent

import tiles

import events
import utils.math


import settings.game

if settings.game.game_type == "client":
    import debug


class PlayerPhysicComponent:

    __slots__ = [
        "player_stats",
        "horizontal_velocities_group",
        "vertical_velocities_group",
        "rect",
        "trajectory_rect",
        "accelerations",
        "velocities",
        "previous_velocities",
        "directions",
        "vertical_velocity_class",
        "collision_component",
        "dt_acumulator",
    ]

    def __init__(self, image: pygame.Surface, player_stats: player.PlayerStats) -> None:

        self.player_stats = player_stats

        self.horizontal_velocities_group = PlayerHorizontalVelocitiesGroup()
        self.vertical_velocities_group = PlayerVerticalVelocitiesGroup()
        self.rect = physics.FloatRect.rect_from_img(image)
        self.trajectory_rect = physics.FloatRect([0] * 4)
        self.accelerations = physics.FloatVector2()
        self.velocities = physics.FloatVector2()
        self.directions = pygame.Vector2(1, 0)
        self.vertical_velocity_class = None

        self.dt_acumulator = 0

        self.collision_component = PlayerCollisionComponent(
            self.player_stats, self.rect, self.velocities, self.directions
        )

        debug.max_delta_times.set_categoryes(["vertical", "horizontal"])

    def update(self, delta_time: float, tiles_group: tiles.TilesGroup):

        self.dt_acumulator += delta_time

        while self.dt_acumulator >= settings.game.fixed_dt:

            self._update(settings.game.fixed_dt, tiles_group)

            self.dt_acumulator -= settings.game.fixed_dt

        self.print_debug_info()

    def _update(self, delta_time: float, tiles_group: tiles.TilesGroup) -> None:
        self.trajectory_rect.copy_data_from_rect(self.rect)

        self.limit_vertical_velocity()
        self.update_vertical_position(delta_time)
        self.collision_component.check_vertical_collision(self.trajectory_rect, tiles_group)

        self.update_vertical_acceleration()
        self.update_vertical_velocity(delta_time)

        self.trajectory_rect.copy_data_from_rect(self.rect)

        self.limit_horizontal_velocity()
        self.update_horizontal_position(delta_time)
        self.collision_component.check_horizontal_collision(self.trajectory_rect, tiles_group)
        self.update_horizontal_acceleration()
        self.udpate_horizontal_velocity(delta_time)

        self.check_deltatimes()

    # ---> vertical movement
    # @debug.check_max_dt("vertical")
    def update_vertical_acceleration(self) -> None:
        self.vertical_velocity_class = self.vertical_velocities_group.get_jumping_velocity_class(abs(self.velocities.x))

        if self.player_stats.jump_pressed:
            # if jump is pressed, the vertical velocity will decrease slower
            self.accelerations.y = -self.vertical_velocity_class.gravity_jumping

        else:

            self.accelerations.y = -self.vertical_velocity_class.gravity_no_jumping

    # @debug.check_max_dt("vertical")
    def update_vertical_velocity(self, delta_time: float):
        """Decide the celocity class, based on horizontal velocity."""

        if self.player_stats.vertical_movement_state is player.MovementTypes.jumping and self.velocities.y == 0:
            # if player is not in air, set the initial jumping velocity
            self.velocities.y = self.vertical_velocity_class.jumping_velocity
            self.rect.max_y = 1000

        self.velocities.y += self.accelerations.y * delta_time

    # @debug.check_max_dt("vertical")
    def limit_vertical_velocity(self) -> None:

        if self.velocities.y < -self.vertical_velocities_group.max_vertical_velocity:
            self.velocities.y = -self.vertical_velocities_group.max_vertical_velocity

    # @debug.check_max_dt("vertical")
    def update_vertical_position(self, delta_time: float) -> None:
        distance = self.velocities.y * delta_time + 0.5 * self.accelerations.y * math.pow(delta_time, 2)

        self.calc_vertical_trayectory(distance)
        self.rect.float_y -= distance

        if self.rect.max_y > self.rect.float_y:
            self.rect.max_y = self.rect.float_y

        self.rect.sync_int_coords()

    # @debug.check_max_dt("vertical")
    def calc_vertical_trayectory(self, distance: float) -> None:

        if distance > 0:
            self.trajectory_rect.float_y -= distance

        self.trajectory_rect.sync_int_coords()

        self.trajectory_rect.float_height = self.rect.height + abs(distance)
        self.trajectory_rect.sync_int_sizes()

    # ---> horizontal movement

    # @debug.check_max_dt("horizontal")
    def update_horizontal_acceleration(self) -> None:
        if self.player_stats.horizontal_movement_state is player.MovementTypes.standing:
            if self.velocities.x != 0:
                self.accelerations.x = -self.horizontal_velocities_group.decelerations_dict["release"]
            else:
                self.accelerations.x = 0
            return

        elif self.player_stats.horizontal_movement_state is player.MovementTypes.skiding:
            self.accelerations.x = -self.horizontal_velocities_group.decelerations_dict["skiding"]
            return

        self.accelerations.x = self.horizontal_velocities_group.accelerations_dict[
            self.player_stats.horizontal_movement_state
        ]

    # @debug.check_max_dt("horizontal")
    def udpate_horizontal_velocity(self, delta_time: float):

        """Update the horizontal velocity."""

        if self.velocities.x == 0 and self.player_stats.horizontal_movement_state in (
            player.MovementTypes.running,
            player.MovementTypes.walking,
        ):
            # If player is standing set the minimum velocity
            self.velocities.x = self.directions.x * self.horizontal_velocities_group.min_vel * delta_time
            return

        new_x_vel = self.velocities.x + self.directions.x * self.accelerations.x * delta_time

        if (
            utils.math.opposite_signs(new_x_vel, self.velocities.x)
            and self.player_stats.horizontal_movement_state is player.MovementTypes.standing
        ):
            new_x_vel = 0

        if (
            self.player_stats.horizontal_movement_state is player.MovementTypes.skiding
            and abs(new_x_vel) <= self.horizontal_velocities_group.skid_vel
        ):
            new_x_vel *= -1
            self.directions.x *= -1

        self.velocities.x = new_x_vel

    # @debug.check_max_dt("horizontal")
    def limit_horizontal_velocity(self) -> None:
        if self.player_stats.horizontal_movement_state in (
            player.MovementTypes.standing,
            player.MovementTypes.skiding,
        ):
            return

        if (
            abs(self.velocities.x)
            > self.horizontal_velocities_group.max_vel_dict[self.player_stats.horizontal_movement_state]
        ):
            self.velocities.x = (
                self.directions.x
                * self.horizontal_velocities_group.max_vel_dict[self.player_stats.horizontal_movement_state]
            )

    # @debug.check_max_dt("horizontal")
    def update_horizontal_position(self, delta_time: float) -> None:
        distance = self.velocities.x * delta_time + 0.5 * self.accelerations.x * math.pow(delta_time, 2)
        if not distance:
            return

        self.calc_horizontal_trayectory(distance)
        self.rect.float_x += distance

        self.rect.sync_int_coords()

    # @debug.check_max_dt("horizontal")
    def calc_horizontal_trayectory(self, distance: float) -> None:

        if distance < 0:
            self.trajectory_rect.float_x -= distance
        self.trajectory_rect.sync_int_coords()

        self.trajectory_rect.float_width = self.rect.width + abs(distance)
        self.trajectory_rect.sync_int_sizes()

    def print_debug_info(self) -> None:
        debug_text = f"Player: velocities: {self.velocities.x, self.velocities.y }\n\
            derections: {self.directions.x, self.directions.y}\n\
            float_pos:{None,None}\n\
            int_pos:{self.rect.x, self.rect.y}\n\
            max_y: {self.rect.max_y}\n\
            normal_rect: {self.rect.topleft, self.rect .size }\n\
            trajectory_rect: {self.trajectory_rect.topleft, self.trajectory_rect.size }\n\
            time_passed: vertical: total_decor: {debug.max_delta_times.get_categ_total_dt('vertical')}\n\
                                        {debug.max_delta_times.get_categoty_dict('vertical')},\n\
                         horizontal: total_decor: {debug.max_delta_times.get_categ_total_dt('horizontal')} \n\
                                        {debug.max_delta_times.get_categoty_dict('horizontal')}"

        events.post_event(events.EventID.PRINT_CONSOLE_TEXT, text=debug_text)

    def check_deltatimes(self):
        if (dt := debug.max_delta_times.get_categ_total_dt("vertical")) > 0.017:
            print(f"Warning: vertical movement was done too slow: {dt}")
            debug.max_delta_times.reset_categ("vertical")

        if (dt := debug.max_delta_times.get_categ_total_dt("horizontal")) > 0.017:
            print(f"Warning: horizontal movement was done too slow: {dt}")
            debug.max_delta_times.reset_categ("horizontal")
