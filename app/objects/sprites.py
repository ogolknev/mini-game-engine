import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from objects.behavior.movement import standartMovement


class Group(pygame.sprite.Group):

    def __init__(self, *sprites) -> None:

        super().__init__(*sprites)


    def _setObserver(self, rect, observer, resolution):
        rect.centerx -= int(observer.float_position[0]) - resolution[0] // 2
        rect.centery -= int(observer.float_position[1]) - resolution[1] // 2
        return rect


    def draw(self, surface, bgsurf=None, special_flags=0, **kwargs):

        observer = kwargs["observer"]
        resolution = kwargs["settings"]["window"]["resolution"]

        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (spr.image, self._setObserver(spr.rect.copy(), observer, resolution), None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                
                self.spritedict[spr] = surface.blit(
                    spr.image, self._setObserver(spr.rect.copy(), observer, resolution), None, special_flags
                )

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

class Sprite(pygame.sprite.Sprite):

    def __init__(self, texture: pygame.Surface, position: tuple, *groups) -> None:

        super().__init__(*groups)

        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.float_position = list(position)

        self._clock = pygame.time.Clock()
        self._lifetime = 0


    def update(self, *args, **kwargs):
        pass

class testSprite(Sprite):

    def __init__(self, texture: pygame.Surface, position: tuple, *groups, **kwargs) -> None:

        super().__init__(texture, position, *groups)

        self.speed = [0,0]
        self.move_block = [0,0]

        self.kwattrs = kwargs

    def update(self, *args, **kwargs):

        self._clock.tick()
        self._lifetime += self._clock.get_time()

        standartMovement(self, **kwargs)





        
