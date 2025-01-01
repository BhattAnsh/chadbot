import discord
from discord import app_commands
from discord.ext import commands


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="youtube", description="Tag everyone with a YouTube link")
    async def youtube(self, interaction: discord.Interaction, link: str):
        # Ensure the link is a valid YouTube URL
        if not link.startswith("https://www.youtube.com/") and not link.startswith("https://youtu.be/"):
            await interaction.response.send_message("Please provide a valid YouTube link!", ephemeral=True)
            return

        # Defer the interaction
        await interaction.response.defer()

        # Send the message tagging everyone
        await interaction.channel.send(f"@everyone Check this out! 📹 {link}")

        # Confirm the action in an ephemeral message
        await interaction.followup.send("YouTube link shared with everyone!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(YouTube(bot))
