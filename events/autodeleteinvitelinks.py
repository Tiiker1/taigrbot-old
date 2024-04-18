import discord
from discord.ext import commands

# Dictionary to store user invite link counts
user_invite_counts = {}

# List of server IDs to be blacklisted
server_blacklist = [761154009557106699]

async def mute_user(user, guild):
    # Check if the guild is blacklisted
    if guild.id in server_blacklist:
        return

    # Check if a "Muted" role exists, if not, create one
    muted_role = discord.utils.get(guild.roles, name="muted")
    if not muted_role:
        # Specify the color (in this case, red)
        muted_role = await guild.create_role(name="muted", color=discord.Color.red())
        # Modify the permissions for the Muted role as needed

    # Add the Muted role to the user
    await user.add_roles(muted_role)

async def block_invite_links(message):
    if 'discord.gg/' in message.content:
        # Check if the author has the "Manage Messages" permission
        if message.author.guild_permissions.manage_messages:
            return

        user_id = message.author.id

        # Increment the user's invite link count
        user_invite_counts[user_id] = user_invite_counts.get(user_id, 0) + 1

        # Check if the user has sent 2 or more invite links
        if user_invite_counts[user_id] >= 2:
            try:
                # Delete the message
                await message.delete()
                # Inform the user that Discord invite links are not allowed
                await message.channel.send(f'{message.author.mention}, Kutsu linkkien lähettäminen ei ole sallittua tällä kanavalla.')
                # Mute the user
                await mute_user(message.author, message.guild)
                # Reset the user's invite link count
                user_invite_counts[user_id] = 0
            except discord.Forbidden:
                # Handle if the bot doesn't have permission to delete the message
                print("Virhe: Botilla ei ole oikeuksia poistaa viestiä.")
            except discord.HTTPException as e:
                # Handle other exceptions
                print(f"Virhe poistaessa viestejä.: {e}")
        else:
            try:
                # Delete the message
                await message.delete()
                # Inform the user that Discord invite links are not allowed
                await message.channel.send(f'{message.author.mention}, Kutsu linkkien lähettäminen ei ole sallittua tällä kanavalla.')
            except discord.Forbidden:
                # Handle if the bot doesn't have permission to delete the message
                print("Virhe: Botilla ei ole oikeuksia poistaa viestiä.")
            except discord.HTTPException as e:
                # Handle other exceptions
                print(f"Virhe poistaessa viestejä.: {e}")

def setup(bot):
    bot.add_listener(block_invite_links, 'on_message')