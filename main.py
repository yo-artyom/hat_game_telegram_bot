#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The hat game prototype
"""

import logging

from game import Game
from game.rules import Rules
from repositories.game import GameRepository

import callbacks.register_flow
import callbacks.play_flow

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from utils.read_token import read_token

import logging

TOKEN = read_token()

#   TODO: move this lines initialize to start handler when DB connection is ready
game_rules = Rules(player_number=4, words_per_player=4)
game = GameRepository().create(game_rules)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", callbacks.register_flow.start))
    dispatcher.add_handler(CommandHandler("add", callbacks.register_flow.add_words))
    dispatcher.add_handler(CommandHandler("reset_words", callbacks.register_flow.reset_words))
    dispatcher.add_handler(CommandHandler("ready", callbacks.register_flow.player_ready))

    dispatcher.add_handler(CallbackQueryHandler(callbacks.play_flow.start_show, pattern='^word$'))
    dispatcher.add_handler(CallbackQueryHandler(callbacks.play_flow.timeoff_word_guessed, pattern='^guessed_timeoff_.*$'))
    dispatcher.add_handler(CallbackQueryHandler(callbacks.play_flow.word_guessed, pattern='^guessed_.*$'))
    dispatcher.add_handler(CallbackQueryHandler(callbacks.play_flow.timeoff, pattern='^timeoff$'))

    updater.start_polling()

if __name__ == '__main__':
    main()
