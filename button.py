from gamesprite import GameSprite


class PlayButton(GameSprite):
    def __init__(self, settings):
        # 1. 调用父类方法，设置图片
        super().__init__("images/play.png", 0)
        self.settings = settings
        # 2. 设置按钮的初始位置
        self.rect.centerx = self.settings.SCREEN_RECT.centerx
        self.rect.centery = self.settings.SCREEN_RECT.centery


class StopButton(GameSprite):
    def __init__(self, settings):
        super().__init__("images/stop.png", 0)
        self.settings = settings
        # 设置按钮的初始位置
        self.rect.right = self.settings.SCREEN_RECT.right - 20
        self.rect.top = 100


class ExitButton(GameSprite):
    def __init__(self, settings):
        super().__init__("images/exit.png", 0)
        self.settings = settings
        # 设置按钮的初始位置
        self.rect.right = self.settings.SCREEN_RECT.right - 20
        self.rect.top = 150
