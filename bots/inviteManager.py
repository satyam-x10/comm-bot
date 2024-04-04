import discord
from bots.welcome import welcome
from dotenv import load_dotenv
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Get channels
load_dotenv()

leaderboard_channel = int(os.getenv("leaderboard_channel"))
general_channel = int(os.getenv("general_channel"))

invites = {}

# Load Invites
def loadinvites():
    
    try:
        with open("invites.txt") as f:
            for line in f:

                data = line.strip().split(";")
                author_id, invite_url, uses, *users = data
                users = [int(user) for user in users if user]
                invites[author_id] = {"url": invite_url, "uses": int(uses), "users": users}

    except FileNotFoundError:
        pass

# Update Invites
def update_invites_file():

    with open("./data/invites.txt", "w") as f:

        for author_id, invite_data in invites.items():
            f.write(f"{author_id};{invite_data['url']};{invite_data['uses']};{';'.join(map(str, invite_data['users']))}\n")

# On Join
@bot.event
async def on_member_join(member):

    await welcome(member=member)
    
    guild = member.guild
    invite = None
    invite_list = await guild.invites()
    most_recent = None
    max_timestamp = 0

    # Find the most recently created invite
    for inv in invite_list:
        if inv.uses > 0 and inv.created_at.timestamp() > max_timestamp:
            max_timestamp = inv.created_at.timestamp()
            most_recent = inv

    if most_recent:
        for author_id, invite_data in invites.items():
            # If the invite URL matches, update invite count
            if invite_data['url'] == most_recent.url:
                invites[author_id]["uses"] += 1
                invites[author_id]["users"].append(member.id)
                invited_by = guild.get_member(int(author_id))
                invites_amount = invite_data["uses"]
                break


    else:
        invited_by = None
        invites_amount = None

    update_invites_file()

# On Leave
@bot.event
async def on_member_remove(member):

    
    for author_id, invite_data in invites.items():
        if member.id in invite_data["users"]:
            invites[author_id]["uses"] -= 1
            invites[author_id]["users"].remove(member.id)
            update_invites_file()
            break

# Display list of commands
@bot.command(description="Displays all available commands.")
async def commandslist(ctx):
    command_list = "Available Commands:\n"

    for command in bot.commands:
        command_list += f"**{command.name}**: {command.description}\n"

    await ctx.send(command_list)

# Create Invites
@bot.command(description="Creates an invite for you.")
async def createinvite(ctx):
    # Check if the command was written in a specific channel
    allowed_channel_id = leaderboard_channel
   
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("This command is only allowed in a specific channel.")
        return

    author_id = str(ctx.author.id)

    if author_id in invites:

        await ctx.send(f"You already have an invite: {invites[author_id]['url']} with {invites[author_id]['uses']} uses.")
        return

    invite = await ctx.channel.create_invite(max_uses=0)
    invites[author_id] = {"url": invite.url, "uses": 0, "users": []}

    update_invites_file()
    await ctx.send(f"Here is your invite: {invite.url}")

    print("New Invite Created")

# Returns Your Existing Invite
@bot.command(description="Responds with your invite.")
async def myinvite(ctx):
    # Check if the command was written in a specific channel
    allowed_channel_id = leaderboard_channel
    if ctx.channel.id != allowed_channel_id:

        await ctx.send("This command is only allowed in a specific channel.")
        return

    author_id = str(ctx.author.id)
    
    if author_id in invites:

        await ctx.send(f"Your invite: {invites[author_id]['url']} has {invites[author_id]['uses']} uses.")

    else:
        await ctx.send("You don't have an invite.")

# Gets The Inviter Of A User If They Joined From A Bot Invite
@bot.command(description="Responds with the inviter of the mentioned user.")
async def inviter(ctx, member: discord.Member):
    # Check if the command was written in a specific channel
    allowed_channel_id = leaderboard_channel
   
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("This command is only allowed in a specific channel.")
        return

    author_id = None
    for invite_author_id, invite_data in invites.items():

        if member.id in invite_data["users"]:

            author_id = invite_author_id
            break

    if author_id is None:
        await ctx.send("Could not find the inviter.")

    else:
        inviter = ctx.guild.get_member(int(author_id))
        await ctx.send(f"{member.mention} was invited by {inviter.mention}")

# Add Invite Amount
@bot.command(description="Add an amount referred to the mentioned user.")
async def inviteadd(ctx, member: discord.Member, amount: int):

    # Check if the command was written in a specific channel
    allowed_channel_id = leaderboard_channel
    
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("This command is only allowed in a specific channel.")
        return

    if not ctx.author.guild_permissions.manage_guild:

        await ctx.send("You do not have permission to use this command.")
        return

    author_id = str(ctx.author.id)
    member_id = str(member.id)

    # Check if the inviter has an existing invite
    if author_id in invites:

        # Update the invite count for the inviter
        invites[author_id]["uses"] += amount
        invites[author_id]["users"].append(member.id)

        update_invites_file()
        # Notify about the invite

        await ctx.send(f"{amount} invites have been added to {ctx.author.mention}'s invite count.")

    else:
        await ctx.send("You don't have an invite. Create one using !createinvite first.")

# Check Invite Amount
@bot.command(description="Responds with the invite count of the mentioned user or the author if no user is specified.")
async def inviteamount(ctx, member: discord.Member = None):
    # Check if the command was written in a specific channel
    allowed_channel_id = leaderboard_channel
    
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("This command is only allowed in a specific channel.")
        return

    if member is None:
        member = ctx.author
    member_id = str(member.id)

    # Check if the member has an existing invite

    if member_id in invites:
        invite_count = invites[member_id]["uses"]
        await ctx.send(f"{member.mention} has referred a total of {invite_count} invites.")

    else:
        await ctx.send("This member does not have any invites.")

# Leaderboard
@bot.command(description="Displays the invite leaderboard for the server.")
async def leaderboard(ctx):
    # Check if the command was written in a specific channel
    allowed_channel_id = leaderboard_channel
    
    if ctx.channel.id != allowed_channel_id:

        await ctx.send("This command is only allowed in a specific channel.")
        return

    leaderboard_text = "invite Leaderboard:\n"

    # Sort invites by the number of uses in descending order
    sorted_invites = sorted(invites.items(), key=lambda x: x[1]['uses'], reverse=True)

    for idx, (author_id, invite_data) in enumerate(sorted_invites, start=1):
        member = ctx.guild.get_member(int(author_id))

        if member:
            invite_count = invite_data['uses']
            # Assign a medal emoji based on the position

            if idx == 1:
                medal = "🥇"
            elif idx == 2:
                medal = "🥈"
            elif idx == 3:
                medal = "🥉"                
            else:
                medal = ""

            # Define color based on the position (just an example, you can adjust as needed)
            color = f"{255 - min(idx * 10, 255):02X}FFFF"  
            leaderboard_text += f"{medal} {idx}. **{member.display_name}** ({member.mention}): {invite_count} invites\n"

    # Send the formatted leaderboard
    embed = discord.Embed(
        title="Congratss Guys !!!",
        description=leaderboard_text,
        color=discord.Color(int(color, 16)) if sorted_invites else discord.Color.default(),
    )
    await ctx.send(embed=embed)

# These are the commands availaible

#  `!createinvite` - This will create an invite and assign it to you
#  `!myinvite` - Responds with your invite
#  `!inviter <@User>` - This will allow you to see who invited a mentioned user
#  `!inviteadd <user> <amount> ` - Adds an amount of money to the mentioned user
#  `!inviteamount [user]` - Responds with how much someone has referred
#  `!leaderboard ` - Responds with how much someone has referred
