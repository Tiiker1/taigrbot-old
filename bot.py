import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from scripts.github import fetch_all_commits, load_commit_data, save_commit_data, create_commit_embed
from scripts.github import check_commits_and_send_message
from scripts.xp_database import XPDatabase

from commands.moderation import rolemenu
from commands.moderation import bug_contextmenu
from commands.moderation import report_contextmenu
from commands.moderation import mute
from commands.moderation import unmute
from commands.moderation.clear import setup as setup_clear

from commands.information import help
from commands.information import ahelp
from commands.information import permissions

from commands.features.poll import setup as setup_poll
from commands.features import review

from commands.xpsystem import xp

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.xp_database = XPDatabase()

    async def setup_hook(self):
        await self.tree.sync()  # Syncs commands globally

intents = discord.Intents.all()
client = MyClient(intents=intents)

# Call setup functions
report_contextmenu.setup(client)
bug_contextmenu.setup(client)

help.setup(client)
ahelp.setup(client)
permissions.setup(client)

mute.setup(client)
unmute.setup(client)
rolemenu.setup(client)
setup_clear(client)

setup_poll(client)
review.setup(client)

xp.setup(client)

@client.event
async def on_ready():
    print('client is ready.')
    await client.change_presence(activity=discord.CustomActivity(name='whateveryouwanttoplay', emoji='🖥️'))
    await check_commits_and_send_message(client)
    asyncio.create_task(schedule_commit_check(client))

# Dictionary to store the channel IDs for each guild
welcome_leave_channels = {
    putyourguildidhere: andtextchannelforwelcomeandleavemessageshere,  # Guild ID : Channel ID
}

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
        
    guild_id = message.guild.id
    if client.xp_database.get_xp_system_status(guild_id):
        new_level = client.xp_database.add_xp(guild_id, message.author.id, 10)  # Award 10 XP for each message
        if new_level:
            await message.channel.send(f"Congratulations {message.author.mention}, you've leveled up to level {new_level}!")

async def schedule_commit_check(client):
    while True:
        await asyncio.sleep(600)  # Sleep for 10 minutes (600 seconds)
        await check_commits_and_send_message(client)

client.run("put your bot token here")
