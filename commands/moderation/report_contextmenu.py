import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import os

# Define the path to the SQLite database file
DATABASE_FILE = 'databases/log_channels.db'

# Ensure the data folder exists
if not os.path.exists('databases'):
    os.makedirs('databases')

# Connect to the SQLite database
conn = sqlite3.connect(DATABASE_FILE)
c = conn.cursor()

# Create the log_channels table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS log_channels (
                guild_id TEXT PRIMARY KEY,
                channel_id INTEGER
             )''')
conn.commit()

def get_log_channel(guild_id):
    c.execute('SELECT channel_id FROM log_channels WHERE guild_id = ?', (str(guild_id),))
    result = c.fetchone()
    return result[0] if result else None

def set_log_channel(guild_id, channel_id):
    c.execute('REPLACE INTO log_channels (guild_id, channel_id) VALUES (?, ?)', (str(guild_id), channel_id))
    conn.commit()

def setup(client):
    @client.tree.context_menu(name='Report to Moderators')
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(
            'Thanks for reporting this message to our moderators.', ephemeral=True
        )

        # Retrieve the log channel for the guild where the command was invoked
        guild_id = interaction.guild.id
        log_channel_id = get_log_channel(guild_id)

        if log_channel_id is None:
            return await interaction.followup.send(
                'Reports channel not found. Please ask server staff to set it with /setreports <channelnamehere>', ephemeral=True
            )

        log_channel = client.get_channel(log_channel_id)
        if log_channel is None:
            return await interaction.followup.send(
                'Reports channel not found. Please check the channel ID in the settings.', ephemeral=True
            )

        # Create and send the embed
        embed = discord.Embed(title='Reported Message')
        if message.content:
            embed.description = message.content

        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.timestamp = message.created_at

        url_view = discord.ui.View()
        url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

        await log_channel.send(embed=embed, view=url_view)

    # Define the command to set the log channel for the guild
    @client.tree.command(name="setreports")
    @commands.guild_only()
    async def set_log_channel_command(interaction: discord.Interaction, channel: discord.TextChannel):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        # Proceed with the command logic if the user has administrator permissions
        set_log_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(f"Reports channel set to {channel.mention}", ephemeral=True)

# Don't forget to close the database connection when shutting down the bot
def close_connection():
    conn.close()

# Ensure to close the connection when the bot is shut down
import atexit
atexit.register(close_connection)
