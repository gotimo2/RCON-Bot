
#imports
import os
import discord
import dotenv
from valve import rcon, source
import valve
import asyncio
from dotenv import load_dotenv

#definitions
load_dotenv() #load .env
TOKEN = os.getenv("TOKEN") #get token from .env and define it
client = discord.Client()


#global variables, because they're annoying to implement otherwise
global rconChannel


def connectServer():
    #get rcon info from .env
    rconAdress = (os.getenv("RCONADRESS"), int(os.getenv("RCONPORT"))) #why is this a tuple with port and adress, instead of RCON having another argument? I DON'T KNOW, IT DOESN'T MAKE ANY SENSE!
    rconPassword = os.getenv("RCONPASSWORD")
    global rc
    try: #remove existing connection
        del(rc)
    except:
        pass
    rc = rcon.RCON(rconAdress, rconPassword) #make new one
    rc.connect() #connect to it
    rc.authenticate() #authenticate with it
    rc.execute("echo bot online").body.decode('utf-8', 'ignore') #print "bot online" in the console of the server
    

@client.event
async def on_ready(): #when the bot connects
    rconChannelId = os.getenv("RCONCHANNELID") #get the rcon channel id
    print(f'{client.user} has connected to Discord!') #print that the bot's connected
    global rconChannel
    rconChannel = client.get_channel(int(rconChannelId)) #get the rcon channel by id
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="A source server"))




@client.event
async def on_message(message):
    global rconChannel
    global rc
    if message.author == client.user: #we don't want the bot to send commands to itself /shrug
        return
    if message.content == 'hello bot': #ping-like command
        response = f'hello human {message.author}'
        print(f'sent {response}')
        await message.channel.send(response)
    if message.channel == rconChannel:
        command = message.content
        if command == "!connect" or command == "!c": #reconnect command
            await message.channel.send("attempting to connect to the server")
            try:
                connectServer()
            except:
                await message.channel.send("error connecting to the server")
            #if no bug arises, the bot connected
            await message.channel.send("connected to the server")
            #execute status on connect
            await message.channel.send(rc.execute("status").body.decode('utf-8', 'ignore'))
            #if no command is done, just execute any message in the rcon channel
        else:
            try:
                print(f"{message.author}:{message.content}")
                message.channel.send(rc.execute(message.content).body.decode('utf-8', 'ignore'))
            except:
                print("bot disconnected, reconnecting...")
                connectServer()
                message.channel.send(rc.execute(message.content).body.decode('utf-8', 'ignore'))


    

connectServer()

client.run(TOKEN)