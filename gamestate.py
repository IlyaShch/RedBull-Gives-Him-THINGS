class GameState:
    def __init__(self):
        self.stash = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.time_left=3
        self.high_score = 0