from player import Player

class PlayerFactory:
    @classmethod
    def from_tg_update(self, update):
        player_id = update.message.from_user.id
        player_name = update.message.from_user.first_name or update.message.from_user.username
        return Player(player_id, player_name)

    @classmethod
    def from_tg_callback(self, update):
        player_id = update.callback_query.message.chat.id
        player_name = update.callback_query.message.chat.first_name or update.callback_query.message.chat.username
        return Player(player_id, player_name)


