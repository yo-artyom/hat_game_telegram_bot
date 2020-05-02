from game_round import GameRound

class Starter:
    def __init__(self, game):
        self.game = game

    def call(self):
        if not self.game.validator.ready():
            return False

        self.game.add_round(self.__build_first_round())
        return True

    def __build_first_round(self):
        return GameRound(self.game.words(), 1)

