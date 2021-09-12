import discord
import random
import RollMode as RM
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

client = discord.Client()
global playerModes
global default #default gamemode
playerModes = {}
dicOfModes = {}


#Bot Permissions number is 2048
#https://discord.com/api/oauth2/authorize?client_id=843156754921160724&permissions=2048&scope=bot

#Change which of these is commented out to change the default
DEFAULT_MODE = "dnd"
#default = RM.dndMode.setMode()

dicOfModes.update({"dnd" : RM.dndMode.setMode()})
#default = RM.ShadowrunMode.setMode()
dicOfModes.update({"shadowrun" : RM.ShadowrunMode.setMode()})
#default = RM.MotwMode.setMode()
dicOfModes.update({"motw" : RM.MotwMode.setMode()})
#default = RM.FateMode.setMode()
dicOfModes.update({"fate" : RM.FateMode.setMode()})
#default = RM.MnMMode.setMode()
dicOfModes.update({"mnm" : RM.MnMMode.setMode()})
default = dicOfModes[DEFAULT_MODE]


'''Prints all avalible game systems'''
def getModes():
    return "Here are the avalible modes: " + str(dicOfModes.keys())

    



'''Sets the dice roller to the game system provided in the message'''

def setMode(message):
    #Remove !mode
    msg = message.content.replace("!mode ", "")
    return dicOfModes.get(msg, default)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    

@client.event
async def on_message(message : discord.Message):
    global playerModes
    if message.author == client.user:
        return
    if not(message.author.id in playerModes):
        playerModes.update({message.author.id : default})
        print("New user added")
        print(playerModes, '\n')
    if message.content.startswith("!modes"): #TODO add this to help text
        await message.channel.send(getModes())
    elif message.content.startswith('!roll'):
        await message.channel.send(playerModes[message.author.id].roll(message))
        
    elif message.content.startswith("!mode"):
        playerModes.update({message.author.id : setMode(message)})
        print(playerModes, '\n')
        await message.channel.send(message.author.display_name + "'s mode has been set to " + playerModes.get(message.author.id).toString())
    elif message.content.startswith("!current"):
        await message.channel.send(playerModes.get(message.author.id).toString())

    #print("sucsess")









client.run(config["BOT"]["RollBot"])
