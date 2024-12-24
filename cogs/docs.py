import discord
from discord.ext import commands
from discord import app_commands
from serpapi import GoogleSearch


class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_data(self, query):
        """Fetch documentation data using SerpAPI Google Search."""
        search = GoogleSearch({
            "q": f"{query} documentation",
            "location": "India",  # Adjust location as needed
            "api_key": "acef8007efe4c4c2fd5d61c5952659c010130bb47a631f84fa06cb7bbe1d2b30"
        })
        result = search.get_dict()
        return result

    @app_commands.command(name="docs", description="Search for documentation of a specific technology or topic")
    async def docs(self, interaction: discord.Interaction, query: str):
        """Search and display documentation-related results."""
        await interaction.response.defer()  # Defer the response to allow time for fetching data
        data = await self.fetch_data(query)

        # Handle API errors or empty results
        if not data or "error" in data:
            await interaction.followup.send("Unable to fetch data. Please try again later.")
            return

        organic_results = data.get("organic_results", [])
        if not organic_results:
            await interaction.followup.send(f"No documentation found for '{query}'.")
            return

        # Create an embed to display results
        embed = discord.Embed(
            title=f"Documentation for: {query}",
            description=f"Top search results for '{query}' documentation:",
            color=discord.Color.blue(),
        )

        # Add up to 5 results from organic results
        for result in organic_results[:5]:
            title = result.get("title", "No Title")
            link = result.get("link", "#")
            snippet = result.get("snippet", "No description available.")
            embed.add_field(name=title, value=f"{snippet}\n[Read More]({link})", inline=False)

        embed.set_footer(text="Powered by SerpAPI | Results may vary.")
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Docs(bot))
