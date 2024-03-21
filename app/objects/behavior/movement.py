'''
Модуль содержит функции описывающие движение объектов.
'''
import pygame
import math
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../..")
from tools.math_tools import sign, signFilter, absMax


def calculatePath(sprite: pygame.sprite.Sprite, **kwargs):
    '''
    !!! ФУНКЦИЮ НЕОБХОДИМО ПЕРЕПИСАТЬ !!! (Разделить на более мелкие и абстрактные функции)

    Расчитывает путь объекта, который он попытается пройти за 1 кадр и обновляет атрибут `sprite.path`.
    Расчитывает скорость в начале текущего кадра и обновляет `sprite.speed`. Вызывает метод анимации спрайта.

    Принимает:
    - `sprite` - объект для которого выполняются расчеты и вызывается метод анимации
    - `kwargs` - кей-ворд параметры передаваемые контроллеру объекта

    Возвращает:
    - `sprite.path` - путь объекта, который он попытается пройти за 1 кадр
    '''

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

    sprite.animation(20, "moving", tuple(move_direction))

    return sprite.path


def calculateEntitiesPaths(moving_entities: pygame.sprite.Group, **kwargs):
    '''
    Вычисляет путь для каждой сущности из группы. Возвращает список всех компонентов (горизонатльный/вертикальный путь)
    всех вычесленных путей.

    Принимает:
    - `moving_entities` - группа сущностей для которых вычисляются пути (смещения между текущим и следующим кадром)
    - `kwargs` - дополнительные параметры нужные для calculatePath()

    Возвращает:
    - `paths` - список всех компонентов (горизонатльный/вертикальный путь) всех вычесленных путей
    '''

    paths = []

    for sprite in moving_entities.sprites():
        paths += calculatePath(sprite, **kwargs)

    return paths


def standartMovement(entities: pygame.sprite.Group, moving_entities: pygame.sprite.Group, **kwargs):
    '''
    Основная функция реализующая движение объектов через их контроллеры и максимальную скорость/ускорение.

    Суть текущей реализации: Вычисляются пути всех объектов. Они делятся на одинаковое колличество шагов такое,
    что максимальный шаг объекта был не больше 1 пикселя (при scale=1.0). Потом путь проходится всеми объектами пошагово,
    проверяя столкновения на каждом шаге.
    
    Принимает:
    - `entities` - группа (pygame.sprite.Group) объектов для которой реализуется движение
    - `moving_entities` - группа (pygame.sprite.Group) объектов способных двигаться
    - `kwargs` - кей-ворд параметры для calculateEntitiesPaths()
    '''

    steps_num = math.ceil(absMax(calculateEntitiesPaths(moving_entities, **kwargs)))

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

            entity.float_position[0] += signFilter(steps[entity][0], entity.move_block[0])
            entity.float_position[1] += signFilter(steps[entity][1], entity.move_block[1])

            entity.rect.centerx = int(entity.float_position[0])
            entity.rect.centery = int(entity.float_position[1])

            entity.add(entities)
            

def collideHandle(sprite: pygame.sprite.Sprite, collisions):
    '''
    !!! ДОПИСАТЬ !!! `diff` определяется неверно
    
    Определяет направления заблокированные для движения `move_block`. Обновляет `sprite.move_block`.
    Перед использованием заблокированные направления должны быть сброшены (move_block = [0,0]).
    
    Принимает:
    - `sprite` - объект для которого определяются блокировки
    - `collisions` - список объектов с которыми он столкнулся
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
