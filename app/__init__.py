'''
Корень приложения.
'''
import pygame
import os
from tools.load_tools import loadJson
from objects.sprites import Entity, Sprite, Group, getSpriteSheet
from objects.behavior.controllers import gameKeyController, appKeyController, gameRandController
from random import randint

settings = loadJson(os.path.abspath(__file__) + "/../data/settings.json") # словарь содержащий текущие настройки

window = pygame.display.set_mode(settings["window"]["resolution"]) # главная поверхность
pygame.display.set_caption(settings["window"]["caption"]) # установка загаловка окна
resolution_modes = pygame.display.list_modes() # список доступных разрешений

# ingame_surface = pygame.Surface((5000,5000))
# cropped_ingame_surface = pygame.Surface(settings["window"]["resolution"])
# ingame_surface = SuperSurface((3000, 3000))
# main_surface = GroupSingle(ingame_surface)

clock = pygame.time.Clock() # объект pygame для отслеживания времени
fps = settings["window"]["fps"] # ограничение fps

run = True # переключатель работы приложения

scale = 1.0 # значение приближения

observer = None # объект за которым следит камера
main_surface = pygame.surface.Surface((1100,1100))


# дальше инициализация конкретного уровня
# TEST.entities

entities = Group()
moving_entities = Group()

border_horizontal_texture = pygame.Surface((1000, 50))
border_vertical_texture = pygame.Surface((50, 1000))
border_horizontal_texture.fill((255,255,255))
border_vertical_texture.fill((255,255,255))

border_top = Sprite((50, 0), clock, None, None, border_horizontal_texture, entities)
border_bottom = Sprite((50, 1000 + 50), clock, None, None, border_horizontal_texture, entities)
border_left = Sprite((0, 50), clock, None, None, border_vertical_texture, entities)
border_right = Sprite((1000 + 50, 50), clock, None, None, border_vertical_texture, entities)

player_spritesheet = getSpriteSheet(os.path.abspath(__file__) + "/../static/textures/spritesheets/spritesheet_man.png", scale=2)
obstacle_texture = pygame.Surface((randint(5, 200), randint(5, 200)))
obstacle_texture.fill((255,255,255))

player = Entity((randint(50, 950), randint(50, 950)),
                clock,
                gameKeyController,
                pygame.Rect(4,0,24,32),
                player_spritesheet,
                None,
                entities, moving_entities,
                maxacceleration=500,
                maxspeed=500)

for _ in range(10):
    creature = Entity((randint(50, 950), randint(50, 950)),
                      clock,
                      gameRandController,
                      pygame.Rect(4,0,24,32),
                      player_spritesheet,
                      None,
                      entities, moving_entities,
                      maxacceleration=200,
                      maxspeed=100)

obstacle = Sprite((randint(25, settings["window"]["resolution"][0] - 25), randint(25, settings["window"]["resolution"][1] - 25)),
                  clock,
                  None,
                  None,
                  obstacle_texture,
                  entities)

observer = player

# TEST.DEBUG_PANEL

pygame.font.init()
font = pygame.font.Font(None, 24)