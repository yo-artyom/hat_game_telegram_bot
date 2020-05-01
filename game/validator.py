class Validator:
    def __init__(self, game):
        self.game = game

    def enough_players(self):
        return len(self.game.players) == self.game.rules.player_number

    def enough_words_for_player(self, player):
        return len(self.game.words_by_player[player.id]) == self.game.rules.words_per_player

    def ready(self):
        return self.enough_players() and all(self.enough_words_for_player(p) for p in self.game.players)
