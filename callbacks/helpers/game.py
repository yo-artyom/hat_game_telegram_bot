def send_message_to_all_players(bot, game, text):
    for player in game.players:
        bot.send_message(chat_id=player.id, text=text)
