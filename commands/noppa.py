# commands/noppa.py

import random

async def execute(message, args, client, commands):
    result = random.randint(1, 6)
    await message.channel.send(f'Heitit: {result}!')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'noppa'
