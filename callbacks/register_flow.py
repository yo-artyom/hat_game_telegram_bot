import re

from player.factory import PlayerFactory
from repositories.game import GameRepository
from game.starter import Starter
from game.registrator import Registrator
import callbacks.play_flow
import callbacks.helpers.game as helpers

def start(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    registrator = Registrator(game)
    if game.validator.enough_players():
        update.message.reply_text('Игра заполнена, уходи')
        return

    if game.is_started():
        update.message.reply_text('Игра уже начата, чего ты ещё хочешь?')
        return

    register_success = registrator.register_player(player)
    if not register_success:
        update.message.reply_text('Невозможно 🙅')
        return

    if len(game.players) > 1:
        helpers.send_message_to_all_players(context.bot, game, __new_player_message(game))
    update.message.reply_text(__greeting_text(game))


def add_words(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    registrator = Registrator(game)

    if not registrator.player_registred(player):
        update.message.reply_text("Эй, сначала зарегистрируйся при помощи /start")
        return

    if game.is_started():
        update.message.reply_text('Игра уже начата, чего ты ещё хочешь?')
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
        update.message.reply_text('Игра уже начата, чего ты ещё хочешь?')
        return

    if not registrator.player_registred(player):
        update.message.reply_text("Эй, сначала зарегистрируйся при помощи /start")
        return

    game.reset_words_for_player(player)
    update.message.reply_text('Я удалил твои слова, можешь написать новые')

def player_ready(update, context):
    player = PlayerFactory.from_tg_update(update)
    game = GameRepository().find_by_player(player)
    game_starter = Starter(game)

    if game.is_started():
        update.message.reply_text('Игра уже начата, чего ты ещё хочешь?')
        return

    if game.missing_words_for_player(player) > 0:
        update.message.reply_text("НУЖНО БОЛЬШЕ СЛОВ! 🧙")
        return

    if game_starter.call():
        callbacks.play_flow.start_play(context.bot, game)
    else:
        update.message.reply_text("Супер, ожидаем других игроков 🐕")

def __greeting_text(game):
    if len(game.players) == 1:
        player_names_text = "Ты пока единственный/ая игрок/НЯ"
    else:
        player_names = map(lambda player: player.name, game.players)
        player_names_text = f"Сейчас с тобой в игре: {', '.join(player_names)}"

    return f"Йо! Ты зарегистрирован_а в игру 🎉\n"\
           f"{player_names_text}\n"\
           f"(Если кого-то нет в списке, ткните его палочкой — скорее всего, он не нажал /start)\n"\
           "\n"\
           f"🎩Отправь мне команду  /add и {game.rules.words_per_player} имен, которые хочешь положить в шляпу, через запятую\n"\
           "\n"\
           f"Пример: /add Блоб, Шлоб, Крот, Блев, Кнут"


def __formatted_words(game, player):
    formatted_words = map(lambda word: f"• {word}", game.words_by_player[player.id])

    return_words = "\n".join(formatted_words)
    missing_text = ""

    if game.missing_words_for_player(player) > 0:
        missing_text = f"не хватает {game.missing_words_for_player(player)} слов\n"

    return f"Ты добавил слова:\n"\
           f"{return_words}\n"\
           f"{missing_text}\n"\
           f"⛔Если ты хочешь удалить свои слова — отправь /reset_words\n" \
           f"✅Если тебя устраивают твои слова и ты готов начать — отправь /ready"

def __new_player_message(game):
    res = "Новый игрок! Теперь в игре: "
    return res + ", ".join(map(lambda player: player.name, game.players))
