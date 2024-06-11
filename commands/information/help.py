import discord
from discord.ext import commands

COMMANDS = {
    "General": {
        "/help": "Shows all available commands",
        "/ahelp": "Shows available administrative commands"
    },
    "XP System": {
        "/xp": "Shows how much XP you or another user has",
        "/leaderboard": "Shows the leaderboard"
    },
    "Utilities": {
        "/poll": "Creates a poll",
        "/review": "Creates a product review with assisted fields"
    }
}

def setup(client: commands.Bot):
    @client.tree.command(name='help')
    async def help_command(interaction: discord.Interaction):
        embed = discord.Embed(title="Bot Commands", color=discord.Color.blurple())
        for category, cmds in COMMANDS.items():
            cmd_list = "\n".join([f"`{cmd}` - {desc}" for cmd, desc in cmds.items()])
            embed.add_field(name=category, value=cmd_list, inline=False)
        await interaction.response.send_message(embed=embed)
