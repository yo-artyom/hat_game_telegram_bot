from game_round import GameRound
class Starter:
    def __init__(self, game):
        self.game = game

    def call(self):
        self.__create_round()
        return True

    def __create_round(self):
        first_round = GameRound(self.game.words(), 1)
        self.game.add_round(first_round)
