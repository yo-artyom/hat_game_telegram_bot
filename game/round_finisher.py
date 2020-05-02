from game_round import GameRound

class RoundFinisher:
    def __init__(self, game):
        self.game = game

    def call(self):
        last_round_number = self.game.active_round().number
        new_round = GameRound(self.game.words(), last_round_number + 1)
        self.game.add_round(new_round)
        return True


