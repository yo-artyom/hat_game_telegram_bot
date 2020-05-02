def send_message_to_all_players(bot, game, text):
    for player in game.players:
        bot.send_message(chat_id=player.id, text=text)

def send_keyboard_to_all_players(bot, game, text, keyboard):
    for player in game.players:
        bot.send_message(chat_id=player.id, text=text, reply_markup=keyboard)

def pretty_scoreboard_player_text(game, player):
    return f"{player.name} - {game.scoreboard.score_for(player)}"

def pretty_scoreboard_text(game):
    res = "Результаты:\n"
    for player in game.players:
        res += f"{pretty_scoreboard_player_text(game, player)}\n"
    return res

