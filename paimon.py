# paimon.py
import os

import database
import discord
from dotenv import load_dotenv

# Load secret from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
 
client = discord.Client()

# Load userdata {message.author:[characters], [weapons]}

# Load "database"
'''
we can ignore common ascension materials because they're world drops
characters: level ascension materials
characters: talent ascension materials
weapons: weapon ascension materials
talent ascension materials: (day, location)
weapon ascension materials: (day, location)
'''

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to Discord!')
    print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    # prevent recursion
    if message.author == client.user:
        return

    

client.run(TOKEN)
