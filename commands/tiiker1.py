import asyncio

# commands/tiiker1.py

async def execute(message, args, client, commands):
    # Check if the user invoking the command is authorized
    if message.author.id == 267240625596792833:
        # Delete the user's message
        await message.delete()

        # Send the activation message
        activation_message = await message.channel.send('Self-destruction activated. Initiating shutdown in 10 seconds...')
        
        # Introducing a 10-second delay using asyncio.sleep
        await asyncio.sleep(10)

        # Delete the activation message before shutting down
        await activation_message.delete()
        
        await client.close()

execute.__command_name__ = 'tiiker1'