# PaimonBot
Genshin Impact resource tracking bot.

create an .env file and populate with DISCORD_TOKEN and DISCORD_SERVER

e.g.
```
DISCORD_TOKEN=$SERVER_TOKEN
DISCORD_SERVER=$SERVER_NAME
```

Might be broken soon, with the halting of development on `discord.py`: read more [here](https://www.reddit.com/r/programming/comments/pd092x/discordpy_development_ceased/).

Feel free to delete `users.pkl`, I was just keeping it around for personal backup.

Also, would be nice to migrate the database from the JSON mess to scrape [honey impact](https://genshin.honeyhunterworld.com/) for all the needed data. When this bot was created, there was no good authoritive source for Genshin info anywhere
