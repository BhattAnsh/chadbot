import discord

def create_embed(title, description, color=discord.Color.blue()):
    """Create a basic embed with the given parameters"""
    return discord.Embed(title=title, description=description, color=color)

def format_duration(seconds):
    """Format duration in seconds to a readable string"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {seconds}s"