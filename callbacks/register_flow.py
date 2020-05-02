import re

from player.factory import PlayerFactory
from repositories.game import GameRepository
from game.starter import Starter
from game.registrator import Registrator
import callbacks.play_flow

def start(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    registrator = Registrator(game)

    if game.validator.enough_players():
        update.message.reply_text('Игра заполнена, уходи')
        return

    if game.is_started():
        update.message.reply_text('Игра уже начата')
        return


    if not registrator.register_player(player):
        update.message.reply_text('Невозможно')
        return

    update.message.reply_text(__greeting_text(game))


def add_words(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    registrator = Registrator(game)

    if not registrator.player_registred(player):
        update.message.reply_text("Эй, сначала зарегистрируйся при помощи /start")
        return

    if game.is_started():
        update.message.reply_text('Игра уже начата')
        return

    # remove /add from begging of the message
    words = re.sub('/add\s{0,1}', '', update.message.text)
    # remove spaces after commas, and split by comma
    parsed_words = re.sub(",\s*", ",", words).split(",")

    for word in parsed_words:
        registrator.register_player_word(player, word)

    update.message.reply_text(__formatted_words(game, player))


def reset_words(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    registrator = Registrator(game)

    if game.is_started():
        update.message.reply_text('Игра уже начата')
        return

    if not registrator.player_registred(player):
        update.message.reply_text("Эй, сначала зарегистрируйся при помощи /start")
        return

    game.reset_words_for_player(player)
    update.message.reply_text('Я удалил твои слова')

def player_ready(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    game_starter = Starter(game)

    if game.is_started():
        update.message.reply_text('Игра уже начата')
        return

    if game.missing_words_for_player(player) > 0:
        update.message.reply_text("Эй, все еще не хватает слов")
        return

    if game_starter.call():
        callbacks.play_flow.start_play(context.bot, game)
    else:
        update.message.reply_text("Отлично, ожидаем других игроков")

def __greeting_text(game):
    print(len(game.players))
    if len(game.players) == 1:
        player_names_text = "Ты пока единственный игрок"
    else:
        player_names = map(lambda player: player.name, game.players)
        player_names_text = f"С тобой играют: {', '.join(player_names)}"

    return f"Привет! Ты зарегистрирован в игру.\n"\
           f"{player_names_text}\n"\
           f"Отправь мне команду /add и {game.rules.words_per_player} слов через запятую\n"\
           f"Например: /add Блоб, Шлоб, Крот, Блев, Кнут"


def __formatted_words(game, player):
    formatted_words = map(lambda word: f"• {word}", game.words_by_player[player.id])

    return_words = "\n".join(formatted_words)
    missing_text = ""

    if game.missing_words_for_player(player) > 0:
        missing_text = f"не хватает {game.missing_words_for_player(player)} слов\n"

    return f"Ты добавил слова:\n"\
           f"{return_words}\n"\
           f"{missing_text}"\
           f"Если ты хочешь удалить свои слова - отправь /reset_words\n" \
           f"Если тебя устраивают твои слова и ты готов начать - отправь /ready"
