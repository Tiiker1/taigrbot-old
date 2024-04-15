import discord
import requests
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Retrieve Discord bot token from environment variables
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# GitHub repository information
GITHUB_USERNAME = '-'
REPOSITORY_NAME = '-'

# Define gateway intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True

# Discord bot client
bot = discord.Client(intents=intents)

# Function to fetch recent commits from GitHub
def fetch_recent_commits():
    response = requests.get(f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/commits')
    return response.json()

# Function to check for new commits and send message to Discord
async def check_commits_and_send_message():
    commits = fetch_recent_commits()

    # Get the latest commit
    latest_commit_sha = commits[0]['sha']

    # Check if the latest commit is different from the previous one
    if latest_commit_sha != check_commits_and_send_message.latest_commit:
        check_commits_and_send_message.latest_commit = latest_commit_sha

        # Format commit information into a Discord message
        message = f'New commit in {REPOSITORY_NAME}: {commits[0]["commit"]["message"]}'

        # Post the message to the specified Discord channel
        channel_id = -  # Replace this with the actual channel ID
        channel = bot.get_channel(channel_id)
        await channel.send(message)

# Initialize the latest commit variable
check_commits_and_send_message.latest_commit = ''

# Event: Triggered when the bot is ready
@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)

    # Run the task to check for new commits periodically
    while True:
        await check_commits_and_send_message()
        await asyncio.sleep(600)  # Check every 10 minutes

# Run the bot
bot.run(BOT_TOKEN)