'''
Модуль содержит функции описывающие движение объектов.
'''
import pygame
import math
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../..")
from tools.math_tools import sign, blockFilter, absMax


def calculatePath(sprite: pygame.sprite.Sprite, **kwargs):

    # Извлечение необходимых аттрибутов из объекта
    maxacceleration = sprite.kwattrs["maxacceleration"]
    maxspeed = sprite.kwattrs["maxspeed"]

    # Получение направления движения от контроллера объекта
    move_direction = sprite.controller(**(kwargs | {"sprite": sprite}))

    # Вычисление скорости на текущем тике
    time = sprite._clock.get_time() * 0.001

    acceleration = [maxacceleration * move_direction[0],
                    maxacceleration * move_direction[1]]
    
    sprite.speed[0] += acceleration[0] * 2 * time
    sprite.speed[1] += acceleration[1] * 2 * time

    decreasespeed = maxacceleration * sign(sprite.speed[0]) * time, maxacceleration * sign(sprite.speed[1]) * time

    sprite.speed[0] -= decreasespeed[0] if abs(sprite.speed[0]) >= abs(decreasespeed[0]) else sprite.speed[0]
    sprite.speed[1] -= decreasespeed[1] if abs(sprite.speed[1]) >= abs(decreasespeed[1]) else sprite.speed[1]

    if (sprite.speed[0]**2 + sprite.speed[1]**2)**(1/2) > maxspeed:
        sprite.speed[0] = move_direction[0] * maxspeed if not acceleration[1] else move_direction[0] * maxspeed / 2
        sprite.speed[1] = move_direction[1] * maxspeed if not acceleration[0] else move_direction[1] * maxspeed / 2

    sprite.path = [sprite.speed[0] * time, sprite.speed[1] * time]

    sprite.animation("moving", tuple(move_direction))

    return sprite.path


def calculateEntitiesPaths(**kwargs):
    '''
    Принимает:
    - `group` - группа сущностей для которых вычисляются пути (смещения между текущим и следующим кадром)
    - `kwargs` - дополнительные аргументы

    Вычисляет путь для каждой сущности из группы. Возвращает список всех компонентов (горизонатльный/вертикальный путь)
    всех вычесленных путей.
    '''

    moving_entities = kwargs["moving_entities"]
    paths = []

    for sprite in moving_entities.sprites():
        paths += calculatePath(sprite, **kwargs)

    return paths


def standartMovement(entities: pygame.sprite.Group,
                     **kwargs):
    

    moving_entities = kwargs["moving_entities"]

    steps_num = math.ceil(absMax(calculateEntitiesPaths(**kwargs)))

    if not steps_num: return 0

    steps = {}
    for entity in moving_entities:
        steps.update({entity: [entity.path[0] / steps_num, entity.path[1] / steps_num]})
    

    for _ in range(steps_num):

        for entity in moving_entities:

            entity.remove(entities)
            entity.move_block = [0,0]

            collisions = pygame.sprite.spritecollide(entity, entities, False)
            if collisions:
                collideHandle(entity, collisions)

            entity.float_position[0] += blockFilter(steps[entity][0], entity.move_block[0])
            entity.float_position[1] += blockFilter(steps[entity][1], entity.move_block[1])

            entity.rect.centerx = int(entity.float_position[0])
            entity.rect.centery = int(entity.float_position[1])

            entity.add(entities)
            

def collideHandle(sprite: pygame.sprite.Sprite, collisions):
    '''
    Принимает:
    - `sprite` - объект для которого определяются блокировки
    - `collisions` - список объектов с которыми он столкнулся

    Определяет направления `move_block` заблокированные для движения.
    Перед использованием заблокированные направления должны быть сброшены.
    '''

    for collided in collisions:

        diffx = (sprite.rect.centerx - collided.rect.centerx) / max(sprite.rect.width, collided.rect.width)
        diffy = (sprite.rect.centery - collided.rect.centery) / max(sprite.rect.height, collided.rect.height)

        if abs(diffx) > abs(diffy):
            if diffx < 0: 
                sprite.move_block[0] += 2
            else:
                sprite.move_block[0] += 1
        elif abs(diffy) > abs(diffx):
            if diffy < 0: 
                sprite.move_block[1] += 2
            else:
                sprite.move_block[1] += 1
        else:
            if diffx > 0:
                sprite.move_block[0] += 1
                if diffy > 0:
                    sprite.move_block[1] += 1
                else:
                    sprite.move_block[1] += 2
            else:
                sprite.move_block[0] += 2
                if diffy > 0:
                    sprite.move_block[1] += 1
                else:
                    sprite.move_block[1] += 2
