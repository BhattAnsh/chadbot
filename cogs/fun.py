import discord
from discord import app_commands
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask the magic 8ball a question")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.", "Without a doubt.", "Yes definitely.",
            "You may rely on it.", "As I see it, yes.", "Most likely.",
            "Better not tell you now.", "Cannot predict now.",
            "Don't count on it.", "My reply is no.", "Very doubtful."
        ]
        await interaction.response.send_message(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @app_commands.command(name="roll", description="Roll a dice")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        result = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 You rolled a {result}!")

    @app_commands.command(name="flip", description="Flip a coin")
    async def flip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"🪙 {result}!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
