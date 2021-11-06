class Player:
    def __init__(self, discord_user):
        self.discord_name = discord_user.name


class PlayerGroup:
    def __init__(self, discord_user):
        self.number = 5
        self.leader = discord_user.name
