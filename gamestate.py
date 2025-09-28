class GameState:
    def __init__(self):
        self.stash = 0
        self.level = 1
        self.game_over = False
        self.win=False
        self.paused = False
        self.time_left=10
        self.high_score = 0
        self.inventory =0
        self.time=0
        self.best_time= 100000000