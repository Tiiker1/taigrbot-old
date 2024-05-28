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
            "**Moderation**": [
                ("/mute", 
                 "Mutes a user by assigning them the 'muted' role.", 
                 "Requires `Manage Roles` permission."
                ),
                ("/unmute", 
                 "Unmutes a previously muted user by removing the 'muted' role.", 
                 "Requires `Manage Roles` permission."
                )
            ],
            "**Role Management**": [
                ("/buttons", 
                 "Sends out a menu with clickable buttons for users to assign themselves roles.", 
                 "Requires `Manage Roles` permission."
                ),
                ("/add_option <rolename>", 
                 "Adds a role button to the role menu.", 
                 "Requires `Manage Roles` permission."
                ),
                ("/remove_option <rolename>", 
                 "Removes a role button from the role menu.", 
                 "Requires `Manage Roles` permission."
                )
            ],
            "**Utility**": [
                ("/clear", 
                 "Clears a defined amount of messages from the channel.", 
                 "Requires `Manage Messages` permission."
                )
            ],
            "**Contextmenu commands**": [
                ("/setlogchannel <channel>", 
                 "Sets the channel where reported messages will be sent.", 
                 "Requires `Send Messages` permission."
                )
            ]
        }

        # Create the embed and add fields for each category
        embed = discord.Embed(title="Adminstrative bot commands", color=discord.Color.blue())

        color_mapping = {
            "**Moderation**": discord.Color.gold(),
            "**Role Management**": discord.Color.green(),
            "**Utility**": discord.Color.orange(),
            "**Contextmenu commands**": discord.Color.teal()
        }

        for category, commands in command_categories.items():
            color = color_mapping.get(category, discord.Color.blue())
            command_list = "\n".join([f"**Command:** `{command}`\n**Description:** {description}\n**Permissions:** {permission}\n" 
                                      for command, description, permission in commands])
            embed.add_field(name=f"{category}\n", value=command_list, inline=False)
            embed.set_footer(text="Permissions are required as indicated.")
            embed.color = color  # Set embed color for each category

        await interaction.response.send_message(embed=embed)
