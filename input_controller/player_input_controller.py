import pygame
import settings.player
import copy
import time
from typing import Callable

import player

import physics.player

import events


class PlayerInputController:
    def __init__(
        self, physic_component: physics.player.PlayerPhysicComponent, player_status: player.PlayerStats
    ) -> None:
        self.player_stats = player_status
        self.physic_component = physic_component
        self.controls = copy.deepcopy(settings.player.player_controls)
        self.handlers = dict()

        self.last_frame_input_actions = set()
        self.configure_input_controller()

    def configure_input_controller(self) -> None:

        self.subscribe_input_handlers(player.InputActions.duck, self.duck_input_action)
        self.subscribe_input_handlers(player.InputActions.jump, self.jump_input_action)
        self.subscribe_input_handlers(player.InputActions.left, self.left_input_action)
        self.subscribe_input_handlers(player.InputActions.right, self.right_input_action)
        self.subscribe_input_handlers(player.InputActions.sprint, self.sprint_input_action)
        self.subscribe_input_handlers(player.InputActions.pause, self.pause_game_input_action)
        self.subscribe_input_handlers(player.InputActions.slow_game, self.slow_the_game)

    def subscribe_input_handlers(self, input_type: player.InputActions, handler_func: Callable):
        self.handlers[input_type] = handler_func

    def get_inputs(self) -> None:
        pressed_keys = pygame.key.get_pressed()

        for input_type, handler_func in self.handlers.items():
            key_id = self.controls[input_type]

            if pressed_keys[key_id]:
                handler_func()
                self.last_frame_input_actions.add(input_type)
            else:
                if input_type in self.last_frame_input_actions:
                    self.last_frame_input_actions.remove(input_type)

    def duck_input_action(self) -> None:
        """When the down input is pressed.

        Args:
            keys_pressed (list): a list with all pressed keys.
        """
        self.player_stats.set_animation_type(player.MovementTypes.ducking)

    def jump_input_action(self) -> None:
        """When the jump button is pressed.

        Args:
            keys_pressed (list): a list with all pressed keys.
        """

        if player.InputActions.jump in self.last_frame_input_actions:
            self.player_stats.jump_pressed = True
            return

        self.player_stats.set_animation_type(player.MovementTypes.jumping)
        self.player_stats.set_vertical_movement_state(player.MovementTypes.jumping)

    def left_input_action(self) -> None:
        if self.physic_component.velocities.x > 0:
            self.player_stats.set_horizontal_movement_state(player.MovementTypes.skiding)
            self.player_stats.set_animation_type(player.MovementTypes.skiding)
            return

        self.player_stats.set_horizontal_movement_state(player.MovementTypes.walking)
        self.player_stats.set_animation_type(player.MovementTypes.walking)
        self.physic_component.directions.x = -1

    def right_input_action(self) -> None:
        if self.physic_component.velocities.x < 0:
            self.player_stats.set_horizontal_movement_state(player.MovementTypes.skiding)
            self.player_stats.set_animation_type(player.MovementTypes.skiding)
            return

        self.player_stats.set_horizontal_movement_state(player.MovementTypes.walking)
        self.player_stats.set_animation_type(player.MovementTypes.walking)
        self.physic_component.directions.x = 1

    def sprint_input_action(self) -> None:
        self.player_stats.set_animation_type(player.MovementTypes.skiding)
        self.player_stats.set_horizontal_movement_state(player.MovementTypes.running)
        self.player_stats.sprint_counter.start()

    def pause_game_input_action(self) -> None:
        if player.InputActions.pause in self.last_frame_input_actions:
            return

        events.post_event(event_id=events.EventID.PAUSE_GAME)

    def slow_the_game(self) -> None:
        events.post_event(event_id=events.EventID.SUBSTRACT_SLEEP_FROM_DT, time=0.5)
        time.sleep(0.5)
