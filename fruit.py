from gamesprite import GameSprite
import random


class Fruit(GameSprite):
    def __init__(self, image_name, settings):
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(image_name)
        # 3. 指定敌机的随机位置
        self.rect.bottom = 0
        self.settings = settings
        # 设置出现的初始位置
        self.rect.x = random.randint(200, 400)
        self.rect.y = random.randint(300, 400)
