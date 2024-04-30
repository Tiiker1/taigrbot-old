import discord
from discord.ext import commands

# Emojis for reactions
EMOJI_LETTERS = [chr(0x1F1E6 + i) for i in range(26)]

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
        
        # Check if the number of options exceeds the number of available emojis
        if len(options_list) > len(EMOJI_LETTERS):
            await ctx.response.send_message("Too many options provided. Maximum number of options allowed is {}.".format(len(EMOJI_LETTERS)))
            return
        
        # Create an embed for the poll message
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        
        # Add the options to the embed as fields with corresponding emojis
        for i, option in enumerate(options_list):
            embed.add_field(name=f"{EMOJI_LETTERS[i]} {option.strip()}", value="\u200b", inline=False)
        
        # Send the embed message and capture the sent message object
        poll_message = await ctx.channel.send(embed=embed)
        
        # Add reactions for each option
        for i in range(len(options_list)):
            await poll_message.add_reaction(EMOJI_LETTERS[i])
