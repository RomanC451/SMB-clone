import pygame
import copy

import events
import graphics

import utils.counters.time_counters
import utils.fonts


console_font_size = 16


class Console:

    __slots__ = ["drawing_manager", "printed_lines", "new_lines", "time_counter", "max_width", "lines_number"]

    def __init__(self, drawing_manager: graphics.DrawingManager) -> None:
        self.drawing_manager = drawing_manager
        self.printed_lines = list()
        self.new_lines = list()

        self.time_counter = utils.counters.time_counters.TimeCounter(
            seconds=0.5, handler_funct=self.update_console_text
        )
        self.max_width = 0
        self.lines_number = 0

        events.subscribe_event(events.EventID.PRINT_CONSOLE_TEXT.value, handler_function=self.print_text)

    def print_text(self, text: str) -> None:

        self.new_lines.extend(text.splitlines())

        if len(self.new_lines) > 14:
            pass

    def update(self, dt: float):

        self.time_counter.count(dt)
        # self.update_console_text()
        self.print_console_background()
        self.display_console()
        self.new_lines.clear()

    def update_console_text(self):
        self.printed_lines = copy.copy(self.new_lines)
        self.max_width = len(max(self.printed_lines, key=len)) * console_font_size
        self.lines_number = len(self.printed_lines)

    def print_console_background(self) -> None:
        background_surf = pygame.Surface((self.max_width + 40, self.lines_number * (console_font_size + 10) + 10))
        background_surf.set_alpha(200)
        background_surf.fill(graphics.Colors.WHYTE.value)
        self.drawing_manager.draw_surface_statically(background_surf, (0, 0))

    def display_console(self) -> None:
        y_coord = 5

        for line in self.printed_lines:
            text_surface = utils.fonts.render_text(line, size=console_font_size)
            self.drawing_manager.draw_surface_statically(text_surface, (20, y_coord))
            y_coord += console_font_size + 10
