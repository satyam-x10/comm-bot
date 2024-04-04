# DiscordBot
Scripts to create a discord bot application

## This is totally a voluntary project and no one is forced to work on it. In case you find the project interesting and want to contribute, message me (ARVY).
I am working on a new discord server that will be public and will be used to create our first network of community. For the server, I am programming a custom discord bot that will automate a lot of things on the server and also guide new users through the server.

## Example features
Some example features include: create embed message to introduce team members (founders+interns), act as a chatbot and help new users guide through the server and answer their questions, automatically answer repetitive questions in the forum and q&a channels.

## These are the files:
embed_message.py --> Creates embed messages to introduce team members. I still need to find a way to make the embed widths equal for all team members.

q_and_a.py --> If there is a common keyword, the bot automatically replies with a response.

chatbot.py --> still working on it but trying to do a POST request to the website: api_url = "https://chatgpt-api.shn.hk/v1/" to get response from Free Chat GPT. If it works, then we can think of getting our own OPENAI API.

inviteManager.py --> keep track of invites of the users and a leaderboard based on quantity of joinees on referrals .

poll.py --> Create a poll in Poll channel

Spammers.py --> Warns user if they exceed hourly message limit , Bans them if they keep spammimg

voiceChannel.py -> Create a temporary voice channel in the server

Welcome.py --> sends a personal dm to a user after they join the server

Please update this on every new push.