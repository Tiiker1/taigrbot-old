# commands/ehdotus.py
import discord

async def execute(message, args, client, commands):
    question = ' '.join(args)

    if not question:
        return await message.reply('Esitä Ehdotus.')

    author = message.author
    avatar_url = author.avatar.url if author.avatar else discord.Embed.Empty

    ehdotus_embed = discord.Embed(
        title='Ehdotus',
        description=f'**{question}**',
        color=0x7F00FF,  # You can change the color to your preference
    )
    ehdotus_embed.set_footer(text=f'Requested by {author.display_name}', icon_url=avatar_url)

    ehdotus_message = await message.channel.send(embed=ehdotus_embed)
    for emoji in ['👍', '👎']:
        await ehdotus_message.add_reaction(emoji)

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'ehdotus'
