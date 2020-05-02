import re

class Registrator:
    def __init__(self, game):
        self.game = game

    def register_player(self, player):
        if self.game.validator.enough_players():
            return False
        #   already registred
        if (player.id in map(lambda p: p.id, self.game.players)):
            return False

        self.game.add_player(player)
        print(f"REGISTRED PLAYER {player.name}")

        return True

    def register_player_word(self, player, word):
        if self.game.validator.enough_words_for_player(player):
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

    def player_registred(self, player):
        return player.id in map(lambda p: p.id, self.game.players)
