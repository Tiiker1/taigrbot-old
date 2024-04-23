# commands/clear.py
import discord

async def execute(message, args, client, commands):
    amount = int(args[0]) + 1

    if not amount or amount <= 1 or amount > 100:
        return await message.reply('Käytä numeroa väliltä 1-99 massapoistaaksesi viestejä.')

    try:
        # Check if the bot has the required permissions
        if not message.guild.me.guild_permissions.manage_messages:
            return await message.reply('Bot does not have the required permissions to manage messages.')

        # Check if the user has the required permissions
        if not message.author.guild_permissions.manage_messages:
            return await message.reply('You do not have the required permissions to manage messages.')

        deleted_messages = await message.channel.purge(limit=amount)
        await message.channel.send(f'Poistettu {len(deleted_messages) - 1} viestiä.')
    except Exception as error:
        print(error)
        await message.reply('Virhe tapahtui poistaessa viestejä.')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'clear'
