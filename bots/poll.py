import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
poll_channel_id = int(os.getenv("poll_channel"))

@bot.command(name='poll', help='Create a poll. Use: !poll "Question" "Option 1" "Option 2" ...')
async def poll(ctx, question, *options):
    # Check if the command is invoked in the poll channel
    if ctx.channel.id != poll_channel_id:
        await ctx.send('Polls can only be created in the designated poll channel.')
        return

    if len(options) < 2 or len(options) > 9:
        await ctx.send('Please provide at least 2 options and no more than 9 options for the poll.')
        return

    formatted_options = '\n'.join([f'{index + 1}. {option}' for index, option in enumerate(options)])
    poll_message = f'{question}\n\n{formatted_options}'

    poll_embed = discord.Embed(title='Poll', description=poll_message, color=0x3498db)

    poll_msg = await ctx.send(embed=poll_embed)

    for emoji in range(1, len(options) + 1):
        await poll_msg.add_reaction(f'{emoji}\ufe0f\u20e3')
