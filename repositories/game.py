from game import Game
from utils.meta_singleton import MetaSingleton

#   Repository that provide interface to Games storage
#   Currently it uses pattern signleton and keeps only one created game
class GameRepository(metaclass = MetaSingleton):
    def __init__(self, *args, **kwargs):
        self._games = []

    def create(self, rules):
        game = Game(rules)
        self._games.append(game)
        return True

    #   Returns only one existing game.
    #   TODO: reimplement when connection to DB is ready
    def find_by_player(self, player):
        return self._games[0]
