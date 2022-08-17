from xml.dom import NotFoundErr
import pygame
import inspect
import traceback
from enum import Enum, auto
from typing import List, Dict, Callable


class AutoID(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count, last_values: List) -> int:
        for last_value in reversed(last_values):
            try:
                return last_value + 1
            except TypeError:
                pass
        return pygame.USEREVENT + 1


class EventID(AutoID):
    # game events
    START_GAME = auto()
    PAUSE_GAME = auto()

    # hud events
    ADD_COIN = auto()
    ADD_SCORE = auto()

    # level events
    PAUSE_RUNNING_LEVEL = auto()
    UNPAUSE_RUNNING_LEVEL = auto()
    CHANGE_MUSIC = auto()
    CHANGE_FLOOR = auto()
    NEXT_LEVEL = auto()

    # cutscenes events
    STAGE_CLEAR = auto()
    START_COUNTING_SCORE = auto()
    CASTEL_ANIMATION = auto()
    DESTROY_BRIDGE = auto()

    # projectiles events
    SPAWN_BOWSER_FIRE = auto()

    # particles events
    ADD_PARTICLE = auto()
    ADD_PARTICLE_SCORE = auto()

    # items events
    CREATE_ITEM = auto()

    # debug
    PRINT_CONSOLE_TEXT = auto()
    SUBSTRACT_SLEEP_FROM_DT = auto()


subscribed_events = {}

handlers_args = dict()


def subscribe_event(event_id: int, handler_function: Callable):
    subscribed_events[event_id] = handler_function
    handler_args = inspect.getfullargspec(handler_function).args
    if "self" in handler_args:
        handler_args.remove("self")
    handlers_args[event_id] = handler_args


def post_event(event_id: EventID, **kwargs: Dict):

    check_event_agrs(event_id=event_id, kwargs=kwargs)
    event = pygame.event.Event(event_id.value, **kwargs)

    pygame.event.post(event)


def check_event_agrs(event_id: EventID, kwargs: Dict):
    correct_args = handlers_args[event_id.value]
    given_args = kwargs
    if correct_args == given_args:
        return

    missing_args = set(correct_args) - set(given_args)
    if missing_args:
        print(f"Missing arguments for event {event_id} : {missing_args} \n{traceback.format_exc()}")

    unknown_args = set(given_args) - set(correct_args)
    if unknown_args:
        print(f"Unkown arguments for event {event_id} : {unknown_args} \n{traceback.format_exc()}")


def check_event(event: pygame.event.Event):
    if event.type in subscribed_events:
        args = [arg for _, arg in event.dict.items()]
        subscribed_events[event.type](*args)
