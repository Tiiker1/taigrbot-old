# commands/kolikko.py
import random

async def execute(message, args, client, commands):
    result = random.choice(['Kruuna', 'Klaava'])
    await message.channel.send(f"Kolikon heiton tulos: {result}")

execute.__command_name__ = 'kolikko'
