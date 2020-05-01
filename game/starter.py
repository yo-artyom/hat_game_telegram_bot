from game_round import GameRound

class Starter:
    def __init__(self, game):
        self.game = game

    def call(self):
        if not self.game.validator.ready():
            return False

        self.game.add_round(self.__create_round())
        return True

    def __create_round(self):
        first_round = GameRound(self.game.words(), 1)
        self.game.add_round(first_round)

