from gamesprite import GameSprite
from settings import Settings
from pygame.sprite import Group
from bullet import Bullet
from missile import Missile
import pygame
import time


class Hero(GameSprite):
    start = None

    def __init__(self, images_name):
        # 1. 调用父类方法，设置图片
        super().__init__(images_name, 0)
        self.settings = Settings()
        # 2. 设置飞船的初始位置
        self.center_hero()
        self.speed_x = 0
        self.speed_y = 0
        # 3. 创建子弹精灵组
        self.bullets = Group()
        # 4. 创建导弹精灵组
        self.missiles = Group()
        self.is_unbeatable = False

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 控制英雄不能离开边界
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > self.settings.SCREEN_RECT.right:
            self.rect.right = self.settings.SCREEN_RECT.right

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > self.settings.SCREEN_RECT.bottom:
            self.rect.bottom = self.settings.SCREEN_RECT.bottom
        
        # 判断英雄是否处于无敌状态
        if self.is_unbeatable:
            self.image = pygame.image.load("images/unbeatable_ship.png")
            if time.time() - Hero.start >= 3:
                self.is_unbeatable = False
                self.image = pygame.image.load("images/ship1.png")

    def fire(self, is_skill=False):
        if not is_skill:
            # 1. 创建子弹精灵
            bullet = Bullet("images/bullet.png", 2)
            # 2. 设置精灵位置
            bullet.rect.bottom = self.rect.y+10
            bullet.rect.centerx = self.rect.centerx
            # 3. 添加到精灵组
            self.bullets.add(bullet)
        # 发射的是导弹：
        else:
            missile = Missile(self.settings)
            missile.rect.bottom = self.rect.y+10
            missile.rect.centerx = self.rect.centerx
            self.missiles.add(missile)

    # 将英雄放置在游戏窗口底部的中部
    def center_hero(self):
        self.rect.midbottom = self.settings.SCREEN_RECT.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    # 吃无敌果实
    def eat_fruit(self):
        Hero.start = time.time()
        self.is_unbeatable = True


class HeroScoreBoard(GameSprite):
    def __init__(self, image_name="images/ship2.png", speed=0):
        super().__init__(image_name, speed=0)