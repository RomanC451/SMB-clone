import physics
import utils.counters.frame_counters
import settings.player
from .player_enums import MovementTypes, DefaultAnimationCategories, PlayerStates


class PlayerStats:
    def __init__(self):

        self.state = PlayerStates.little

        self.animation_category = DefaultAnimationCategories.normal
        self.animation_type = MovementTypes.standing

        self.horizontal_movement_state = MovementTypes.standing
        self.vertical_movement_state = MovementTypes.standing

        self.stomping_counter = 0
        self.invincible = False
        self.invisible = False
        self.imune_to_damage = False
        self.jump_pressed = False

        self.animation_stack = ["normal"]

        self.config_counters()

    def config_counters(self) -> None:
        self.sprint_counter = utils.counters.frame_counters.OneWayCounter(
            max_value=settings.player.player_frames["running_reset"],
            reach_max_value_handler=self.reset_horizontal_movement_state,
            looping=False,
        )
        self.imune_to_damage_counter = utils.counters.frame_counters.OneWayCounter(
            max_value=settings.player.player_frames["imune_to_damage"],
            reach_max_value_handler=self.reset_imune_to_damage_flag,
            looping=False,
        )

    def reset(self):
        self.animation_type = MovementTypes.standing
        self.jump_pressed = False
        self.reset_horizontal_movement_state()
        self.reset_vertical_movement_state()
        self.sprint_counter.count()

    def set_animation_type(self, movement_type: MovementTypes) -> None:
        if movement_type is MovementTypes.ducking and (
            self.animation_category == DefaultAnimationCategories.firing
            or self.horizontal_movement_state != MovementTypes.standing
            or self.state == PlayerStates.little
        ):
            return

        self.movement_type = movement_type

    def set_horizontal_movement_state(self, horizontal_movement_state: MovementTypes) -> None:
        if (
            horizontal_movement_state in (MovementTypes.walking, MovementTypes.standing)
            and self.horizontal_movement_state is MovementTypes.running
        ) or (
            horizontal_movement_state is MovementTypes.running
            and self.horizontal_movement_state is not MovementTypes.walking
        ):
            return

        self.horizontal_movement_state = horizontal_movement_state

    def set_vertical_movement_state(self, vertical_movement_state: MovementTypes) -> None:

        self.vertical_movement_state = vertical_movement_state

    def reset_horizontal_movement_state(self) -> None:
        self.horizontal_movement_state = MovementTypes.standing

    def reset_vertical_movement_state(self) -> None:
        self.vertical_movement_state = MovementTypes.standing

    def reset_imune_to_damage_flag(self) -> None:
        self.imune_to_damage = False
