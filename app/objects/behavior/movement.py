'''
Модуль содержит функции описывающие движение объектов.
'''
import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../../..")
from tools.math_tools import sign, blockFilter


def standartMovement(sprite: pygame.sprite.Sprite, **kwargs):
    '''
    Принимает:
    - `sprite` - объект для которого реализуется передвижение
    - `kwargs` - дополнительные аргументы:
        - обязательные: аргументы необходимые для контроллера объекта
    
    Реализует передвижение объекта через направление движения определяемое контроллером объекта.
    Имея направление, объект ускоряется с постоянным ускорением `maxacceleration` пока не упирается в препятствие
    или максимальную скорость `maxspeed`. Теряя направление, объект замедляется с тем же ускорением `maxacceleration`.
    Наткнувшись на препятствие объект останавливается и больше не может двигаться в данном направлении,
    поскольку данное направление добавляется в заблокированные направления `move_block` и остается там пока объект упирается в это припятствие.
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

    sprite.speed[0] -= maxacceleration * sign(sprite.speed[0]) * time
    sprite.speed[1] -= maxacceleration * sign(sprite.speed[1]) * time

    if (sprite.speed[0]**2 + sprite.speed[1]**2)**(1/2) > maxspeed:
        sprite.speed[0] = move_direction[0] * maxspeed if not acceleration[1] else move_direction[0] * maxspeed / 2
        sprite.speed[1] = move_direction[1] * maxspeed if not acceleration[0] else move_direction[1] * maxspeed / 2

    sprite.move_block = [0,0]

    pathInterpole(sprite, (sprite.speed[0] * time, sprite.speed[1] * time))

def pathInterpole(sprite: pygame.sprite.Sprite, path):
    '''
    Принимает:
    - `sprite` - объект для которого реализуется передвижение
    - `path` - путь (изменение положения (diffx, diffy)) объекта между двумя кадрами

    Разбивает путь `path` на маленькие отрезки `stepx`/`stepy` и реализует передвижение,
    проверяя столкновения и применяя блокировки `move_block` движения на каждом отрезке.
    '''

    steps_num = int(max(abs(path[0]), abs(path[1]))) + 1
    stepx = path[0] / steps_num
    stepy = path[1] / steps_num

    group = sprite.groups()[0]
    sprite.remove(group)

    for _ in range(steps_num):

        collisions = pygame.sprite.spritecollide(sprite, group, False)

        if collisions:
            collideHandle(sprite, collisions)

        stepx = blockFilter(stepx, sprite.move_block[0])
        stepy = blockFilter(stepy, sprite.move_block[1])

        if stepx or stepy:

            sprite.float_position[0] += stepx
            sprite.float_position[1] += stepy

            sprite.rect.centerx = int(sprite.float_position[0])
            sprite.rect.centery = int(sprite.float_position[1])

        else:

            break

    
    sprite.add(group)

def collideHandle(sprite: pygame.sprite.Sprite, collisions):
    '''
    Принимает:
    - `sprite` - объект для которого определяются блокировки
    - `collisions` - список объектов с которыми он столкнулся

    Определяет направления `move_block` заблокированные для движения.
    Перед использованием заблокированные направления должны быть сброшены.
    '''

    for collided in collisions:

        diffx = (sprite.rect.centerx - collided.rect.centerx) / (sprite.rect.width + collided.rect.width)
        diffy = (sprite.rect.centery - collided.rect.centery) / (sprite.rect.height + collided.rect.height)

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
