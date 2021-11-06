import bot_config
import player


class Logic:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.ringer_avi_list = []
        self.pcw_request_list = []
        self.embed = bot_config.Embed(logic=self)
        self.button = bot_config.ButtonComponent()
        self.message = bot_config.Message()

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
        player_group = player.PlayerGroup(interaction.user)
        self.pcw_request_list.append(player_group)

        await self.update_status_embed()
        await self.broadcast(self.message.request_pcw)
        await interaction.respond(type=6)

    async def ringer_avi(self, interaction):
        ringer = player.Player(interaction.user)
        self.ringer_avi_list.append(ringer)

        await self.update_status_embed()
        await self.broadcast(self.message.ringer_avi)
        await interaction.respond(type=6)

    async def broadcast(self, message):
        await self.bot.channel_general.send(message)
