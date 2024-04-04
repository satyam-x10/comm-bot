import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def create_channel(ctx, channel_name, duration: float):
    guild = ctx.guild
    existing_channel = discord.utils.get(
        guild.voice_channels, name=channel_name)

    if not existing_channel:
        # Create a new voice channel
        new_channel = await guild.create_voice_channel(channel_name)
        await ctx.send(f'Voice channel "{channel_name}" created!')

        # Schedule channel deletion after the specified duration
        await asyncio.sleep(duration * 3600)  # Convert hours to seconds
        await new_channel.delete()
        await ctx.send(f'Voice channel "{channel_name}" deleted after {duration} hours.')
    else:
        await ctx.send(f'A voice channel with the name "{channel_name}" already exists.')
