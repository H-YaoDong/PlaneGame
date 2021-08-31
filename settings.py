import pygame
import random


class Settings():
    def __init__(self, stats=None):
        """保存游戏的基本设置"""
        self.stats = stats
        self.SCREEN_RECT = pygame.Rect(0, 0, 800, 600)
        self.FRAME_PER_SEC = 60
        # 创建敌机的定时器常量 --> 设置定时器事件 --> 事件监听
        self.CREATE_ENEMY_EVENT = pygame.USEREVENT
        self.CREATE_ELITE_ENEMY_EVENT = pygame.USEREVENT + 1
        self.ELITE_ENEMY_CRASH_EVENT = pygame.USEREVENT + 2
        self.ENEMY_FIRE_EVENT = pygame.USEREVENT + 3
        self.BOSS_APPEAR = pygame.USEREVENT + 4
        self.ELITE_ENEMY_CRASH_EVENT = pygame.USEREVENT + 5
        self.FRUIT_APPEAR = pygame.USEREVENT + 6
        self.CHANGE_DIRECTION = pygame.USEREVENT + 7

        self.enemy_speed = random.randint(1, 3)

        self.hero_speed = 4
        self.bullet_speed = 2
        self.missile_speed = 3
        self.score_board_bgcolor = (150, 150, 150)
        self.score_text_color = (255, 255, 255)

        self.alien_points = 500
        self.eltie_points = 100
