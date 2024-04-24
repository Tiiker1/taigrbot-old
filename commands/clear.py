import discord
from discord.ext import commands

def setup(client):
    @client.tree.command()
    async def clear(interaction: discord.Interaction, amount: int):
        """Clears the specified number of messages."""
        # Send an initial response to acknowledge the command
        initial_response = await interaction.response.send_message("Started clearing messages please wait..", ephemeral=False)

        # Perform the message purge operation
        await interaction.channel.purge(limit=amount + 1)

        # Send a follow-up message indicating that the messages were cleared
        followup_message = await interaction.followup.send(f'{amount} messages were cleared by {interaction.user.mention}', ephemeral=False)

        # Attempt to delete the initial response message if it was sent successfully
        if initial_response:
            try:
                await initial_response.delete()
            except discord.NotFound:
                print("Initial response message not found.")
