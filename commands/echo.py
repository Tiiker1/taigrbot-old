# commands/echo.py

async def execute(message, args, client, commands):
    if not args:
        return await message.reply('Lisää viesti joka echotaan.')

    echoed_message = ' '.join(args)
    await message.channel.send(f'You said: {echoed_message}')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'echo'
