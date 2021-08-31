from gamesprite import GameSprite


class Bullet(GameSprite):
    def __init__(self, image_name, speed):
        super().__init__(image_name, -speed)

    def update(self):
        super().update()
        # 放置子弹超过游戏边界
        if self.rect.bottom < 0:
            self.kill()
