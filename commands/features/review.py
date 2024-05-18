import discord
from discord import app_commands

def setup(client):
    @client.tree.command()
    async def review(interaction: discord.Interaction, product: str, rating: int, review_text: str):
        """Submit a review with a rating for a product."""
        if rating < 1 or rating > 5:
            await interaction.response.send_message("Rating must be between 1 and 5.", ephemeral=True)
            return
        
        review_channel = discord.utils.get(interaction.guild.text_channels, name='reviews')
        if review_channel:
            embed = discord.Embed(title=f"Review for {product}", description=review_text, color=discord.Color.blue())
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            embed.add_field(name="Rating", value=f"{rating} / 5")
            await review_channel.send(embed=embed)
            await interaction.response.send_message("Your review has been submitted.", ephemeral=True)
        else:
            await interaction.response.send_message("Review channel not found. Please create a channel named 'reviews'.", ephemeral=True)
