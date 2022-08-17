import pygame
from typing import Tuple

fonts: dict[Tuple[str, int] : pygame.font.SysFont] = {("Arial", 24): pygame.font.SysFont("Arial", 24)}


def create_font(font: str, size: int) -> None:
    "Creates different fonts with one list"
    fonts[(font, size)] = pygame.font.SysFont(font, size)


def render_text(text: str, color: str = "black", font: str = "Arial", size: int = 24) -> pygame.Surface:
    if (font, size) not in fonts:
        create_font(font, size)

    return fonts[(font, size)].render(text, False, color)
