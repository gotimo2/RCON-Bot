# RCON-Bot

Do you host a source-based game server? 

is having to open an entire SSH session just too much effort for you?

## Try RCON-Bot!

this bot will allow you to input details for a source server, and details for a channel in discord, which will allow you to control your server from that discord channel!
simply input details of a discord text channel that the bot has access to and details of a source server in .env, start the bot with python3 bot.py and pray to god the bot works!

it is known that the bot's connection to a server will break on a map change. since i'm too lazy to implement an actual solution to this issue, saying "!connect" in the rcon channel should restart the connection to the server.
