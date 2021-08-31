from gamesprite import GameSprite
from settings import Settings


class Background(GameSprite):
    """背景精灵组，让背景图移动起来"""
    def __init__(self, is_alt=False):
        super().__init__("images/backgroud.png")
        if is_alt:
            self.rect.y = -self.rect.height
        self.settings = Settings()

    def update(self):
        # 调用父类的update方法
        super().update()
        # 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= self.settings.SCREEN_RECT.height:
            self.rect.y = -self.rect.height
