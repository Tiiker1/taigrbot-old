import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='help')
    async def help_command(interaction: discord.Interaction):
        embed = discord.Embed(title="Bot Commands")
        embed.add_field(name="/help", value="Shows all avaible commands", inline=False)
        embed.add_field(name="/poll", value="Creates poll", inline=False)
        embed.add_field(name="/review", value="creates product review with assisted fields", inline=False)
        embed.add_field(name="/visitturku", value="sends events from visitturku.fi", inline=False)
        await interaction.response.send_message(embed=embed)
