'''
Функции работающие с файлами.
'''
import json
import pygame

def loadJson(path: str) -> dict:
    '''
    Возвращает словарь соответствующий указанному json-объекту
    '''
    with open(path) as settings_file:
        return json.load(settings_file)


def getSpriteSheet(path:str, size:int=16, scale:float=1):

    spritesheet_image = pygame.transform.scale_by(pygame.image.load(path), scale)
    size *= scale

    spritesheet = {
        "default":spritesheet_image.subsurface((0,0,size,size)),
        "moving":{
            (0,0): [spritesheet_image.subsurface((0,0,size,size)),],
            (0,-1): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (1,-1): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (1,0): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (1,1): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (0,1): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (-1,1): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (-1,0): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
            (-1,-1): [spritesheet_image.subsurface((0,0,size,size)), spritesheet_image.subsurface((size,0,size,size))],
        }
    }

    return spritesheet