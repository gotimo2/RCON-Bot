import os
import discord
import dotenv
from valve import rcon
import asyncio
#dotenv stuff
from dotenv import load_dotenv #import loading .env function
load_dotenv() #load .env
TOKEN = os.getenv("TOKEN") #get token from .env and define it

client = discord.Client()

global rconChannel

@client.event
async def on_ready():
    rconChannelId = os.getenv("RCONCHANNELID")
    print(f'{client.user} has connected to Discord!')
    global rconChannel
    rconChannel = client.get_channel(int(rconChannelId))
    #get rcon info from .env
    rconAdress = (os.getenv("RCONADRESS"), int(os.getenv("RCONPORT")))
    rconPassword = os.getenv("RCONPASSWORD")
    global rc
    rc = rcon.RCON(rconAdress, rconPassword)
    rc.connect()
    rc.authenticate()
    rc.execute("echo bot online").body.decode('utf-8', 'ignore')


@client.event
async def on_message(message):
    global rconChannel
    global rc
    if message.author == client.user: #we don't want the bot to send commands to itself /shrug
        return
    if message.content == 'hello bot':
        response = f'hello human {message.author}'
        print(f'sent {response}')
        await message.channel.send(response)
        if message.channel == rconChannel:
                rc.connect()
                rc.authenticate()
                rc.execute("echo bot online").body.decode('utf-8', 'ignore')
    if message.channel == rconChannel:
        await message.channel.send(rc.execute(message.content).body.decode('utf-8', 'ignore'))
    



client.run(TOKEN)