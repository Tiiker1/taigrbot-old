# commands/kysely.py
import discord

async def execute(message, args, client, commands):
    question = ' '.join(args)

    if not question:
        return await message.reply('Esitä kysymys kyselyä varten.')

    author = message.author
    avatar_url = author.avatar.url if author.avatar else discord.Embed.Empty

    kysely_embed = discord.Embed(
        title='Kysely',
        description=f'**{question}**',
        color=0x7F00FF,  # You can change the color to your preference
    )
    kysely_embed.set_footer(text=f'Requested by {author.display_name}', icon_url=avatar_url)

    kysely_message = await message.channel.send(embed=kysely_embed)
    for emoji in ['👍', '👎']:
        await kysely_message.add_reaction(emoji)

# Assign the execute function to a 'name' attribute
execute.__command_name__ = 'kysely'