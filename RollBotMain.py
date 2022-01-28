import discord
import RollMode as RM
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

client = discord.Client()
global playerModes
global default #default gamemode
playerModes = {}
dicOfModes = {}
ADMIN_ID = int(config["ADMIN"]["adminID"])

#Bot Permissions number is 2048
#https://discord.com/api/oauth2/authorize?client_id=843156754921160724&permissions=2048&scope=bot

#Change which of these is commented out to change the default
DEFAULT_MODE = "fev"

#Put all modes to be made available here.
dicOfModes.update({"dnd" : RM.dndMode.setMode()})
dicOfModes.update({"shadowrun" : RM.ShadowrunMode.setMode()})
dicOfModes.update({"motw" : RM.MotwMode.setMode()})
dicOfModes.update({"fate" : RM.FateMode.setMode()})
dicOfModes.update({"mnm" : RM.MnMMode.setMode()})
dicOfModes.update({"cofd" : RM.CofdMode.setMode()})
dicOfModes.update({"sbk" : RM.SpellboundKingdomsMode.setMode()})
dicOfModes.update({"fev" : RM.FEVMode})
default = dicOfModes[DEFAULT_MODE]



def getModes():
    '''Prints all avalible game systems'''
    return "Here are the avalible modes: " + str(dicOfModes.keys())

    
def setMode(message):
    '''Sets the dice roller to the game system provided in the message'''
    #Remove !mode
    msg = message.content.replace("!mode ", "")
    return dicOfModes.get(msg, default)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    

@client.event
async def on_message(message : discord.Message):
    """
    Parses a message submitted by a user
    If a user does not have an assosiated gamemode, it is set to DEFAULT_MODE.
    If the message starts with !modes, a message is sent that sends all available modes.
    If a message starts with !roll, it parses the rest of the message as described in the users Mode
    If a message starts with !mode, the senders mode is set to the mode associated with the end of the string. If the message sent is not a valid key, the mode is set to the default mode insted.
    If a message starts with !current, it sends a message displaying the users current mode.
    If a message starts with !default, setDefault is called.
    """
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
    elif(message.content.startswith("!default")):
        await setDefault(message)
        #await message.channel.send("Default changed")
    #print("sucsess")

async def setDefault(message : discord.Message):
    '''Changes the default gamemode to the game listed in message.'''
    global default
    if(message.author.id == ADMIN_ID):
        msg = message.content.replace("!default", "").strip()
        print(msg)
        if msg in dicOfModes:
            default = dicOfModes[msg]
            await message.channel.send("Default set to " + msg)
        else:
            await message.channel.send("mode not found")
    else:
            print("Invaled default change. The the culprit is:", message.author)
            await message.channel.send("***DEFAULT CAN ONLY BE CHANGED BY BOT OWNER***")
        







client.run(config["BOT"]["RollBot"])
