from random import choice

class GameRound:
    def __init__(self, words, round_number):
        self.left_words = words
        self.guessed_words = []
        self.number = round_number

    def guess_word(self, word):
        self.left_words.remove(word)

    def random_word(self):
        return random.choice(self.left_words)

    def finished(self):
        return len(self.left_words) == 0
