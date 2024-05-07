from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
from datetime import datetime
import pytz
import json

from commands import bug_contextmenu
from commands import report_contextmenu
from commands.clear import setup as setup_clear
from commands.poll import setup as setup_poll

MY_GUILD = discord.Object(id=guildidhere)  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

# Call setup functions
report_contextmenu.setup(client)
bug_contextmenu.setup(client)
setup_clear(client)
setup_poll(client)

# Define your GitHub repository information
GITHUB_USERNAME = 'github username here'
REPOSITORY_NAME = 'repo name here'
REPOSITORY_URL = f'https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}'
COMMIT_DATA_DIR = 'commit_data'

# Define Helsinki timezone
helsinki_tz = pytz.timezone('Europe/Helsinki')

# Function to fetch recent commits from GitHub
def fetch_recent_commits():
    try:
        response = requests.get(f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/commits')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except Exception as e:
        print(f"Failed to fetch commits: {e}")
        return []

# Function to load commit data from a JSON file
def load_commit_data():
    try:
        with open(os.path.join(COMMIT_DATA_DIR, 'commits.json'), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save commit data to a JSON file
def save_commit_data(commits):
    try:
        os.makedirs(COMMIT_DATA_DIR, exist_ok=True)
        with open(os.path.join(COMMIT_DATA_DIR, 'commits.json'), 'w') as file:
            json.dump(commits, file, indent=4)
    except Exception as e:
        print(f"Failed to save commit data: {e}")

# Function to create an embed message for a commit
def create_commit_embed(commit):
    try:
        commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
        commit_date = commit_date.replace(tzinfo=pytz.utc).astimezone(helsinki_tz)  # Convert to Helsinki timezone
        commit_date_str = commit_date.strftime("%b %d, %Y %I:%M %p %Z")

        github_username = commit["commit"]["author"].get("username", commit["commit"]["author"]["name"])

        embed = discord.Embed(
            title="New Commit",
            description=f"**{commit['commit']['message'].splitlines()[0]}**",
            color=0x6e5494,
        )
        embed.set_author(name=commit["commit"]["author"]["name"], icon_url=commit["author"]["avatar_url"])
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/Octocat.png")
        embed.set_footer(text=f"{github_username} | {commit_date_str}")
        embed.add_field(name="\u200b", value=f"[View Commit on GitHub]({REPOSITORY_URL}/commit/{commit['sha']})",
                        inline=False)

        return embed
    except Exception as e:
        print(f"Failed to create commit embed: {e}")
        return None

# Function to check for new commits and send message to Discord
async def check_commits_and_send_message():
    try:
        # Fetch recent commits from GitHub
        commits = fetch_recent_commits()
        if not commits:
            print("No commits found.")
            return

        # Reverse the order of commits to process them from oldest to newest
        commits.reverse()

        # Load previously sent commits
        sent_commits = load_commit_data()

        # Filter out already sent commits
        unsent_commits = [commit for commit in commits if commit['sha'] not in sent_commits]

        # Send messages for unsent commits
        for commit in unsent_commits:
            embed = create_commit_embed(commit)
            if embed:
                channel_id = 1232513106471686255  # Replace this with the actual channel ID
                channel = client.get_channel(channel_id)
                await channel.send(embed=embed)

        # Update the list of sent commits
        all_commits = sent_commits + [commit['sha'] for commit in unsent_commits]
        save_commit_data(all_commits)
    except Exception as e:
        print(f"Failed to check commits and send message: {e}")

# Dictionary to store the channel IDs for each guild
welcome_leave_channels = {
    23423424242423424: 2342424234324,  # Guild ID : Channel ID -> remeber to place with actual guild and channel id´s 
}

@client.event
async def on_ready():
    print('Bot is ready.')
    await check_commits_and_send_message()

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

client.run("put your bot token here")
