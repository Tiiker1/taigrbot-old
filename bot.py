import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from github import check_commits_and_send_message  # Updated import statement

# Load environment variables
load_dotenv()

# Retrieve Discord bot token from environment variables
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Initialize intents to allow all intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with custom command prefix and intents
bot = commands.Bot(command_prefix='?', intents=intents)

# Load command files dynamically
import importlib

commands = {}

for file in os.listdir('./commands'):
    if file.endswith('.py'):
        module = importlib.import_module(f'commands.{os.path.splitext(file)[0]}')
        commands[module.execute.__command_name__] = module.execute

# Event: Triggered when a message is received
@bot.event
async def on_message(message):
    # Ignore messages from bots to prevent infinite loops
    if message.author.bot:
        return

    # Check if the message is a command
    if message.content.startswith('?'):
        args = message.content[1:].strip().split(' ')
        command_name = args.pop(0).lower()

        # Check if the command exists
        if command_name not in commands:
            await message.channel.send(f"{message.author.mention}, Unknown command '{command_name}'. Use ?help to see available commands.")
            return

        # Execute the command
        command = commands[command_name]
        await command(message, args, bot, commands)

        # Delete the user's command message for configured commands
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
    # Set bot presence
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('?help'))

    # Print bot name once it's logged in
    print('Logged in as', bot.user.name)

    # Run the task to check for new commits periodically
    while True:
        await check_commits_and_send_message(bot)
        await asyncio.sleep(600)  # Check every 10 minutes

# Run the bot
bot.run(BOT_TOKEN)
