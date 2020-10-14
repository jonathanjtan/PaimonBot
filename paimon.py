# paimon.py
import os

from database import *
import datetime
import discord
from dotenv import load_dotenv
import pickle

# Load secret from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
USERDATA_LOCATION = "users.pkl"
userdata = None

client = discord.Client()

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

    content = message.content
    if content.startswith("="):
        tokens = content[1:].split()
        if not tokens or tokens[0] not in valid_commands:
            await message.channel.send(f"That's not a valid command, {message.author}!")
        else:
            if len(tokens) == 1:
                await valid_commands[tokens[0]](message)
            else:
                await valid_commands[tokens[0]](message, *tokens[1:])

async def help(message, *args):
    await message.channel.send(f"valid commands are: {', '.join(valid_commands.keys())}")

async def test(message, *args):
    await message.channel.send("Test post please ignore")

async def register(message, *args):
    username = str(message.author)
    if username not in userdata:
        userdata[username] = set()
        save()
        await message.channel.send(f"{username}, you have been registered to the database!")
    else:
        await message.channel.send(f"{username}, you have already been registered to the database!")

async def add(message, *args):
    username = str(message.author)
    added = []
    if args:
        for arg in args:
            arg = str.lower(arg)
            if arg not in characters_element and arg not in weapons_materials:
                await message.channel.send(f"{arg.capitalize()} is neither a character nor weapon in Genshin Impact, please try again!")
            else:
                if arg not in userdata[username]:
                    userdata[username].add(arg)
                    added.append(arg.capitalize())
                else:
                    await message.channel.send(f"You've already added {arg.capitalize()} to your list of characters and weapons!")
        if added:
            save()
            await message.channel.send(f"You've added {natural_format(added)} to your list of characters and weapons!")
    else:
        await message.channel.send(f"Please provide space delimited arguments!")

async def remove(message, *args):
    username = str(message.author)
    removed = []
    if args:
        for arg in args:
            arg = str.lower(arg)
            if arg not in characters_element and arg not in weapons_materials:
                await post(message, f"{arg.capitalize()} is neither a character nor weapon in Genshin Impact, please try again!")
            else:
                if arg in userdata[username]:
                    userdata[username].remove(arg)
                    removed.append(arg.capitalize())
                else:
                    await post(message, f"You don't have {arg.capitalize()} on your list of characters and weapons!")
        if removed:
            save()
            await post(message, f"You've removed {natural_format(removed)} from your list of characters and weapons!")
    else:
        await post(message, f"Please provide space delimited arguments!")

# TODO: Split into books/weapon materials
async def today(message, *args):
    now = datetime.datetime.now()
    day_name = now.strftime("%A")
    username = str(message.author)
    possibilities = []
    for character in userdata[username]:
        talent = list(characters_talent[character].intersection(books))[0]
        if day_name in materials[talent][0]:
            possibilities.append(f"{talent.capitalize()} books for {character.capitalize()} at {materials[talent][1]}")
    if possibilities:
        text = "\n".join(possibilities)
        await post(message, f"Today, you can run:\n```{text}```")
    else:
        await post(message, f"Unfortunately, there are no books you can run today!")

async def lookup(message, *args):
    if args:
        for arg in args:
    else:
        await post(message, "You need to enter in space delimited arguments of materials to look up.")

# just so you're not writing awaits everywhere
async def post(message, text):
    await message.channel.send(text)

def natural_format(words):
    words = [w.capitalize() for w in words]
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return " and ".join(words)
    else:
        return ", ".join(words[:len(words) - 1]) + ", and " + words[len(words) - 1]

def save():
    with open(USERDATA_LOCATION, 'wb') as f:
        print(f"saving: {userdata}")
        pickle.dump(userdata, f, pickle.HIGHEST_PROTOCOL)

def load():
    with open(USERDATA_LOCATION, 'rb') as f:
        return pickle.load(f)

# get command list ready
valid_commands = {
    "add" : add,
    "help" : help,
    "register" : register,
    "remove" : remove,
    "test" : test,
    "today" : today
}

# populate "userdata", indexed on author id
if os.path.exists(USERDATA_LOCATION):
    userdata = load()
    print(f"loading: {userdata}")
else:
    userdata = dict()
    save()

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()