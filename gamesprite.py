import pygame
from pygame.sprite import Sprite


class GameSprite(Sprite):
    """游戏精灵的基类，游戏中的所有精灵都将继承该类"""
    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 更新精灵的位置，默认是让精灵向下移动
        self.rect.y += self.speed
