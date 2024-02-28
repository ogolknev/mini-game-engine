import pygame
import tools.load_tools as load_tools
from objects.sprites import testSprite, Sprite, Group

from random import randint

SCALE = 1.0

settings = load_tools.loadJson("data/settings.json") # словарь содержащий текущие настройки

window = pygame.display.set_mode(settings["window"]["resolution"]) # главная поверхность
pygame.display.set_caption(settings["window"]["caption"])
resolution_modes = pygame.display.list_modes() # список доступных разрешений

clock = pygame.time.Clock() # объект pygame для отслеживания времени

run = True # индикатор работы

observer = None

# TEST.SPRITES

sprites = Group()
test_group = Group()

test_sprite_texture = pygame.Surface((70,50))
test_sprite_texture2 = pygame.Surface((30,60))
test_sprite_texture.fill((255,255,255))
test_sprite_texture2.fill((255,255,255))

border_horizontal_texture = pygame.Surface((settings["window"]["resolution"][0], 50))
border_vertical_texture = pygame.Surface((50, settings["window"]["resolution"][1]))
border_horizontal_texture.fill((255,255,255))
border_vertical_texture.fill((255,255,255))

border_top = Sprite(border_horizontal_texture, (settings["window"]["resolution"][0] // 2, 0), sprites)
border_bottom = Sprite(border_horizontal_texture, (settings["window"]["resolution"][0] // 2, settings["window"]["resolution"][1]), sprites)
border_left = Sprite(border_vertical_texture, (0, settings["window"]["resolution"][1] // 2), sprites)
border_right = Sprite(border_vertical_texture, (settings["window"]["resolution"][0], settings["window"]["resolution"][1] // 2), sprites)

test_sprite = testSprite(test_sprite_texture,
                         (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                         sprites, test_group,
                         maxacceleration=5000,
                         maxspeed=700)

test_sprite2 = Sprite(test_sprite_texture2,
                      (randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                      sprites)

observer = test_sprite

# TEST.DEBUG_PANEL

pygame.font.init()
font = pygame.font.Font(None, 24)