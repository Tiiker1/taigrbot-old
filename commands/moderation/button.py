import discord
from discord.ext import commands
import asyncio
import json
import os

# Directory to save custom_options.json
DATA_DIR = "commit_data"

# File path for custom_options.json
CUSTOM_OPTIONS_FILE = os.path.join(DATA_DIR, "custom_options.json")

# Function to save custom options to JSON file
def save_custom_options():
    with open(CUSTOM_OPTIONS_FILE, "w") as file:
        json.dump(custom_options, file)

# Function to load custom options from JSON file
def load_custom_options():
    global custom_options
    if os.path.exists(CUSTOM_OPTIONS_FILE):
        with open(CUSTOM_OPTIONS_FILE, "r") as file:
            custom_options = json.load(file)
    else:
        custom_options = {}

def setup(client):

    async def toggle_role(member: discord.Member, role_name: str):
        print(f"Attempting to toggle role '{role_name}'")
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            print(f"Role '{role_name}' found")
            if role in member.roles:
                print(f"Removing role '{role_name}'")
                await member.remove_roles(role)
                return f"Role '{role_name}' removed successfully!"
            else:
                print(f"Adding role '{role_name}'")
                await member.add_roles(role)
                return f"Role '{role_name}' added successfully!"
        else:
            print(f"Role '{role_name}' not found in the server!")
            return f"Role '{role_name}' not found in the server!"

    # Call the function to load custom options
    load_custom_options()

    @client.tree.command()
    async def buttons(interaction: discord.Interaction):
        # Check if the user invoking the command has the allowed user ID
        allowed_user_id = 6546745645645645645  # Replace this with the allowed user ID
        if interaction.user.id != allowed_user_id:
            await interaction.response.send_message("Sorry, you are not authorized to use this command.")
            return

        # Get the guild ID
        guild_id = str(interaction.guild.id)

        # Get options based on whether custom options exist or not
        if guild_id in custom_options and custom_options[guild_id] is not None:
            options = custom_options[guild_id]
        else:
            options = ["Red", "Green", "Blue"]  # Default options

        # Create buttons for each option
        buttons = [discord.ui.Button(style=discord.ButtonStyle.primary, label=option, custom_id=f"{option.lower()}_button") for option in options]

        # Create a View and add the buttons
        view = discord.ui.View()
        for button in buttons:
            view.add_item(button)

        # Send message with the buttons
        await interaction.response.send_message("Please select a role:", view=view)

    @client.event
    async def on_interaction(interaction):
        if not interaction.type == discord.InteractionType.component:
            return

        try:
            custom_id = interaction.data.get("custom_id")
            member = interaction.user

            # Parse option name from custom ID
            option_name = custom_id.split("_")[0].capitalize()

            # Toggle the role or perform any other action based on the option
            result = await toggle_role(member, option_name)
            print(result)

            # Acknowledge the interaction with a placeholder message
            await interaction.response.send_message(content=result, ephemeral=True)

        except Exception as e:
            print(f"Error handling interaction: {e}")

    @client.tree.command()
    async def add_option(interaction: discord.Interaction, option: str):
        # Check if the user invoking the command has the allowed user ID
        allowed_user_id = 343434343434343  # Replace this with the allowed user ID
        if interaction.user.id != allowed_user_id:
            await interaction.response.send_message("Sorry, you are not authorized to use this command.")
            return

        # Get the guild ID
        guild_id = str(interaction.guild.id)

        # Initialize custom options list if it's None
        if guild_id not in custom_options or custom_options[guild_id] is None:
            custom_options[guild_id] = []

        # Add the option to custom_options dictionary
        custom_options[guild_id].append(option)
        await interaction.response.send_message(f"Option '{option}' added successfully.")

        save_custom_options()  # Save the changes
        print("Custom options after addition:", custom_options)  # Added logging

    @client.tree.command()
    async def remove_option(interaction: discord.Interaction, option: str):
        # Check if the user invoking the command has the allowed user ID
        allowed_user_id = 43434343434343  # Replace this with the allowed user ID
        if interaction.user.id != allowed_user_id:
            await interaction.response.send_message("Sorry, you are not authorized to use this command.")
            return

        # Get the guild ID
        guild_id = str(interaction.guild.id)

        # Remove the option from custom_options dictionary
        if guild_id in custom_options and option in custom_options[guild_id]:
            custom_options[guild_id].remove(option)
            await interaction.response.send_message(f"Option '{option}' removed successfully.")

            # If all custom options are removed, revert to default options
            if not custom_options[guild_id]:
                custom_options[guild_id] = None  # Set custom options to None
                await interaction.followup.send("All custom options removed. Reverting to default options.")
        else:
            await interaction.response.send_message(f"Option '{option}' not found.")

        save_custom_options()  # Save the changes
        print("Custom options after removal:", custom_options)  # Added logging

    @client.tree.command()
    async def list_options(interaction: discord.Interaction):
        # Check if the user invoking the command has the allowed user ID
        allowed_user_id = 343434343434343434  # Replace this with the allowed user ID
        if interaction.user.id != allowed_user_id:
            await interaction.response.send_message("Sorry, you are not authorized to use this command.")
            return

        # Get the guild ID
        guild_id = str(interaction.guild.id)

        # Get custom options for the guild or use default options
        options = custom_options.get(guild_id, ["Red", "Green", "Blue"])

        # Send the list of options as a message
        options_str = "\n".join(options)
        await interaction.response.send_message(f"Custom options for this server:\n{options_str}")
