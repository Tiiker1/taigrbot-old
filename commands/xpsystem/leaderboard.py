import discord
from discord.ext import commands

def setup(client):
    @client.tree.command(name='leaderboard')
    async def leaderboard_command(interaction: discord.Interaction):
        guild_id = interaction.guild.id
        leaderboard = client.xp_database.get_leaderboard(guild_id)

        # Create a new embed with a title and color
        embed = discord.Embed(title="🏆 Leaderboard 🏆", color=discord.Color.gold())

        # Add a description to the embed
        embed.description = "Here are the top members of the server!"

        # Create sections for top 3 and the rest
        top_3 = ""
        others = ""

        for rank, (user_id, xp, level) in enumerate(leaderboard, start=1):
            user = interaction.guild.get_member(int(user_id))
            if user:
                # Format the user info and rank
                user_info = f"**{user.display_name}**#{user.discriminator}"
                if rank == 1:
                    top_3 += f"🥇 {user_info}\n**Level:** {level}\n**XP:** {xp}\n\n"
                elif rank == 2:
                    top_3 += f"🥈 {user_info}\n**Level:** {level}\n**XP:** {xp}\n\n"
                elif rank == 3:
                    top_3 += f"🥉 {user_info}\n**Level:** {level}\n**XP:** {xp}\n\n"
                else:
                    others += f"**#{rank} {user_info}**\n**Level:** {level}\n**XP:** {xp}\n\n"

        # Add fields for the top 3 and others
        if top_3:
            embed.add_field(name="Top 3", value=top_3, inline=False)
        if others:
            embed.add_field(name="Others", value=others, inline=False)

        # Handle case where leaderboard is empty
        if not leaderboard:
            embed.description = "No data available yet. Start chatting to get on the leaderboard!"

        # Set the footer of the embed
        embed.set_footer(text="Keep chatting to climb the leaderboard!", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        # Send the embed as a response
        await interaction.response.send_message(embed=embed)
