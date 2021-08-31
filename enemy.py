from gamesprite import GameSprite
import random
from settings import Settings
from bullet import Bullet
import pygame


class Enemy(GameSprite):
    def __init__(self, image_name, enemy_group):
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(image_name)
        # 2. 指定敌机的随机速度 1~3
        self.speed = random.randint(1, 3)
        # 3. 指定敌机的随机位置
        self.rect.bottom = 0
        self.directoin = random.randint(-1, 1)
        self.enemy_group = enemy_group
        self.isCollide = False
        self.settings = Settings()
        max_x = self.settings.SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()
        x = self.rect.x + self.directoin*self.speed
        for enemy in self.enemy_group:
            if self == enemy:
                continue
            else:
                if pygame.sprite.collide_rect(self, enemy):
                    self.isCollide = True
        if 0 <= x <= self.settings.SCREEN_RECT.width - self.rect.width and not self.isCollide:
            self.rect.x = x
        else:
            self.directoin = -self.directoin
        # 2. 判断是否飞出屏幕，如果是，则从精灵组中删除
        if self.rect.y >= self.settings.SCREEN_RECT.height:
            # kill() 方法可将精灵从精灵组中移除，并且会调用 __del_() 方法
            self.kill()


class EnemyElite(Enemy):
    isBuilded = False

    def __init__(self, image_name, stats, enemy_group):
        # 调用父类的初始化方法
        super().__init__(image_name, enemy_group)
        EnemyElite.isBuilded = True
        # 设置boss敌机的血量
        self.health_point = 5
        self.is_missile = False
        self.enemy_group = enemy_group
        self.hit_flag = False
        self.speed = 1
        self.stats = stats

    # 更新状态
    def update(self):
        if self.hit_flag:
            if self.is_missile:
                self.health_point -= 2
                self.is_missile = False
            else:
                self.health_point -= 1
            self.hit_flag = False

        if self.health_point <= 0:
            self.kill()
            self.stats.game_active = False
        super().update()

    # 发射子弹
    def fire(self, bullets_group):
        bullet = Bullet("images/bullet1.png", -2)
        bullet.rect.top = self.rect.y + self.rect.height + 5
        bullet.rect.centerx = self.rect.centerx + 1
        bullets_group.add(bullet)

    # 被英雄子弹击中
    def get_hit(self, is_missile=False):
        self.hit_flag = True
        self.is_missile = is_missile
