import re
from random import choice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from player.factory import PlayerFactory
from repositories.game import GameRepository
from game.round_finisher import RoundFinisher
from game_round.lock import Lock
import callbacks.helpers.game as helpers

def start_play(bot, game):
    helpers.send_message_to_all_players(bot, game, 'Игра начата!')
    helpers.send_keyboard_to_all_players(bot, game,
                                        text=__play_rules(), keyboard=__wait_keyboard())

def start_show(update, context):
    game, game_round, player, query = __set_env(update)

    if not Lock().free:
        update.message.reply_text(f'Нет, сейчас показывает {Lock().player.name}')
        return

    Lock().obtain(player)

    if not game_round.finished():
        word = game_round.random_word()
        query.edit_message_text(text=word, reply_markup=__play_word_keyboard(word))
    else:
        __finish_round(context.bot, game)

def word_guessed(update, context):
    game, game_round, player, query = __set_env(update)

    guessed_word = re.sub("guessed_", "", update.callback_query.data)
    game_round.guess_word(guessed_word)

    if not game_round.finished():
        word = game_round.random_word()
        #   we don't want to show the same word again
        while word == guessed_word:
            word = game_round.random_word()

        query.edit_message_text(text=word, reply_markup=__play_word_keyboard(word))
    else:
        __finish_round(context.bot, game)

def timeoff_word_guessed(update, context):
    game, game_round, player, query = __set_env(update)

    Lock().release()

    guessed_word = re.sub("guessed_timeoff_", "", update.callback_query.data)
    game_round.guess_word(guessed_word)

    if not game_round.finished():
        query.edit_message_text(text=__motivation_text(), reply_markup=__wait_keyboard())
    else:
        __finish_round(context.bot, game)

def timeoff(update, context):
    game, game_round, player, query = __set_env(update)
    Lock().release()
    query.edit_message_text(text=__motivation_text(), reply_markup=__wait_keyboard())


def __wait_keyboard():
    keyboard = [[InlineKeyboardButton("Начать показывать!", callback_data='word')]]
    return InlineKeyboardMarkup(keyboard)

def __play_word_keyboard(word):
    keyboard = [
        [InlineKeyboardButton("Слово угадано!", callback_data=f"guessed_{word}")],
        [InlineKeyboardButton("Время, угадано", callback_data=f"guessed_timeoff_{word}"),
         InlineKeyboardButton("Время, неугадано", callback_data='timeoff')]
    ]
    return InlineKeyboardMarkup(keyboard)

def __play_rules():
    return 'Правила игры: текст текст текст'

def __motivation_text():
    return choice(["Отличный раунд", "Супер", "Было весело"])

def __set_env(update):
    player = PlayerFactory.from_tg_callback(update)
    game = GameRepository().find_by_player(player)
    game_round = game.active_round()
    query = update.callback_query

    return game, game_round, player, query

def __finish_round(bot, game):
    new_round = RoundFinisher(game).call()
    helpers.send_message_to_all_players(bot, game, 'Раунд закончен!')
    helpers.send_keyboard_to_all_players(bot, game,
                                        text=f"Начинается раунд {game.active_round().number}",
                                        keyboard=__wait_keyboard())
