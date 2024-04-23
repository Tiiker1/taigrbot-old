# commands/random.py

import random

async def execute(message, args, client, commands):
    random_number = random.randint(1, 100)
    await message.reply(f'Random Number: {random_number}')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'random'
