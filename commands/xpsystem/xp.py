import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='xp')
    async def xp_command(interaction: discord.Interaction, user: discord.User = None):
        guild_id = interaction.guild.id
        user_id = user.id if user else interaction.user.id
        user_data = client.xp_database.get_user_data(guild_id, user_id)
        xp = user_data["xp"]
        level = user_data["level"]
        await interaction.response.send_message(f"{user.mention if user else interaction.user.mention} has {xp} XP and is at level {level} in this server")
