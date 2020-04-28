import re

class Game:
    PLAYERS_NUM = 8;
    WORDS_PER_PLAYER = 5;

    def __init__(self, hat):
        self.id = "HARDCODED"
        self.hat = hat
        self.words_by_player = {}
        self.players = []

    def ready(self):
        return  len(self.players) == self.PLAYERS_NUM

    def register_player(self, player):
        if (len(self.players) == self.PLAYERS_NUM):
            return False
        if (player.id in map(lambda p: p.id, self.players)):
            return False

        self.players.append(player)
        self.words_by_player[player.id] = []

        print(f"REGISTRED PLAYER {player}")
        return True

    def add_word(self, player, word):
        if len(self.words_by_player[player.id]) == self.WORDS_PER_PLAYER:
            return False
        if player.id not in self.words_by_player:
            return False
        #   check for empty word
        if re.match("^\s*$", word):
            return False

        self.words_by_player[player.id].append(word)
        print(f"REGISTRED WORD FOR {player} {word}")
        return True

    def missing_words_for_player(self, player):
        return (self.WORDS_PER_PLAYER - len(self.words_by_player[player.id]))

    def reset_words_for_player(self, player):
        self.words_by_player[player.id] = []
        print(f"RESETED WORDS FOR {player}")
        return True

    def player_registred(self, player):
        return player.id in map(lambda p: p.id, self.players)
