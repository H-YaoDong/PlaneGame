import pygame.font
from hero import Hero, HeroScoreBoard
from pygame.sprite import Group


class Scoreboard():
    """显示得分信息的类"""
    isSix = False

    def __init__(self, screen, settings, stats):
        pygame.init()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_heros()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, (245, 122, 39))

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分渲染成图片"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, (0, 176, 240))

        # 将最高分显示在屏幕顶部的中部
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """将等级渲染成图像"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, (112, 48, 160))

        # 将等级显示在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def update_level(self):
        if self.stats.score % 500 == 0:
            if self.stats.score >= 2000 and not Scoreboard.isSix:
                self.stats.level = 5
                self.prep_level()
                pygame.event.post(pygame.event.Event(self.settings.BOSS_APPEAR))
                pygame.event.post(pygame.event.Event(self.settings.FRUIT_APPEAR))
                Scoreboard.isSix = True
            elif self.stats.score < 2000 and self.stats.score % 500 == 0:
                self.stats.level += 1
                self.prep_level()
                pygame.event.post(pygame.event.Event(self.settings.FRUIT_APPEAR))

    def prep_heros(self):
        self.heros = Group()
        for hero_number in range(self.stats.ships_limit):
            hero = HeroScoreBoard()
            hero.rect.x = 10 + hero_number * hero.rect.width
            hero.rect.y = 10
            self.heros.add(hero)
