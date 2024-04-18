import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from utils.github import check_commits_and_send_message  # Updated import statement

load_dotenv()

# Retrieve Discord bot token from environment variables
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)

# Load command files
import importlib

commands = {}

for file in os.listdir('./commands'):
    if file.endswith('.py'):
        module = importlib.import_module(f'commands.{os.path.splitext(file)[0]}')
        commands[module.execute.__command_name__] = module.execute

@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # Check for command
    if message.content.startswith('?'):
        args = message.content[1:].strip().split(' ')
        command_name = args.pop(0).lower()

        # Check if the command exists
        if command_name not in commands:
            await message.channel.send(f"{message.author.mention}, Tuntematon komento '{command_name}'. tee komento ?help nähdäksesi käytössä olevat komennot.")
            return

        # Execute the command
        command = commands[command_name]
        await command(message, args, bot, commands)

        # Delete the user's command message only for configured commands
        if command_name in ['clear', 'wiki', 'ping', 'troll', 'ehdotus']:  # Add other configured commands as needed
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass  # Message already deleted or not found

# Load events from the "events" folder
for filename in os.listdir('./events'):
    if filename.endswith('.py') and not filename.startswith('__'):
        event_module = __import__(f'events.{filename[:-3]}', fromlist=[''])
        if hasattr(event_module, 'setup'):
            event_module.setup(bot)

# Event: Triggered when the bot is ready
@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)

    # Run the task to check for new commits periodically
    while True:
        await check_commits_and_send_message(bot)
        await asyncio.sleep(10)  # Check every 10 minutes

# Run the bot
bot.run(BOT_TOKEN)
