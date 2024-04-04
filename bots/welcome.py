import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

# Get channels
general_channel = int(os.getenv("general_channel"))

async def welcome(member):
    if member.bot:
        return

    user_dm_channel = await member.create_dm()
    # change the wqelcome message accordingly
    welcome_message = f"Hello {member.mention}! Welcome to **{member.guild.name}**"
    
    print('Member joined')

    await user_dm_channel.send(welcome_message)