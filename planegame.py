import pygame
from pygame.time import Clock
from settings import Settings
from background import Background
from pygame.sprite import Group
from hero import Hero
from enemy import Enemy, EnemyElite
from pygame import key
import sys
from button import PlayButton, StopButton, ExitButton
from scoreboard import Scoreboard
from game_stats import Stats
from time import sleep
from fruit import Fruit


class PlaneGame(object):
    def __init__(self):
        self.stats = Stats()
        self.settings = Settings(self.stats)
        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(self.settings.SCREEN_RECT.size)

        # 2. 创建游戏时钟
        self.clock = Clock()
        # 3. 调用私有方法，创建精灵和精灵组
        self.__create_sprites()

        # 设置定时器事件 -- 创建敌机
        pygame.time.set_timer(self.settings.CREATE_ENEMY_EVENT, 3000)
        pygame.time.set_timer(self.settings.ENEMY_FIRE_EVENT, 1000)
        pygame.time.set_timer(self.settings.CHANGE_DIRECTION, 2000)

    def __create_sprites(self):
        # 创建背景精灵和背景精灵组
        bg1 = Background()
        bg2 = Background(True)
        # 创建敌机精灵组
        self.bg_group = Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = Group()
        self.elite_enemy_group = Group()

        self.enemy_bullets_group = Group()
        # 创建飞船和飞船精灵组
        self.hero = Hero("images/ship1.png")
        self.hero_group = Group(self.hero)

        self.fruit_group = Group()

        self.playbutton = PlayButton(self.settings)
        self.playbutton_group = Group(self.playbutton)

        self.stopbutton = StopButton(self.settings)
        self.stopbutton_group = Group(self.stopbutton)

        self.exitbutton = ExitButton(self.settings)
        self.exitbutton_group = Group(self.exitbutton)

        self.scoreboard = Scoreboard(self.screen, self.settings, self.stats)

        # 先显示背景图片和英雄飞船
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)

    def start_game(self):
        while True:
            if not self.stats.game_active:
                self.playbutton_group.update()
                self.playbutton_group.draw(self.screen)
            else:
                # 1. 设置刷新频率
                self.clock.tick(self.settings.FRAME_PER_SEC)

                # 3. 碰撞检测
                self.__check_collide()

                # 4. 更新/绘制精灵组
                self.__update_sprites()
            # 2. 事件监听
            self.__event_handler()

            self.screen.blit(self.scoreboard.score_image, self.scoreboard.score_rect)
            self.screen.blit(self.scoreboard.high_score_image, self.scoreboard.high_score_rect)
            self.screen.blit(self.scoreboard.level_image, self.scoreboard.level_rect)

            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == self.settings.CREATE_ENEMY_EVENT:
                enemy = Enemy("images/enemy1.png", self.enemy_group)
                self.enemy_group.add(enemy)
            elif event.type == self.settings.CHANGE_DIRECTION:
                for enemy in self.enemy_group:
                    enemy.directoin = -enemy.directoin
                self.enemy_group.update()
                self.enemy_group.draw(self.screen)
            elif event.type == self.settings.BOSS_APPEAR:
                if not EnemyElite.isBuilded:
                    eliteenemy = EnemyElite("images/enemy3.png", self.stats, self.enemy_group)
                    self.elite_enemy_group.add(eliteenemy)
            elif event.type == self.settings.ENEMY_FIRE_EVENT:
                for enemy in self.elite_enemy_group.sprites():
                    enemy.fire(self.enemy_bullets_group)
            elif event.type == self.settings.FRUIT_APPEAR:
                self.fruit_group.add(Fruit("images/fruit.png", self.settings))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.hero.fire()
                elif event.key == pygame.K_r:
                    self.hero.fire(True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.playbutton.rect.collidepoint(mouse_x, mouse_y):
                    if not self.stats.game_continue:
                        self.stats.game_active = True
                        EnemyElite.isBuilded = False
                        Scoreboard.isSix = False
                        self.hero = Hero("images/ship1.png")
                        self.hero_group = Group(self.hero)
                        self.enemy_bullets_group.empty()
                        self.stats.reset_stats()
                        self.settings.alien_points = 500
                        self.settings.eltie_points = 100
                        self.settings.hero_speed = 4
                        self.settings.bullet_speed = 2
                        self.settings.missile_speed = 3
                        self.enemy_group.empty()

                        self.scoreboard.prep_score()
                        self.scoreboard.prep_level()
                        self.scoreboard.prep_heros()
                        self.scoreboard.heros.update()
                        self.scoreboard.heros.draw(self.screen)
                        pygame.display.update()
                    else:
                        self.stats.game_active = True
                        self.stats.game_continue = False
                elif self.stopbutton.rect.collidepoint(mouse_x, mouse_y):
                    self.stats.game_active = False
                    self.stats.game_continue = True
                elif self.exitbutton.rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        key_pressed = key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed_x = self.settings.hero_speed
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed_x = -self.settings.hero_speed
        else:
            self.hero.speed_x = 0

        if key_pressed[pygame.K_UP]:
            self.hero.speed_y = -self.settings.hero_speed
        elif key_pressed[pygame.K_DOWN]:
            self.hero.speed_y = self.settings.hero_speed
        else:
            self.hero.speed_y = 0

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.elite_enemy_group.update()
        self.elite_enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.fruit_group.update()
        self.fruit_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.hero.missiles.update()
        self.hero.missiles.draw(self.screen)

        self.enemy_bullets_group.update()
        self.enemy_bullets_group.draw(self.screen)

        self.scoreboard.heros.update()
        self.scoreboard.heros.draw(self.screen)

        self.stopbutton_group.update()
        self.stopbutton_group.draw(self.screen)

        self.exitbutton_group.update()
        self.exitbutton_group.draw(self.screen)

    def __check_collide(self):
        # 子弹与敌机碰撞
        self.bullet_collisions = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True,  True)
        if self.bullet_collisions:
            for aliens in self.bullet_collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()
            self.scoreboard.check_high_score()
            self.scoreboard.update_level()
            pygame.display.update()

        # 导弹与敌机碰撞
        self.missle_collisions = pygame.sprite.groupcollide(self.hero.missiles, self.enemy_group, True,  True)
        if self.missle_collisions:
            for aliens in self.missle_collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()
            self.scoreboard.check_high_score()
            self.scoreboard.update_level()
            pygame.display.update()

        
        # 敌机精英子弹摧毁英雄
        if pygame.sprite.spritecollideany(self.hero, self.enemy_bullets_group):
            if not self.hero.is_unbeatable:
                if self.stats.ships_limit > 0:
                    self.stats.ships_limit -= 1
                    self.enemy_group.empty()
                    self.elite_enemy_group.empty()
                    self.enemy_bullets_group.empty()
                    self.scoreboard.prep_heros()
                    self.hero.center_hero()
                    pygame.display.update()
                    sleep(0.5)
                else:
                    self.stats.game_active = False

        # 子弹与敌机精英碰撞
        self.elite_enemy_bullet_collided_dict = pygame.sprite.groupcollide(self.hero.bullets, self.elite_enemy_group, True, False)
        if self.elite_enemy_bullet_collided_dict:
            for bullet in self.elite_enemy_bullet_collided_dict:
                if bullet in self.elite_enemy_bullet_collided_dict:
                    for enemy_collided in self.elite_enemy_bullet_collided_dict[bullet]:
                        enemy_collided.get_hit()  # 被击中的精英敌人调用更改击中状态的函数
            self.stats.score += self.settings.alien_points
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()
            self.scoreboard.check_high_score()
            self.scoreboard.update_level()
            pygame.display.update()


        # 英雄吃果实
        if pygame.sprite.spritecollide(self.hero, self.fruit_group, True):
            self.hero.eat_fruit()

        # 导弹与敌机精英碰撞
        self.elite_enemy_missile_collided_dict = pygame.sprite.groupcollide(self.hero.missiles, self.elite_enemy_group, True, False)
        if self.elite_enemy_missile_collided_dict:
            for bullet in self.elite_enemy_missile_collided_dict:
                if bullet in self.elite_enemy_missile_collided_dict:
                    for enemy_collided in self.elite_enemy_missile_collided_dict[bullet]:
                        enemy_collided.get_hit(True)  # 被击中的精英敌人调用更改击中状态的函数
            for eltie in self.elite_enemy_missile_collided_dict.values():
                self.stats.score += self.settings.alien_points * len(eltie)
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()
            self.scoreboard.check_high_score()
            self.scoreboard.update_level()
            self.enemy_bullets_group.empty()
            self.hero.bullets.empty()
            pygame.display.update()

        # 敌机精英与英雄飞机的子弹碰撞会消失，导弹碰撞不会消失
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_bullets_group, True, True)

        # 敌机撞毁英雄
        if not self.hero.is_unbeatable:
            if pygame.sprite.spritecollideany(self.hero, self.enemy_group):
                if self.stats.ships_limit > 0:
                    self.stats.ships_limit -= 1
                    self.enemy_group.empty()
                    self.elite_enemy_group.empty()
                    self.enemy_bullets_group.empty()
                    self.scoreboard.prep_heros()
                    self.hero.center_hero()
                    pygame.display.update()

                    sleep(0.5)
                else:
                    self.stats.game_active = False
        else:
            pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 敌机精英与英雄撞毁
        if pygame.sprite.spritecollideany(self.hero, self.elite_enemy_group) and not self.hero.is_unbeatable:
            if self.stats.ships_limit > 0:
                self.stats.ships_limit -= 1
                self.enemy_group.empty()
                self.elite_enemy_group.empty()
                self.enemy_bullets_group.empty()
                self.scoreboard.prep_heros()
                self.hero.center_hero()
                pygame.display.update()
                sleep(0.5)
            else:
                self.stats.game_active = False

    def __game_over(self):
        print("game over!")
        pygame.quit()
        sys.exit()
