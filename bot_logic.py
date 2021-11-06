from bot_config import Embed, ButtonComponent, Message
from player import Player, PlayerGroup


class Logic:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.ringer_avi_list = []
        self.pcw_request_list = []
        self.embed = Embed(logic=self)
        self.button = ButtonComponent()
        self.message = Message()

    async def update_status_embed(self):
        self.embed.update_status()

        if self.bot.status_embed is None:
            status_embed = await self.bot.channel_status.send(
                embed=self.embed.status,
                components=self.button.status
            )

            self.config.set("status_embed_id", status_embed.id)
            self.bot.status_embed = status_embed
            return
        await self.bot.status_embed.edit(
            embed=self.embed.status
        )

    async def request_pcw(self, interaction):
        player_group = PlayerGroup(interaction.user)
        if self.is_in_queue(player_group.leader):
            await interaction.respond(
                type=4,
                content=self.message.error_inqueue
                )
            return

        self.pcw_request_list.append(player_group)

        await self.update_status_embed()
        await self.broadcast(self.message.request_pcw.format(
            playername=player_group.leader.discord_name)
            )
        await interaction.respond(type=6)

    async def ringer_avi(self, interaction):
        ringer = Player(interaction.user)
        if self.is_in_queue(ringer):
            await interaction.respond(
                type=4,
                content=self.message.error_inqueue
                )
            return

        self.ringer_avi_list.append(ringer)

        await self.update_status_embed()
        await self.broadcast(self.message.ringer_avi.format(
            playername=ringer.discord_name)
            )
        await interaction.respond(type=6)

    async def remove_from_queue(self, interaction):
        player_toremove = Player(interaction.user)
        if not self.is_in_queue(player_toremove):
            await interaction.respond(
                type=4,
                content=self.message.error_notinqueue
                )
            return

        for ring_in_queue in self.ringer_avi_list:
            if player_toremove == ring_in_queue:
                self.ringer_avi_list.remove(ring_in_queue)
        for pcw_in_queue in self.pcw_request_list:
            if pcw_in_queue.leader == player_toremove:
                self.pcw_request_list.remove(pcw_in_queue)

        await self.update_status_embed()
        await self.broadcast(self.message.remove_from_queue.format(
            playername=player_toremove.discord_name)
            )
        await interaction.respond(type=6)

    def is_in_queue(self, player):
        for ring_in_queue in self.ringer_avi_list:
            if player == ring_in_queue:
                return True
        for pcw_in_queue in self.pcw_request_list:
            if pcw_in_queue.leader == player:
                return True
        return False

    async def broadcast(self, message):
        await self.bot.channel_general.send(message)
