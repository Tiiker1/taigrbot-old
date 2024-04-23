# commands/troll.py

async def execute(message, args, client, commands):
    await message.channel.send('https://images-ext-2.discordapp.net/external/QcCjcHHsFfplLAZeWpH6JsrtunKRWLD5TdpGB3DCe3Y/https/media.tenor.com/3f87UxkcPREAAAPo/troll-troll-face.mp4')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'troll'


