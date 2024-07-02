import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='permissions')
    async def permissions_command(interaction: discord.Interaction):
        
        # Check if the command invoker has administrative permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.")
            return

        # Define command categories by required permissions
        permission_categories = {
            "Administrator": [
                ("/xp_on", "Turns xp system on."),
                ("/xp_off", "Turns xp system off.")
            ],
            "Manage Roles": [
                ("/mute", "Mutes a user by assigning them the 'muted' role."),
                ("/unmute", "Unmutes a previously muted user by removing the 'muted' role."),
                ("/rolemenu", "Sends out a menu with clickable buttons for users to assign themselves roles."),
                ("/addrole <rolename>", "Adds a role button to the role menu."),
                ("/removerole <rolename>", "Removes a role button from the role menu.")
            ],
            "Manage Messages": [
                ("/clear <amount>", "Clears a defined amount of messages from the channel.")
            ],
            "Send Messages": [
                ("/setlogchannel <channel>", "Sets the channel where reported messages will be sent.")
            ]
        }

     # Create the main embed for permissions
        embed = discord.Embed(title="Bot Commands - Permissions Required", color=discord.Color.blue())
        embed.set_footer(text="Bot by tiiker1")  # Replace with your information

        # Add fields to the embed for each permission category
        for category, commands in permission_categories.items():
            command_list = "\n".join([f"`{command}` - {usage}" for command, usage in commands])
            embed.add_field(name=f"**Requires {category}**", value=command_list, inline=False)

        # Send the embed as a response to the interaction
        await interaction.response.send_message(embed=embed)
