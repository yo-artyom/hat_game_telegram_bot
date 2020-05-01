#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The hat game prototype
"""

import logging

from game import Game
from game.rules import Rules
from player import Player
from repositories.game import GameRepository

import callbacks.register_flow
import callbacks.game_flow

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils.read_token import read_token

import logging

TOKEN = read_token()

#   TODO: move this lines initialize to start handler when DB connection is ready
game_rules = Rules(player_number=1, words_per_player=5)
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

    updater.start_polling()

if __name__ == '__main__':
    main()
