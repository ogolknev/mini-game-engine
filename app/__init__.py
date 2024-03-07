'''
Корень приложения.
'''
import pygame
import os
from tools.load_tools import loadJson
from objects.sprites import Entity, Sprite, Group
from objects.behavior.controllers import gameKeyController, appKeyController, gameRandController
from random import randint

settings = loadJson(os.path.abspath(__file__) + "/../data/settings.json") # словарь содержащий текущие настройки

window = pygame.display.set_mode(settings["window"]["resolution"]) # главная поверхность
pygame.display.set_caption(settings["window"]["caption"])
resolution_modes = pygame.display.list_modes() # список доступных разрешений

clock = pygame.time.Clock() # объект pygame для отслеживания времени
fps = settings["window"]["fps"]

run = True # индикатор работы

scale = 1.0

observer = None

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

player_spritesheet_image = pygame.image.load(os.path.abspath(__file__) + "/../static/textures/spritesheets/spritesheet_man.png")
player_spritesheet = {
    "default": player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)),
    "moving": {
        (0,0): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)),),
        (0,-1): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (1,-1): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (1,0): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (1,1): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (0,1): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (-1,1): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (-1,0): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
        (-1,-1): (player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16)), player_spritesheet_image.subsurface(pygame.Rect(16,0,16,16))),
    }
}
player_texture = player_spritesheet_image.subsurface(pygame.Rect(0,0,16,16))
obstacle_texture = pygame.Surface((randint(5, 200), randint(5, 200)))
obstacle_texture.fill((255,255,255))

player = Entity((randint(50, 950), randint(50, 950)),
                clock,
                gameKeyController,
                pygame.Rect(2,0,12,16),
                player_spritesheet,
                None,
                entities, moving_entities,
                maxacceleration=5000,
                maxspeed=500)

for _ in range(10):
    creature = Entity((randint(50, 950), randint(50, 950)),
                      clock,
                      gameRandController,
                      pygame.Rect(2,0,12,16),
                      player_spritesheet,
                      None,
                      entities, moving_entities,
                      maxacceleration=3000,
                      maxspeed=200,
                      func=print)

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