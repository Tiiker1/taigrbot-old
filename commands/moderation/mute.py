import discord
from discord import app_commands

async def mute_command(interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
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

    # Mute the member
    try:
        await member.add_roles(muted_role, reason=reason)
        await interaction.response.send_message(f"{member.display_name} has been muted for: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to mute this user.")
    except discord.HTTPException:
        await interaction.response.send_message("An error occurred while trying to mute the user.")

def setup(client):
    client.tree.add_command(app_commands.Command(name="mute", description="Mute a member", callback=mute_command))
