import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='ahelp')
    async def help_command(interaction: discord.Interaction):

        # Check if the command invoker has permissions to manage roles
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.")
            return

        embed = discord.Embed(title="Adminstrative bot commands")
        embed.add_field(name="/button", value="creates role menu (for now only avaible thru Tiiker1)", inline=False)
        embed.add_field(name="/mute", value="Mutes user with role muted (reguires manage role permissions)", inline=False)
        embed.add_field(name="/unmute", value="Unmutes user with removing muted role (requires manage roles permission)", inline=False)
        embed.add_field(name="/clear", value="clears defined amount of messages (requires manage messages permission)", inline=False)
        await interaction.response.send_message(embed=embed)
