import re

class Registrator:
    def __init__(self, game):
        self.game = game

    def game_ready(self):
        return self.__enough_players() and all(self.__enough_words_by_player(p) for p in self.game.players)

    def register_player(self, player):
        if self.__enough_players():
            return False
        #   already registred
        if (player.id in map(lambda p: p.id, self.game.players)):
            return False

        self.game.add_player(player)
        print(f"REGISTRED PLAYER {player}")

        return True

    def register_player_word(self, player, word):
        if self.__enough_words_by_player(player):
            return False
        #   player isn't registred yet
        if player.id not in self.game.words_by_player:
            return False
        #   check for empty word
        if re.match("^\s*$", word):
            return False

        self.game.add_word(player, word)
        print(f"REGISTRED WORD FOR {player} {word}")
        return True

    def __enough_players(self):
        return len(self.game.players) == self.game.rules.player_number

    def __enough_words_by_player(self, player):
        return len(self.game.words_by_player[player.id]) == self.game.rules.words_per_player
