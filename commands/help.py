import discord

# commands/help.py

async def execute(message, args, client, commands):
    # Create an embed message
    embed = discord.Embed(
        title='Lista saatavilla olevista komennoista🚀',
        description='Tässä on lista kaikista käytettävissä olevista komennoista ryhmiteltynä kategorioittain.',
        color=0xb977ff  # Light purple color
    )

    # Define command categories and associated commands with descriptions
    categories = {
        'Yleiset': {
            '?ping': 'Tarkistaa botin latenssin',
            '?troll': 'Lähettää trollface gifin',
            '?echo': 'Toistaa annetun tekstin',
            '?random': 'Lähettää satunnaisen numeron 1-100',
        },
        'Hallinta': {
            '?clear': 'Poistaa viestejä 1-99',
            '?kysely': 'Luo kyselyn',
            '?ehdotus': 'Luo äänestyksen ehdotuksesta',
        },
        'Pelit': {
            '?noppa': 'Heittää noppaa ja kertoo tuloksen.',
            '?kolikko': 'Heittää kolikkoa ja kertoo tuloksen',
            '?rps <kivi sakset tai paperi>': 'Pelaa kivi sakset paperi pelin bottia vastaan',
        },
        'Informaatio': {
            '?wiki <hakusana>': 'Hakee lyhyen tiivistelmän Wikipedia-artikkelista',
            '?serverinfo': 'Kertoo tietoja palvelimesta',
            '?userinfo': 'Näyttää saatavilla olevat komennot',
            '?botinfo': 'näyttää botin tiedot(vain Tiiker1 voi suorittaa tämän komennon)',
        },
        'Apua': {
            '?help': 'Näyttää saatavilla olevat komennot',
        },
    }

    # Add command information to the embed
    for category, commands_dict in categories.items():
        command_list = '\n'.join([f'`{cmd}` - {desc}' for cmd, desc in commands_dict.items()])
        embed.add_field(name=f'**{category}**', value=command_list, inline=False)

    # Add a thumbnail (you can customize this URL)
    embed.set_thumbnail(url='https://i.imgur.com/YourCoolIcon.png')

    # Set the footer with additional information
    embed.set_footer(
        text='taigrfull | Dev',
        icon_url='https://i.imgur.com/FooterIcon.png'  # Customize the footer icon URL
    )

    # Set a timestamp for the embed (current time)
    embed.timestamp = message.created_at

    # Send the embed message
    await message.channel.send(embed=embed)

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'help'
