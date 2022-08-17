import time

import events


class FpsManager:

    __slots__ = ["previous_time", "display_fps", "sleep_time"]

    def __init__(self, display_fps: bool = False) -> None:

        self.display_fps = display_fps
        self.sleep_time = 0

        events.subscribe_event(
            event_id=events.EventID.SUBSTRACT_SLEEP_FROM_DT.value, handler_function=self.substract_sleep
        )

    def start(self) -> None:
        self.previous_time = time.time()

    def substract_sleep(self, time: float) -> None:
        pass
        # self.sleep_time = time

    def get_delta_time(self) -> float:
        dt = time.time() - self.previous_time
        self.previous_time = time.time()
        if dt == 0:
            dt = 0.017
        # elif dt > 0.47:
        #     dt = dt - 0.5

        if dt < 0:
            pass
        if self.display_fps:

            fps = int(1 / dt)
            events.post_event(events.EventID.PRINT_CONSOLE_TEXT, text=f"FPS(time): {fps}")
            events.post_event(events.EventID.PRINT_CONSOLE_TEXT, text=f"DT(time): {dt}")
        # if self.sleep_time:
        #     1)

        # self.sleep_time = 0
        # dt = 0.0090

        return dt  # / 0.017
