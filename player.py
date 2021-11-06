class Player:
    def __init__(self, discord_user):
        self.discord_name = discord_user.name
        self.discord_id = discord_user.id

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.discord_id == other.discord_id
        return False


class PlayerGroup:
    def __init__(self, discord_user):
        self.number = 5
        self.leader = Player(discord_user)
