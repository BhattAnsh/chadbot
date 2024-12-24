import discord
from discord import app_commands
from discord.ext import commands
import aiohttp  # For asynchronous HTTP requests
from json import loads


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_data(self, url):
        """Fetch data from the Ok.surf API and handle errors."""
        async with aiohttp.ClientSession() as session:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return {"error": f"API returned status {response.status}"}
                return await response.json()

    @app_commands.command(name="technews", description="Get the latest tech news")
    async def technews(self, interaction: discord.Interaction):
        """Fetch and display the latest tech-related news."""
        url = "https://ok.surf/api/v1/news-feed"

        news_data = await self.fetch_data(url)

        if "error" in news_data:
            await interaction.response.send_message(news_data["error"])
            return

        if not news_data.get("data"):
            await interaction.response.send_message("No tech-related news available at the moment.")
            return

        embed = discord.Embed(
            title="Latest Tech News",
            color=discord.Color.blue(),
        )

        for article in news_data["data"][:5]:  # Display the first 5 articles
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            url = article.get("url", "#")
            embed.add_field(
                name=title,
                value=f"{description}\n[Read more]({url})",
                inline=False,
            )

        embed.set_footer(text="Data powered by Ok.surf | Tech News")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(News(bot))
