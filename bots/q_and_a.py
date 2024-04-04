import discord

client = discord.Client(intents=discord.Intents.all())

# Define common keywords and their corresponding responses
common_keywords = {
    "rules": "Here are the rules of the game: [Link to Rules]",
    "gameplay": "Gameplay tips: [Link to Gameplay Guide]",
    "cheats": "We do not support cheats in this forum.",
    "help" : "Here is the link to [Link  to Help]"
}
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the message contains any common keywords
    for keyword, response in common_keywords.items():
        if keyword in message.content.lower():
            # Respond with the predefined answer and mention the user who asked the question
            reply = f'{message.author.mention}, {response}'
            await message.channel.send(reply)
