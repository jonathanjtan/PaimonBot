# paimon.py
import datetime
import discord
import json
import os
import pickle
import requests

from dotenv import load_dotenv
from owotext import OwO

from database import *

# Load secret from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

# flags and stuff
USERDATA_LOCATION = "users.pkl"
userdata = None
uwu_owo = False
owo_uwu = False

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

async def owo(message, *args):
    global owo_uwu
    owo_uwu = not owo_uwu
    if owo_uwu:
        await post(message, "going sicko mode")
    else:
        await post(message, "<:Sadge:766857757533536266>")

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
    await post(message, f"Your tracked characters are: {natural_format(characters)}.\n Your tracked weapons are: {natural_format(weapons)}")

async def resin(message, *args):
    if args:
        current_resin_string = args[0]
        try:
            print(current_resin_string)
            current_resin = int(current_resin_string)
            time_to_full = (160 - current_resin) * datetime.timedelta(minutes=8)
            time_full = datetime.datetime.now() + time_to_full
            pst = (time_full - datetime.timedelta(hours=8)).strftime("%H:%M")
            est = (time_full - datetime.timedelta(hours=5)).strftime("%H:%M")

            time_to_twenty = 20 - current_resin % 20
            next_twenty = current_resin + time_to_twenty
            time_twenty = datetime.datetime.now() + (datetime.timedelta(minutes=8) * time_to_twenty)
            pst_twenty = (time_twenty - datetime.timedelta(hours=8)).strftime("%H:%M")
            est_twenty = (time_twenty - datetime.timedelta(hours=5)).strftime("%H:%M")

            time_to_fourty = time_to_twenty + 20
            next_fourty = next_twenty + 20
            time_fourty = time_twenty + (datetime.timedelta(minutes=8) * 20)
            pst_fourty = (time_fourty - datetime.timedelta(hours=8)).strftime("%H:%M")
            est_fourty = (time_fourty - datetime.timedelta(hours=5)).strftime("%H:%M")

            if current_resin > 160 or current_resin < 0:
                await post(message, f"That's not possible bruh")
            elif current_resin >= 140:
                await post(message, f"Your resin will be full at around {pst} PST / {est} EST")
            elif current_resin >= 120:
                await post(message, f"Your resin will be full at around {pst} PST / {est} EST\nYou'll have {next_twenty} resin in roughly {time_to_twenty * 8} minutes around {pst_twenty} PST / {est_twenty} EST")
            elif current_resin >= 0:
                await post(message, f"""Your resin will be full at roughly {pst} PST / {est} EST\nYou'll have {next_twenty} resin in roughly {time_to_twenty * 8} minutes around {pst_twenty} PST / {est_twenty} EST\nYou'll have {next_fourty} resin in roughly {time_to_fourty * 8} minutes around {pst_fourty} PST / {est_fourty} EST""")


        except:
            await post(message, f"Provide your current amount of resin as an integer!") 

    else:
        await post(message, f"Provide your current amount of resin!")

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
    farmable_mats = natural_format(list(characters_level[character]))
    element_mats = natural_format(list(element_materials[element]))
    talent_mats = natural_format(list(characters_talent[character]))
    character = character.capitalize()
    text = (
        f"{character} uses {element_mats} boss drops to level up. \n"
        f"They also use {farmable_mats} farmables to level up. \n"
        f"Their talents use {talent_mats} to level up. \n"
    )
    await post(message, text)

'''
small use warframe section
input should be like: !relic lith foo1 bar2 baz3
for each relic, query warframe.market for items last three plat prices
then output sorted by plat value
https://warframe.market/api_docs
https://github.com/TitaniaProject/warframe-relic-data/blob/master/data/Relics.json
'''
async def relic(message, *args):
    endpoint = "https://api.warframe.market/v1"
    strips = ['neuroptics', 'systems', 'chassis']

    if args:
        if len(args) < 3 or len(args) % 2 == 0:
            await post(message, f"Expected format: `n <era> <type> <era> <type>...`, e.g. `=relic 3 lith a1`")
        else:
            reward_pool = {} # map from rewards to plat values

            # tokenize into groupings
            relic_groups = []
            for i in range(1, len(args), 2):
                relic_groups.append((args[i], args[i + 1]))

            # populate item pool with all possible rewards
            for relic_name, relic_type in relic_groups:
                print(f"Processing {relic_name} {relic_type}")

                # hit the local JSON relic mappings
                lookup_string = f"{relic_name.lower().capitalize()} {relic_type.capitalize()}"
                if lookup_string not in relics:
                    continue
                else:
                    for reward in relics[lookup_string]['rewards']:
                        reward_name = reward['item'].lower().replace(' ', '_')
                        if any(x in reward_name for x in strips):
                            reward_name = reward_name.replace('_blueprint', '')
                        if reward_name not in reward_pool:
                            reward_pool[reward_name] = []

            # remove forma, can't trade it
            if 'forma_blueprint' in reward_pool:
                del reward_pool['forma_blueprint']

            # hit warframe market for each item in the pool
            for reward in reward_pool.keys():
                r = requests.get(f"https://api.warframe.market/v1/items/{reward}/orders").json()

                # filter by online/ingame
                curr_orders = []
                if 'payload' in r and 'orders' in r['payload']:
                    for order in r['payload']['orders']:
                        status = order['user']['status']
                        if order['order_type'] == 'sell' and status == 'ingame' or status == 'online':
                            curr_orders.append(order['platinum'])
                else:
                    continue

                # grab cheapest n orders
                reward_pool[reward] = sorted(curr_orders)[:min(int(args[0]), len(curr_orders))]
           
            print(f"Processed reward pool: {reward_pool}")
            
            output = [f'Stack ranked cheapest {args[0]} sell orders from requested relic(s)']
            output.append('```')
            for reward in sorted(reward_pool.keys(), key=lambda x: sum(reward_pool[x])/len(reward_pool[x]), reverse=True):
                output.append(f"{reward}: {reward_pool[reward]}, avg = {sum(reward_pool[reward])/len(reward_pool[reward]):.2f}")
            output.append('```')

            await post(message, '\n'.join(output))

            # TODO: refactor so it doesn't look like shit
            # calculate expected plat value from a relic (intact and radiant)
            # intact: (.2533... * 3) + (.11 * 2) + (.02)
            # radiant: (.1667... * 3) + (.2 * 2) + (.1)

            relic_output = []
            for relic_name, relic_type in relic_groups:
                print(f"Processing {relic_name} {relic_type}")


                intact_ev, radiant_ev = 0, 0
                # hit the local JSON relic mappings
                lookup_string = f"{relic_name.lower().capitalize()} {relic_type.capitalize()}"
                if lookup_string not in relics:
                    continue
                else:
                    for reward in relics[lookup_string]['rewards']:
                        reward_name = reward['item'].lower().replace(' ', '_')
                        if any(x in reward_name for x in strips):
                            reward_name = reward_name.replace('_blueprint', '')
                        if reward_name == "forma_blueprint":
                            continue
                        curr_avg = sum(reward_pool[reward_name]) / len(reward_pool[reward_name])
                        if reward['chance'] == .02: # rare
                            intact_ev += .02 * curr_avg
                            radiant_ev += .1 * curr_avg
                        elif reward['chance'] == .11: # uncommon 
                            intact_ev += .11 * curr_avg
                            radiant_ev += .2 * curr_avg
                        elif reward['chance'] == .25: # common
                            intact_ev += .2533 * curr_avg
                            radiant_ev += .1667 * curr_avg

                relic_output.append(f"{relic_name} {relic_type}: Intact Plat EV ({intact_ev:.2f}), Radiant Plat EV ({radiant_ev:.2f}) ")
            await post(message, '\n'.join(relic_output))
                        
    else:
        await post(message, f"Expected format: `lith a1 lith b2...`")

# just so you're not writing awaits everywhere
async def post(message, text):
    if owo_uwu:
        uwu = OwO()
        await message.channel.send(uwu.whatsthis(text))
    elif uwu_owo:
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
        print(f"saving: {userdata}\n")
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
    "owo" : owo,
    "uwu" : uwu,
    "register" : register,
    "relic" : relic,
    "remove" : remove,
    "resin" : resin,
    "test" : test,
    "today" : today,
    "tomorrow" : tomorrow
}

# load warframe relics
relics = {}
with open('relics.json') as json_file:
    data = json.load(json_file)
 
    for entry in data:
        relics[entry['name']] = entry

# populate "userdata", indexed on author id
if os.path.exists(USERDATA_LOCATION):
    userdata = load()
    print(f"Loading registered data... \n {userdata} \n")
else:
    userdata = dict()
    save()

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()
