from logging import log
import discord
from discord_components import ComponentsBot
import bot_config
import bot_logic


intents = discord.Intents.all()
bot = ComponentsBot(command_prefix='!', intents=intents)
bot.remove_command('help')
bot.guild = None
bot.channel_general = None
bot.channel_status = None
bot.channel_live = None

config = bot_config.Env()
logic = bot_logic.Logic(bot, config)


@bot.event
async def on_ready():
    bot.guild = discord.utils.get(
        bot.guilds,
        id=int(config.guild_id)
    )
    bot.channel_general = discord.utils.get(
        bot.guild.channels,
        id=int(config.channel_general_id)
    )
    bot.channel_status = discord.utils.get(
        bot.guild.channels,
        id=int(config.channel_status_id)
    )
    bot.channel_live = discord.utils.get(
        bot.guild.channels,
        id=int(config.channel_live_id)
    )
    status_messages = await bot.channel_status.history(limit=5).flatten()
    bot.status_embed = discord.utils.get(
        status_messages,
        id=int(config.status_embed_id)
    )

    if bot.guild is None or\
       bot.channel_general is None or\
       bot.channel_status is None or\
       bot.channel_live is None:
        raise Exception("Couldn't find discord server or channels")

    await logic.update_status_embed()


@bot.event
async def on_button_click(interaction):
    if interaction.component.id == "button_request_pcw":
        await logic.request_pcw(interaction)
    elif interaction.component.id == "button_ringer_avi":
        await logic.ringer_avi(interaction)


bot.run(config.token)
