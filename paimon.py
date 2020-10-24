# paimon.py
import datetime
import os
import pickle

import discord
from dotenv import load_dotenv

from database import *

# Load secret from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
USERDATA_LOCATION = "users.pkl"
userdata = None
uwu_owo = False

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
            await post(message, f"That's not a valid command, {message.author}!")
        else:
            if len(tokens) == 1:
                await valid_commands[tokens[0]](message)
            else:
                if tokens[0] == "add" or tokens[0] == "remove": # switch to comma delmited arguments after initial token
                    comma_tokens = " ".join(tokens[1:]).split(",")
                    await valid_commands[tokens[0]](message, *comma_tokens)
                else:
                    await valid_commands[tokens[0]](message, *tokens[1:])

async def help(message, *args):
    await post(message, f"valid commands: {', '.join(valid_commands.keys())}")

async def test(message, *args):
    await post(message, "Test post please ignore")

async def uwu(message, *args):
    global uwu_owo
    uwu_owo = not uwu_owo
    await post(message, "o")

async def register(message, *args):
    username = str(message.author)
    if username not in userdata:
        userdata[username] = set()
        save()
        await post(message, f"{username}, you have been registered to the database!")
    else:
        await post(message, f"{username}, you have already been registered to the database!")

async def add(message, *args):
    username = str(message.author)
    added = []
    if args:
        for arg in args:
            arg = str.lower(arg).strip()
            if arg not in characters_element and arg not in weapons_materials:
                await post(message, f"{arg.capitalize()} is neither a character nor weapon in Genshin Impact, please try again!")
            else:
                if arg not in userdata[username]:
                    userdata[username].add(arg)
                    added.append(arg.capitalize())
                else:
                    await post(message, f"You've already added {natural_format([arg])} to your list of characters and weapons!")
        if added:
            save()
            await post(message, f"You've added {natural_format(added)} to your list of characters and weapons!")
    else:
        await post(message, f"Please provide comma delimited arguments! Leave out punctuation from weapons.")

async def remove(message, *args):
    username = str(message.author)
    removed = []
    if args:
        for arg in args:
            arg = str.lower(arg).strip()
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
        await post(message, f"Please provide comma delimited arguments! Leave out punctuation from weapons.")

async def today(message, *args):
    print(datetime.datetime.now())
    now = datetime.datetime.now() - datetime.timedelta(hours=9)
    day_name = now.strftime("%A")
    await day(message, day_name)

async def tomorrow(message, *args):
    now = datetime.datetime.now() + datetime.timedelta(days=1) - datetime.timedelta(hours=9)
    day_name = now.strftime("%A")
    await day(message, day_name)

async def day(message, *args):
    if args:
        valid = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = str.lower(args[0]).capitalize()
        print(day_name)
        if day_name in valid:
            username = str(message.author)
            possibilities = possibilities_format(userdata[username], day_name)
            if possibilities:
                text = "\n".join(possibilities)
                await post(message, f"On {day_name}, you can run:\n```{text}```")
            else:
                await post(message, f"Unfortunately, there's nothing you can run!")
        else:
            await post(message, f"{day_name} is not a valid day name! Try a weekday or weekend.")
    else:
        await post(message, f"No valid day was provided to this command.")

async def box(message, *args):
    units = userdata[str(message.author)]
    characters = [c for c in units if c in characters_element]
    weapons = [w for w in units if w in weapons_materials]
    await post(message, f"Your tracked characters are: {natural_format(characters)}. Your tracked weapons are: {natural_format(weapons)}")

# TODO: impl
async def lookup(message, *args):
    if args:
        item = str.lower(args[0])
        if item in characters_level:
            await character_lookup(message, item)
    else:
        await post(message, "You need to enter in one item to look up.")

async def character_lookup(message, character):
    element = characters_element[character]
    farmable_mats = natural_format(list(characters_level_farmable[character]))
    element_mats = natural_format(list(element_materials[element]))
    talent_mats = natural_format(list(characters_talent[character]))
    character = character.capitalize()
    text = (
        f"{character} uses {element_mats} boss drops to level up. \n"
        f"They also use {farmable_mats} farmables to level up. \n"
        f"Their talents use {talent_mats} to level up. \n"
    )
    await post(message, text)

# just so you're not writing awaits everywhere
async def post(message, text):
    if uwu_owo:
        await message.channel.send(text.replace("u", "uwu").replace("o", "owo"))
    else:
        await message.channel.send(text)

def natural_format(words):
    formatted = []
    for w in words:
        string = " ".join([x.capitalize() for x in w.split(" ")])
        formatted.append(string)
    words = formatted
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return " and ".join(words)
    else:
        return ", ".join(words[:len(words) - 1]) + ", and " + words[len(words) - 1]

def possibilities_format(units, day_name):
    possible = {}
    for unit in units:
        if unit in characters_element: # tracking a character
            material = list(characters_talent[unit].intersection(books))[0]
        elif unit in weapons_materials: # tracking a weapon
            material = list(weapons_materials[unit].intersection(weapon_ascension))[0]
        else:
            continue

        if day_name in materials[material][0]:
            location = materials[material][1]
            if material not in possible:
                possible[material] = ["location", []]
                possible[material][0] = location
            possible[material][1].append(unit)
    
    possibilities = []
    for material, v in possible.items():
        location, units = v
        possibilities.append(f"{material.capitalize()} mats for {natural_format(units)} at {location}")
    
    return possibilities

def migrate():
    for user, units in userdata.items():
        if "prototype animus" in units:
            units.remove("prototype animus")
            units.add("prototype aminus")
    save()

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
    "box" : box,
    "day" : day,
    "help" : help,
    "lookup" : lookup,
    "uwu" : uwu,
    "register" : register,
    "remove" : remove,
    "test" : test,
    "today" : today,
    "tomorrow" : tomorrow
}

# populate "userdata", indexed on author id
if os.path.exists(USERDATA_LOCATION):
    userdata = load()
    print(f"loading: {userdata}")
    migrate()

else:
    userdata = dict()
    save()

def main():
    print(uwu_owo)
    client.run(TOKEN)

if __name__ == "__main__":
    main()
