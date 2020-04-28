import re

from factories.player   import PlayerFactory
from repositories.game  import GameRepository

def start(update, context):
    player = PlayerFactory.from_tg_update(update)
    game_repo = GameRepository()
    game = game_repo.find_by_player(player)

    if game.ready():
        update.message.reply_text('Игра заполнена, уходи')
        return

    if not game.register_player(player):
        update.message.reply_text('Невозможно')
        return

    update.message.reply_text(__greeting_test(game))


def add_words(update, context):
    player = PlayerFactory.from_tg_update(update)
    game_repo = GameRepository()
    game = game_repo.find_by_player(player)

    if not game.player_registred(player):
        update.message.reply_text("Эй, сначала зарегистрируйся при помощи /start")
        return

    # remove /add from begging of the message
    words = re.sub('/add\s{0,1}', '', update.message.text)
    # remove spaces after commas, and split by comma
    parsed_words = re.sub(",\s*", ",", words).split(",")

    for word in parsed_words:
        game.add_word(player, word)

    update.message.reply_text(__formatted_words(game, player))


def reset_words(update, context):
    player = PlayerFactory.from_tg_update(update)
    game_repo = GameRepository()
    game = game_repo.find_by_player(player)

    if not game.player_registred(player):
        update.message.reply_text("Эй, сначала зарегистрируйся при помощи /start")
        return

    game.reset_words_for_player(player)
    update.message.reply_text('Я удалил твои слова')


def __greeting_test(game):
    print(len(game.players))
    if len(game.players) == 1:
        player_names_text = "Ты пока единственный игрок"
    else:
        player_names = map(lambda player: player.name, game.players)
        player_names_text = f"С тобой играют: {', '.join(player_names)}"

    return f"Привет! Ты зарегистрирован в игру.\n"\
           f"{player_names_text}\n"\
           f"Отправь мне команду /add и {game.WORDS_PER_PLAYER} слов через запятую\n"\
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
           f"Если ты хочешь удалить свои слова - отправь /reset_words"

