import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.send_message(f'{member.mention} has been warned for: {reason}')

    @app_commands.command(name="timeout", description="Timeout a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = None):
        await member.timeout(duration=minutes*60, reason=reason)
        await interaction.response.send_message(
            f'{member.mention} has been timed out for {minutes} minutes. Reason: {reason}',
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
