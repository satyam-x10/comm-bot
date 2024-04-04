import discord
from discord.ext import commands, tasks
import datetime
import asyncio

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Define Hourly Limits
warnLimitPerHour = 1
muteLimitPerHour = 2
BanLimit = 2
timeoutDuration = 2  #in seconds
muteRoleId = 1171347050424717362

# Dictionary to store user message counts and timeout counts
user_data = {}

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    if user_id not in user_data:
        user_data[user_id] = {
            'message_count': 0, 'mute_count': 0, 'timestamp': datetime.datetime.now()}

    # Check if it's a new hour, reset counts 
    current_timestamp = datetime.datetime.now()
    if (current_timestamp - user_data[user_id]['timestamp']).seconds >= 3600:
        user_data[user_id] = {'message_count': 0,
                              'mute_count': 0, 'timestamp': current_timestamp}

    # Update message count and timestamp
    user_data[user_id]['message_count'] += 1
    user_data[user_id]['timestamp'] = current_timestamp

    # Check for spam and timeout/mute if necessary
    if user_data[user_id]['mute_count'] > BanLimit:
        user = await bot.fetch_user(int(user_id))
        await message.guild.ban(user, reason=f"Exceeded Ban Limit ({BanLimit})")
        await message.channel.send(f" {message.author.mention} has been banned due to excessive messaging.")
        
    elif user_data[user_id]['message_count'] > muteLimitPerHour:
        reason = 'excessive spamming'
        
        # Assign the mute role to the user
        mute_role = message.guild.get_role(muteRoleId)
        await message.author.add_roles(mute_role, reason=reason)
        await message.channel.send(f"{message.author.mention} has been muted for {timeoutDuration} seconds due to excessive spamming. Further violations may result in a ban.")
        
        # Make sure 'mute_count' key exists before incrementing
        user_data.setdefault(user_id, {}).setdefault('mute_count', 0)
        user_data[user_id]['mute_count'] += 1

        # You may want to implement a way to remove the mute role after the timeoutDuration
        await asyncio.sleep(timeoutDuration)
        await message.author.remove_roles(mute_role, reason=f"Mute duration ({timeoutDuration} seconds) expired.")
                
    elif user_data[user_id]['message_count'] > warnLimitPerHour:
        await message.channel.send(f"Warning: {message.author.mention}, you have sent {user_data[user_id]['message_count']} messages in the last hour. Please avoid excessive messaging.")

    # Process commands
    await bot.process_commands(message)

# Command to check message count
@bot.command(name='messagecount')
async def message_count(ctx):
    user_id = str(ctx.author.id)
    count = user_data.get(user_id, {'message_count': 0})['message_count']
    await ctx.send(f"{ctx.author.mention}, you have sent {count} messages in the last hour.")

# Hourly reset task
@tasks.loop(hours=1)
async def hourly_reset():
    for user_id in user_data:
        user_data[user_id]['message_count'] = 0
    hourly_reset.start() 

