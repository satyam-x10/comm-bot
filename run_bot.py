# run_bot.py
import asyncio
import os
from dotenv import load_dotenv

# from bots.chatbot import bot as chatbot_client
from bots.q_and_a import client as q_and_a_client
from bots.inviteManager import bot as invite_manager_bot
from bots.poll import bot as poll_bot
from bots.voiceChannel import bot as voiceChannel_bot
from bots.spammers import bot as spammers_bot

# Load environment variables from a .env file
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    # TOKEN = os.environ[Discord_TOKEN]

    # Create and run separate event loops for each bot
    loop = asyncio.get_event_loop()
    # loop.create_task(chatbot_client.start(TOKEN))  # Run the chatbot
  
    loop.create_task(q_and_a_client.start(TOKEN))  # Run the Q&A bot
    loop.create_task(invite_manager_bot.start(TOKEN))  # Run the invite manager bot
    loop.create_task(poll_bot.start(TOKEN))  # Run the poll bot
    loop.create_task(voiceChannel_bot.start(TOKEN))  # Run the voiceChannel bot
    loop.create_task(spammers_bot.start(TOKEN))  # Run the spammers bot
    

    loop.run_forever()
 