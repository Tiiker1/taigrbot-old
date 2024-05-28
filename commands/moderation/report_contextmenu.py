import discord
from discord.ext import commands
from discord import app_commands
import os
import json

# Define the path to the JSON file where log channel settings will be stored
LOG_CHANNELS_FILE = 'jsondata/log_channels.json'

# Ensure the jsondata folder exists
if not os.path.exists('jsondata'):
    os.makedirs('jsondata')

def load_log_channels():
    if os.path.exists(LOG_CHANNELS_FILE):
        with open(LOG_CHANNELS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_log_channels(log_channels):
    with open(LOG_CHANNELS_FILE, 'w') as file:
        json.dump(log_channels, file)

def setup(client):
    @client.tree.context_menu(name='Report to Moderators')
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(
            f'Thanks for reporting this message to our moderators.', ephemeral=True
        )

        # Retrieve the log channel for the guild where the command was invoked
        guild_id = interaction.guild.id
        log_channels = load_log_channels()
        log_channel_id = log_channels.get(str(guild_id))

        if log_channel_id is None:
            return await interaction.response.send_message(
                'Log channel not set for this server.', ephemeral=True
            )

        log_channel = client.get_channel(log_channel_id)
        if log_channel is None:
            return await interaction.response.send_message(
                'Log channel not found. Please check the channel ID in the settings.', ephemeral=True
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
    @client.tree.command(name="setreportschannel")
    @commands.guild_only()
    async def set_log_channel(interaction: discord.Interaction, channel: discord.TextChannel):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        # Proceed with the command logic if the user has administrator permissions
        log_channels = load_log_channels()
        guild_id = str(interaction.guild_id)
        log_channels[guild_id] = channel.id
        save_log_channels(log_channels)
        await interaction.response.send_message(f"Log channel set to {channel.mention}", ephemeral=True)
