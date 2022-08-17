import pygame

import utils.import_assets

import settings.screen
import settings.game


pygame.init()

display = pygame.display.set_mode(
    (settings.screen.screen_width, settings.screen.screen_height), flags=pygame.SCALED, vsync=1
)


utils.import_assets.import_surfaces()
utils.import_assets.import_sounds()
utils.import_assets.import_music()


settings.game.game_type = "client"


pygame.mixer.init()
