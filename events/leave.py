async def on_member_remove(member, bot_message_channel_id):
    # Retrieve the bot message channel for the current server
    bot_message_channel = member.guild.get_channel(bot_message_channel_id)
    
    # Check if the bot message channel exists
    if bot_message_channel is not None:
        # Send a goodbye message to the bot message channel mentioning the removed member
        await bot_message_channel.send(f'Goodbye {member.mention}!')

def setup(bot, bot_message_channel_id):
    # Add the on_member_remove event listener to the bot
    # This event listener will be triggered when a member leaves the server
    bot.add_listener(on_member_remove)
