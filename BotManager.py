import discord
from Functions.One import start1v1, end1v1
from Functions.Two import start2v2, end2v2
from Functions.Four import start4v4, end4v4
from discord.ext import commands
from Functions.Register import register as Register

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

APIKEY = 'a2f9308c-bf8e-4ecf-862c-544085f97e05'

with open('token.txt','r') as f: 
  TOKEN = f.read()
    
with open('GameCount.txt','r') as f:
  games = int(f.read())

myDict = {}
teamsPool = ['Aquarium','Eastwood','Invasion','Lectus','SwashBuckle','Archway','Boletum','Chained']

@client.event
async def on_ready():
  global games_stuff;
  games_stuff = client.get_channel(906351006214930472)
  print('We have logged in as {0.user}'.format(client))

async def startGame(gamemode,playerlst):
  if gamemode == '1v1':
    return await start1v1(playerlst)

  elif gamemode == '2v2': #2v2 start
    return await start2v2(playerlst);
    
  elif gamemode == '4v4':
    return await start4v4(playerlst);

@client.command()
async def force_end(message):
  print(message.channel.category.name)

  if message.channel.category.name == "GAMES":

    staff_team_role = client.get_role(921290756059197460); """Staff team role."""
    if not staff_team_role in message.author.roles:
      await message.channel.send(embed = discord.Embed(title = "You aren't staff!", description = "This command is only meant for staff members."))

    if myDict.get(message.channel.name[9::]):
      returnedDict = myDict.pop(message.channel.name[9::]);

@client.event
async def on_message(message):

  """Checking if message sent by bot."""
  if message.author == client.user: 
    return;

    """Registering"""
  elif message.content.startswith('!register ') and message.channel == client.get_channel(916934075741274162):
    await Register(message)

    """Ending Games"""

  elif message.content == '!end' and int(message.channel.category_id) == 907638053982597162:
    gid = message.channel.name[9::]  #g - game, gid = game id
    gamemode = message.channel.name[:3:]

    """Ending 1v1's"""
    if gamemode == '1v1':
      await end1v1(message.channel, myDict.pop(str(gid)))

      """Ending 2v2's"""
    elif gamemode == '2v2':
      await end2v2(message, myDict.pop(str(gid)))

    elif gamemode == '4v4':
      await end4v4(message, myDict.pop(str(gid)))

  elif message.channel == client.get_channel(906351006214930472): #games-stuff (you can't post normal text anymore)
    try: 
      message.content[0]; await message.delete()
      try: await message.author.send(embed=discord.Embed(title=f'Mate.',description=f'You can only post images on #games-stuff idiot...'))
      except: pass
    except: pass

"""Game Starter"""

@client.event
async def on_voice_state_update(data,before,after):
  global games;

  try:

    """1v1's"""
    if int(after.channel.category_id) == 902217443970285600:

      if len(after.channel.members) == 2:
        if lst := await startGame('1v1', after.channel.members):
          myDict[str(games)] = lst

    elif int(after.channel.category_id) == 902217465432526862:

      """2v2's"""
      if len(after.channel.members) == 4:
        games += 1

        with open('Games.txt','w') as f:
           f.write(str(games))

        if lst := await startGame('2v2',after.channel.members):
          myDict[str(games)] = lst;

    elif int(after.channel.category_id) == 902217485779083326:

      if after.channel.members == 8:
        with open('Games.txt','w') as f: f.write(str(games := games + 1))
        lst = await startGame('4v4', after.channel.members)
        myDict[str(games)]
        print(myDict[str(games)])

  except AttributeError: 
    """A person has left a certain voice channel. (Nothing to do!)"""
    pass

client.run(TOKEN)