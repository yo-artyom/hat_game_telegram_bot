from game.validator import Validator

class Game:
    def __init__(self, rules):
        self.id = "HARDCODED"
        self.validator = Validator(self)
        self.rules = rules
        self.words_by_player = {}
        self.players = []
        self.rounds = []

    def add_player(self, player):
        self.players.append(player)
        self.words_by_player[player.id] = []

    def add_word(self, player, word):
        self.words_by_player[player.id].append(word)
        return True

    def reset_words_for_player(self, player):
        self.words_by_player[player.id] = []
        return True

    def words(self):
        w = []
        for ws in self.words_by_player.values():
            w.extend(ws)
        return w

    def add_round(self, game_round):
        self.rounds.append(game_round)


    def missing_words_for_player(self, player):
        return (self.rules.words_per_player - len(self.words_by_player[player.id]))
