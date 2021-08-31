class Stats():
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.ships_limit = 3
        self.game_active = False
        self.game_continue = False

    def reset_stats(self):
        self.ships_limit = 3
        self.score = 0
        self.level = 1
