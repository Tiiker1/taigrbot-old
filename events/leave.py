import discord
from config import guild_configs

async def on_member_remove(member):
    # This function will be called when a member leaves the server

    # Check if the member left a configured guild
    guild_id = member.guild.id
    if guild_id in guild_configs:
        guild_config = guild_configs[guild_id]
        leave_channel_id = guild_config.get('leave_channel_id')
        goodbye_message = guild_config.get('goodbye_message', '{member.display_name} has left the server. Goodbye!')

        # Check if leave_channel_id is configured for the guild
        if leave_channel_id:
            # Fetch the channel
            leave_channel = member.guild.get_channel(leave_channel_id)

            if leave_channel:
                await leave_channel.send(goodbye_message.format(member=member))
            else:
                print(f"Error: Log channel with ID {leave_channel_id} not found.")
        else:
            print(f"Error: Leave channel ID not configured for guild {guild_id}.")
    else:
        print(f"Error: Guild configuration not found for guild ID {guild_id}.")

def setup(bot):
    bot.add_listener(on_member_remove, 'on_member_remove')
