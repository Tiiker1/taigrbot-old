# commands/ping.py

async def execute(message, args, client, commands):
    latency = round(client.latency * 1000)  # latency is in seconds, convert to milliseconds
    await message.channel.send(f'Pong! Latency: {latency}ms')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'ping'
