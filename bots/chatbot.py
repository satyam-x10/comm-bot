# chatbot.py
import discord
import os
import openai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# chatbot.py

import requests

def send_message_to_api(message):
    api_url = "https://chatgpt-api.shn.hk/v1/"

    payload = {
        "message": message,
    }

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        response_message = data.get("message", "No response message received.")
        return response_message
    else:
        return f"Error: {response.status_code} - {response.text}"

@bot.event
async def on_ready():
    print("Bot is connected and ready!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("bacpac"):
        result = await run_completion(message.content[1:])
        await message.channel.send(result)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)