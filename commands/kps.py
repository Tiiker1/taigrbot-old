import random

async def execute(message, args, client, commands):
    choices = ['kivi', 'paperi', 'sakset']
    user_choice = args[0].lower() if args else random.choice(choices)
    bot_choice = random.choice(choices)

    if user_choice in choices:
        if user_choice == bot_choice:
            await message.channel.send(f'Tasapeli! Molemmat valitsi {bot_choice}.')
        elif (
            (user_choice == 'kivi' and bot_choice == 'sakset') or
            (user_choice == 'paperi' and bot_choice == 'kivi') or
            (user_choice == 'sakset' and bot_choice == 'paperi')
        ):
            await message.channel.send(f'Voitit! {message.author.mention} valitsi {user_choice}, ja botti valitsi {bot_choice}.')
        else:
            await message.channel.send(f'Hävisit! {message.author.mention} valitsi {user_choice}, mutta botti valitsi {bot_choice}.')
    else:
        await message.channel.send('Virheellinen valinta. valitse jokin seuraavista vaihtoehdoista: kivi, paperi, or sakset.')

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'kps'
