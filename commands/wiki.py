import wikipedia

async def execute(message, args, client, commands):
    if not args:
        await message.channel.send('Kirjoita aihe Wikipedia hakua varten.')
        return

    search_query = ' '.join(args)
    try:
        summary = wikipedia.summary(search_query, sentences=2)
        await message.channel.send(f'Wikipedia haku aiheelle "{search_query}":\n{summary}')
    except wikipedia.exceptions.DisambiguationError as e:
        await message.channel.send(f'Useampia osumia löytyi. Tarkenna aihetta: {", ".join(e.options)}')
    except wikipedia.exceptions.PageError:
        await message.channel.send(f'Ei tuloksia haulle "{search_query}" Wikipediassa.')

execute.__command_name__ = 'wiki'