from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
import pytz
import asyncio

from scripts.github import fetch_recent_commits, load_commit_data, save_commit_data, create_commit_embed
from scripts.github import check_commits_and_send_message
from scripts.xp_database import XPDatabase

from commands.moderation import button
from commands.moderation import bug_contextmenu
from commands.moderation import report_contextmenu
from commands.moderation import mute
from commands.moderation import unmute
from commands.moderation.clear import setup as setup_clear

from commands.information import help
from commands.information import ahelp

from commands.xpsystem import xp
from commands.xpsystem import leaderboard

from commands.features.poll import setup as setup_poll
from commands.features import review

MY_GUILD = discord.Object(id=guildidhere)  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.xp_database = XPDatabase()

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

# Call setup functions
report_contextmenu.setup(client)
bug_contextmenu.setup(client)
help.setup(client)
ahelp.setup(client)
mute.setup(client)
unmute.setup(client)
button.setup(client)
setup_clear(client)
setup_poll(client)
xp.setup(client)
leaderboard.setup(client)

# Dictionary to store the channel IDs for each guild
welcome_leave_channels = {
    23423424242423424: 2342424234324,  # Guild ID : Channel ID -> remeber to place with actual guild and channel id´s 
}

@client.event
async def on_ready():
    print('Bot is ready.')
    await check_commits_and_send_message(client)
    asyncio.create_task(schedule_commit_check(client))

@client.event
async def on_member_join(member):
    guild_id = member.guild.id
    if guild_id in welcome_leave_channels:
        channel_id = welcome_leave_channels[guild_id]
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(f"Welcome {member.mention} to the server!")

@client.event
async def on_member_remove(member):
    guild_id = member.guild.id
    if guild_id in welcome_leave_channels:
        channel_id = welcome_leave_channels[guild_id]
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(f"Goodbye {member.mention}!")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    new_level = client.xp_database.add_xp(message.guild.id, message.author.id, 10)  # Award 10 XP for each message
    if new_level:
        await message.channel.send(f"Congratulations {message.author.mention}, you've leveled up to level {new_level}!")
    await client.process_commands(message)

            
async def schedule_commit_check(client):
    while True:
        await asyncio.sleep(600)  # Sleep for 1 hour (3600 seconds)
        await check_commits_and_send_message(client)

client.run("put your bot token here")
