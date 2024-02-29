import pygame
import sys
import os
sys.path.insert(1, os.path.abspath(__file__) + "/../..")
from objects.behavior.movement import standartMovement


class Group(pygame.sprite.Group):

    def __init__(self, *sprites) -> None:

        super().__init__(*sprites)


    def _setObserver(self, rect, observer, resolution, scale):

        if observer.rect == rect:

            rect.width *= scale
            rect.height *= scale

            rect.centerx = resolution[0] // 2
            rect.centery = resolution[1] // 2


        else:

            rect.x *= scale
            rect.y *= scale
            rect.width *= scale
            rect.height *= scale

            rect.x -= observer.rect.centerx * scale - resolution[0] // 2
            rect.y -= observer.rect.centery * scale - resolution[1] // 2

        return rect
    

    def _setScale(self, image, scale):

        size = image.get_size()
        image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))

        return image


    def draw(self, surface, bgsurf=None, special_flags=0, **kwargs):

        observer = kwargs["observer"]
        resolution = kwargs["settings"]["window"]["resolution"]
        scale = kwargs["scale"]

        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (self._setScale(spr.image, scale), self._setObserver(spr.rect.copy(), observer, resolution, scale), None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                
                self.spritedict[spr] = surface.blit(
                    self._setScale(spr.image, scale), self._setObserver(spr.rect.copy(), observer, resolution, scale), None, special_flags
                )

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

class Sprite(pygame.sprite.Sprite):

    def __init__(self, texture: pygame.Surface, position: tuple, *groups) -> None:

        super().__init__(*groups)

        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.float_position = list(self.rect.center)

        self._clock = pygame.time.Clock()
        self._lifetime = 0


    def update(self, *args, **kwargs):
        pass

    # def __eq__(self, other: object) -> bool:
    #     return id(self) == id(other)

class Entity(Sprite):

    def __init__(self, texture: pygame.Surface, position: tuple, controller, *groups, **kwargs) -> None:

        super().__init__(texture, position, *groups)

        self.controller = controller

        self.speed = [0,0]
        self.move_block = [0,0]

        self.kwattrs = kwargs

    def update(self, *args, **kwargs):

        self._clock.tick()
        self._lifetime += self._clock.get_time()

        standartMovement(self, **kwargs)

        # if "func" in self.kwattrs:
        #     self.kwattrs["func"](f"center: {self.rect.center}; float {self.float_position}" )





        
