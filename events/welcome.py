import discord
from config import guild_configs

async def on_member_join(member):
    # This function will be called when a member joins a server
    guild_id = member.guild.id

    # Check if the guild has a configuration
    if guild_id in guild_configs:
        guild_config = guild_configs[guild_id]
        welcome_channel_id = guild_config['welcome_channel_id']
        welcome_message = guild_config['welcome_message']

        # Fetch the channel
        welcome_channel = member.guild.get_channel(welcome_channel_id)

        if welcome_channel:
            # Send a welcome message to the channel
            await welcome_channel.send(welcome_message.format(member=member))
        else:
            print(f"Error: Welcome channel with ID {welcome_channel_id} not found.")
    else:
        print(f"Error: Guild configuration not found for guild ID {guild_id}.")

def setup(bot):
    bot.add_listener(on_member_join, 'on_member_join')
