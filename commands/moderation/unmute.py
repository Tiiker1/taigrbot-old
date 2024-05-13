import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='unmute')
    async def unmute_command(interaction: discord.Interaction, member: discord.Member):
        # Check if the command invoker has permissions to manage roles
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You don't have permission to use this command.")
            return
        
        # Check if the bot has permissions to manage roles
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("I don't have permission to manage roles.")
            return
        
        # Get the muted role
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            await interaction.response.send_message("Muted role not found. Please create a role named 'Muted'.")
            return
        
        # Check if the member is currently muted
        if muted_role not in member.roles:
            await interaction.response.send_message("This user is not currently muted.")
            return
        
        # Unmute the member
        try:
            await member.remove_roles(muted_role)
            await interaction.response.send_message(f"{member.display_name} has been unmuted.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to unmute this user.")
        except discord.HTTPException:
            await interaction.response.send_message("An error occurred while trying to unmute the user.")
