import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='ahelp')
    async def help_command(interaction: discord.Interaction):

        # Check if the command invoker has permissions to manage roles
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.")
            return

        # Create an empty dictionary to store commands grouped by category
        command_categories = {
            "Moderation": [
                ("/mute", "Mutes user with role muted (requires manage roles permission)"),
                ("/unmute", "Unmutes user with removing muted role (requires manage roles permission)")
            ],
            "Role Management": [
                ("/buttons", "Sends out role menu"),
                ("/add_option <rolename>", "Adds role button"),
                ("/remove_option <rolename>", "Removes role button")
            ],
            "Utility": [
                ("/clear", "Clears defined amount of messages (requires manage messages permission)")
            ],
            "Contextmenu commands": [
                ("/setlogchannel <channel>", "sets where reported messages goes. usually mods etc channel")
            ]
        }

        # Create the embed and add fields for each category
        embed = discord.Embed(title="Adminstrative bot commands", color=discord.Color.blue())

        for category, commands in command_categories.items():
            command_list = "\n".join([f"`{command}` - {description}" for command, description in commands])
            embed.add_field(name=category, value=command_list, inline=False)

        await interaction.response.send_message(embed=embed)
