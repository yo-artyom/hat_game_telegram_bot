from player import Player

class PlayerFactory:
    @classmethod
    def from_tg_update(cls, update):
        player_id = update.message.from_user.id
        player_name = update.message.from_user.username or update.message.from_user.first_name
        return Player(player_id, player_name)

