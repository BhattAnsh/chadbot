import discord
from discord import app_commands
from discord.ext import commands
import aiohttp  # For asynchronous HTTP requests


class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_data(self, url):
        """Fetch data from GitHub API and handle errors."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return {"error": f"GitHub API returned status {response.status}"}
                return await response.json()

    @app_commands.command(name="profile", description="Get user GitHub details")
    async def profile(self, interaction: discord.Interaction, profile: str):
        """Fetch and display GitHub profile details."""
        url = f"https://api.github.com/users/{profile}"
        user_data = await self.fetch_data(url)

        if "error" in user_data:
            await interaction.response.send_message(user_data["error"])
            return

        if "message" in user_data and user_data["message"] == "Not Found":
            await interaction.response.send_message(f"User '{profile}' not found on GitHub.")
            return

        embed = discord.Embed(
            title=f"GitHub Profile: {user_data.get('login', 'Unknown')}",
            url=user_data.get("html_url", ""),
            description=user_data.get("bio", "No bio available."),
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=user_data.get("avatar_url", ""))
        embed.add_field(name="Name", value=user_data.get("name", "N/A"), inline=True)
        embed.add_field(name="Public Repos", value=user_data.get("public_repos", 0), inline=True)
        embed.add_field(name="Public Gists", value=user_data.get("public_gists", 0), inline=True)
        embed.add_field(name="Followers", value=user_data.get("followers", 0), inline=True)
        embed.add_field(name="Following", value=user_data.get("following", 0), inline=True)
        embed.add_field(name="Blog", value=user_data.get("blog", "N/A"), inline=False)
        embed.add_field(name="Account Created", value=user_data.get("created_at", "N/A"), inline=False)
        embed.set_footer(text="GitHub API | Data might be cached.")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="repos", description="Get public repositories of a user")
    async def repos(self, interaction: discord.Interaction, profile: str):
        """Fetch and display a user's public repositories."""
        url = f"https://api.github.com/users/{profile}/repos"
        repos = await self.fetch_data(url)

        if "error" in repos:
            await interaction.response.send_message(repos["error"])
            return

        if isinstance(repos, dict) and "message" in repos and repos["message"] == "Not Found":
            await interaction.response.send_message(f"User '{profile}' not found or has no public repositories.")
            return

        embed = discord.Embed(
            title=f"{profile}'s Public Repositories",
            color=discord.Color.green(),
        )

        for repo in repos[:10]:  # Display only the first 10 repositories
            embed.add_field(
                name=repo["name"],
                value=f"[Visit Repo]({repo['html_url']})\n⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}",
                inline=False,
            )

        embed.set_footer(text="GitHub API | Data might be cached.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stars", description="Get repositories starred by a user")
    async def stars(self, interaction: discord.Interaction, profile: str):
        """Fetch and display repositories starred by a user."""
        url = f"https://api.github.com/users/{profile}/starred"
        starred = await self.fetch_data(url)

        if "error" in starred:
            await interaction.response.send_message(starred["error"])
            return

        if isinstance(starred, dict) and "message" in starred and starred["message"] == "Not Found":
            await interaction.response.send_message(f"User '{profile}' not found or has not starred any repositories.")
            return

        embed = discord.Embed(
            title=f"{profile}'s Starred Repositories",
            color=discord.Color.purple(),
        )

        for repo in starred[:10]:  # Display only the first 10 starred repositories
            embed.add_field(
                name=repo["name"],
                value=f"[Visit Repo]({repo['html_url']}) by {repo['owner']['login']}\n⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}",
                inline=False,
            )

        embed.set_footer(text="GitHub API | Data might be cached.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="events", description="Get recent events of a user")
    async def events(self, interaction: discord.Interaction, profile: str):
        """Fetch and display recent public events of a user."""
        url = f"https://api.github.com/users/{profile}/events/public"
        events = await self.fetch_data(url)

        if "error" in events:
            await interaction.response.send_message(events["error"])
            return

        if isinstance(events, dict) and "message" in events and events["message"] == "Not Found":
            await interaction.response.send_message(f"User '{profile}' not found or has no public events.")
            return

        embed = discord.Embed(
            title=f"{profile}'s Recent Public Events",
            color=discord.Color.orange(),
        )

        for event in events[:5]:  # Display only the latest 5 events
            repo_name = event["repo"]["name"]
            event_type = event["type"]
            embed.add_field(
                name=repo_name,
                value=f"Event: {event_type}\n[View Repo](https://github.com/{repo_name})",
                inline=False,
            )

        embed.set_footer(text="GitHub API | Data might be cached.")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Github(bot))
