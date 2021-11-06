import os
import discord
from discord_components import Button, ButtonStyle
import dotenv


class Env:
    def __init__(self):
        self.dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(self.dotenv_file)

        self.token = os.getenv('TOKEN')
        self.guild_id = os.getenv('guild_id')
        self.channel_general_id = os.getenv('channel_general_id')
        self.channel_status_id = os.getenv('channel_status_id')
        self.channel_live_id = os.getenv('channel_live_id')
        self.status_embed_id = os.getenv('status_embed_id')

        if not self.check_if_set(self.token) or \
           not self.check_if_set(self.guild_id) or \
           not self.check_if_set(self.channel_general_id) or\
           not self.check_if_set(self.channel_status_id) or\
           not self.check_if_set(self.channel_live_id):
            raise Exception("Couldn't load .env")

    def check_if_set(self, value):
        if value is None or value == "" or value == 0:
            return False
        return True

    def set(self, key, value):
        os.environ[key] = str(value)
        dotenv.set_key(self.dotenv_file, key, os.environ[key])


class Embed:
    def __init__(self, logic):
        self.logic = logic
        self.update_status()

    def update_status(self):
        ringer_avi_str = ""
        for ringer in self.logic.ringer_avi_list:
            ringer_avi_str += f"{ringer.discord_name} \n"
        if ringer_avi_str == "":
            ringer_avi_str = "No ringer avi"

        pcw_request_str = ""
        for player_group in self.logic.pcw_request_list:
            pcw_request_str += f"{player_group.number}v{player_group.number} \
                Requested by {player_group.leader.discord_name} \n"
        if pcw_request_str == "":
            pcw_request_str = "No pcw requested"

        self.status = discord.Embed(color=0xFFD700, title=f"Status")
        self.status.add_field(
            name="PCW",
            value=pcw_request_str,
            inline=True
            )
        self.status.add_field(
            name="Ringers avi",
            value=ringer_avi_str,
            inline=True
            )


class ButtonComponent:
    def __init__(self):
        self.status = [[
            Button(
                style=ButtonStyle.blue,
                label="Request pcw",
                custom_id=f"button_request_pcw"
                ),
            Button(
                style=ButtonStyle.blue,
                label="Ring avi",
                custom_id=f"button_ringer_avi"
                ),
            Button(
                style=ButtonStyle.red,
                label="Remove",
                custom_id=f"button_remove_from_queue"
                )
            ]]


class Message:
    def __init__(self):
        self.request_pcw = "PCW requested by ``{playername}``."
        self.ringer_avi = "``{playername}`` is available to ring."
        self.error_inqueue = "Error: you are already in queue."
        self.error_notinqueue = "Error: you are not in queue."
        self.remove_from_queue = "``{playername}`` was removed from the queue."
