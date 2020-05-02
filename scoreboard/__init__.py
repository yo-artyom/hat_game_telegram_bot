class Scoreboard:
    def __init__(self, game):
        self.board = {}
        for player in game.players:
            self.board[player.id] = 0

    def increase_score(self, player):
        self.board[player.id] += 1

    def score_for(self, player):
        return self.board[player.id]
