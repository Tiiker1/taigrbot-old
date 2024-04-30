import discord
from discord.ext import commands

def setup(client):
    @client.tree.command()
    async def poll(ctx: discord.Interaction, question: str, options: str):
        """Starts a poll with a question and multiple options."""
        # Split the options string into a list
        options_list = options.split(',')
        
        # Check if the user provided at least two options
        if len(options_list) < 2:
            await ctx.response.send_message("Please provide at least two options for the poll.")
            return
        
        # Format the poll message
        poll_message = f"**Poll:** {question}\n\n"
        for index, option in enumerate(options_list, start=1):
            poll_message += f"{index}. {option.strip()}\n"
        
        # Send the poll message and capture the sent message object
        poll = await ctx.channel.send(poll_message)
        
        # Add reactions for each option
        for index in range(len(options_list)):
            await poll.add_reaction(chr(0x1F1E6 + index))
