import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            application_id=os.getenv('APPLICATION_ID')
        )
        self.initial_extensions = [
            'cogs.admin',
            'cogs.fun',
            'cogs.moderation',
            'cogs.utility',
            'cogs.github',
            'cogs.news'

        ]

    async def setup_hook(self):
        print("Setting up bot...")
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                print(f"Loaded extension {ext}")
            except Exception as e:
                print(f"Failed to load extension {ext}: {e}")

        print("Syncing commands...")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')
        await self.change_presence(
            activity=discord.Game(name="!help for commands")
        )

async def main():
    async with Bot() as bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
