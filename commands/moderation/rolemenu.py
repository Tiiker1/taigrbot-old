import discord
from discord.ext import commands
from discord import app_commands
import os
import sqlite3

# Ensure the databases folder exists
if not os.path.exists("databases"):
    os.makedirs("databases")

def init_database():
    conn = sqlite3.connect("databases/roledata.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS options
                 (guild_id TEXT, option TEXT)''')
    conn.commit()

    conn.close()

def add_option_to_database(guild_id, option):
    conn = sqlite3.connect("databases/roledata.db")
    c = conn.cursor()

    c.execute("INSERT INTO options (guild_id, option) VALUES (?, ?)", (guild_id, option))
    conn.commit()

    conn.close()

def remove_option_from_database(guild_id, option):
    conn = sqlite3.connect("databases/roledata.db")
    c = conn.cursor()

    c.execute("DELETE FROM options WHERE guild_id=? AND option=?", (guild_id, option))
    conn.commit()

    conn.close()

def get_options_from_database(guild_id):
    conn = sqlite3.connect("databases/roledata.db")
    c = conn.cursor()

    c.execute("SELECT option FROM options WHERE guild_id=?", (guild_id,))
    options = [row[0] for row in c.fetchall()]

    conn.close()

    return options

class RoleMenuView(discord.ui.View):
    def __init__(self, options):
        super().__init__(timeout=None)  # Persistent view
        for option in options:
            button = discord.ui.Button(style=discord.ButtonStyle.primary, label=option, custom_id=f"{option.lower()}_button")
            button.callback = self.create_callback(option)
            self.add_item(button)

    def create_callback(self, role_name):
        async def callback(interaction: discord.Interaction):
            guild = interaction.guild
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                await interaction.response.send_message(f"Role '{role_name}' not found.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f"Role '{role_name}' removed.", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Role '{role_name}' added.", ephemeral=True)
        
        return callback

def setup(client):
    init_database()

    # Function to check if the user has the Manage Roles permission
    def has_manage_roles_permission(interaction: discord.Interaction) -> bool:
        return interaction.user.guild_permissions.manage_roles

    # Decorator for the check
    def manage_roles_required():
        return app_commands.check(has_manage_roles_permission)

    @client.tree.command()
    @manage_roles_required()
    async def addrole(interaction: discord.Interaction, option: str):
        guild_id = str(interaction.guild.id)
        add_option_to_database(guild_id, option)
        await interaction.response.send_message(f"Option '{option}' added successfully.")

    @client.tree.command()
    @manage_roles_required()
    async def removerole(interaction: discord.Interaction, option: str):
        guild_id = str(interaction.guild.id)
        remove_option_from_database(guild_id, option)
        await interaction.response.send_message(f"Option '{option}' removed successfully.")

    @client.tree.command()
    @manage_roles_required()
    async def listroles(interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        options = get_options_from_database(guild_id)
        if not options:
            options = ["Red", "Green", "Blue"]  # Default options

        options_str = "\n".join(options)
        await interaction.response.send_message(f"Custom roles for this server:\n{options_str}")

    @client.tree.command()
    @manage_roles_required()
    async def rolemenu(interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        options = get_options_from_database(guild_id)
        if not options:
            options = ["Red", "Green", "Blue"]  # Default options

        view = RoleMenuView(options)
        await interaction.response.send_message("Press a button to get the role:", view=view)

    # Error handler for permission check failures
    @client.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You do not have the necessary permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred while processing the command.", ephemeral=True)
