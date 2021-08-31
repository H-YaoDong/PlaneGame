from gamesprite import GameSprite


class Missile(GameSprite):
    def __init__(self, settings):
        self.settings = settings
        super().__init__("images/missile.png", -self.settings.missile_speed)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
