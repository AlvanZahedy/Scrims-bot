import discord, random, time

client = discord.Client()

with open("token.txt") as token:
  TOKEN = token.read()

teamsPool = ['Aquarium','Eastwood','Invasion','Lectus','SwashBuckle','Archway','Boletum','Chained']

async def start4v4(playerlst):

  """4v4 Starting Initialization"""

  await client.login(TOKEN);
  transcripts = client.get_channel(902587505319247944)
  gamesCategory = client.get_channel(907638053982597162)
  guild = client.get_guild(901527310107279370)
  normRole = guild.get_role(902221222350311434)
  waitingRoom = client.get_channel(909083599318425660)

  with open('GameCount.txt','r') as f: 
    games = int(f.read())

  role = await guild.create_role(name=f'game-{games}')
  channel = await guild.create_text_channel(f'2v2-game-{games}', category=gamesCategory)

  """Channel Permissions Being Set."""

  await channel.set_permissions(role, read_messages = True, read_message_history = True, send_messages = True)
  await channel.set_permissions(normRole, read_messages = False, read_message_history = False, send_messages = False)
  await channel.set_permissions(guild.get_role(901694174192087081), read_messages = True, read_message_history = True, send_messages = True)
  await channel.set_permissions(guild.get_role(901694160443166812), read_messages = True, read_message_history = True, send_messages = True)
  await channel.set_permissions(guild.get_role(909084700688134166), read_messages = True, read_message_history = True, send_messages = True)
  await channel.set_permissions(guild.get_role(901705859447529512), read_messages = True, read_message_history = True, send_messages = True)

  playerlist = []
  for player in playerlst:
    await player.add_roles(role)
    playerlist.append(player.mention)

  random.shuffle(playerlist)
  captains = [playerlist[0], playerlist[1]]
  team1, team2 = [captains[0]], [captains[1]]
  vc1 = await guild.create_voice_channel(name=f'Team-1(2v2)-{games}',category=gamesCategory)
  vc1.user_limit = 4
  await vc1.set_permissions(role, view_channel=True,connect=True,speak=True,)
  await vc1.set_permissions(normRole, view_channel=False,connect=False,speak=False)
  await vc1.set_permissions(role, view_channel = True,connect = True,speak = True)
  await vc1.set_permissions(normRole, view_channel=False,connect=False,speak=False)
  await vc1.set_permissions(guild.get_role(901694174192087081), view_channel = True,connect = True,speak = True)
  await vc1.set_permissions(guild.get_role(901694160443166812), view_channel = True,connect = True,speak = True)
  await vc1.set_permissions(guild.get_role(909084700688134166), view_channel = True,connect = True,speak = True)
  await vc1.set_permissions(guild.get_role(901705859447529512), view_channel = True,connect = True,speak = True)

  for i in playerlst:
    await i.move_to(vc1)

  playerlist.remove(captains[0])
  playerlist.remove(captains[1])

  await channel.send(f'{role.mention}!')
  await channel.send(embed=discord.Embed(title = 'The two chosen captains are: ',description = f'**1.** {captains[0]}\n**2.** {captains[1]}\n**In order to pick, do !pick (player). Ex: "!pick {playerlist[0]}"' ,colour = discord.Colour.blue()))
  
  await channel.send(embed=discord.Embed(title = f"Remaining players:",description = f'The remaining players you can choose from are:\n'))

  def check(m):
    if int(m.channel.category_id) != 907638053982597162:
      return False
      
    elif m.content.startswith('!pick'):
      if (m.author.mention == captains[0]):

        if m.content == '!pick':
          return False

        else:
          player = m.content.split("!pick ", 1)[1]
          if player in playerlist:
            team1.append(player)
            playerlist.remove(player)
            team2.append(playerlist[0])
          elif (player == captains[1]) or (player == captains[0]): 
            return False

          else: 
            return False

          return True

      elif m.author.name == captains[1] or m.author.nick == captains[1]: return False
      else: 
        return False

    else:
      return False

  try: 
    await client.wait_for(event='message', check=check, timeout=60)

  except TimeoutError:
    await channel.send(embed=discord.Embed(title="Nice.",description=f"{captains[0]} doesn't have the smartest of brains and took too long to choose.\n\n**__This channel will close in 15 seconds.__**")); time.sleep(15)
    
    role.delete()
    channel.delete()
    vc1.delete()
    
    for i in playerlst: 
      i.move_to(waitingRoom); return

  await channel.send(embed=discord.Embed(description=f'Once you\'re finished with the game, don\'t forget to do **!end**!'))
  laMsg = await transcripts.send(embed=discord.Embed(title=f'Game ID: {games}.',description=f''))

  vc2 = await guild.create_voice_channel(name=f'Team-2-(2v2)-{games}',category=gamesCategory)
  await vc2.set_permissions(role, view_channel=True,connect=True,speak=True)
  vc2.user_limit = 2
  await vc2.set_permissions(role, view_channel=True,connect=True,speak=True,)
  await vc2.set_permissions(normRole, view_channel=False,connect=False,speak=False)
  
  await vc2.set_permissions(guild.get_role(901694160443166812), view_channel = True,connect = True,speak = True)
  await vc2.set_permissions(guild.get_role(909084700688134166), view_channel = True,connect = True,speak = True)
  await vc2.set_permissions(guild.get_role(901705859447529512), view_channel = True,connect = True,speak = True)
  await vc2.set_permissions(guild.get_role(901694174192087081), view_channel = True,connect = True,speak = True)

  for player in playerlst:
    if player.mention in team2:
      await player.move_to(vc2)

  await client.close();
  return {'deletings':[role,channel,vc1,vc2],'voiceChannels':[vc1,vc2],'teams':[team1,team2],'laMsg':laMsg}

async def end4v4(returnedDict, message):
  """4v4 Ending"""

  await client.login(TOKEN);

  guild = client.get_guild(901527310107279370)
  waitingRoom = client.get_channel(909083599318425660)
  gid = message.channel.name[9::]

  checkmark = await guild.fetch_emoji(909027132691329054)
  
  theMsg = await message.reply(embed=discord.Embed(title=f'React to close channel!',description=f'The channel wil close if **2** or more people react with {checkmark}, the channel will close.'))
  await theMsg.add_reaction(checkmark)

  def check(reaction, user):
    if reaction.count == 5: 
      return True

    return False

  try:
    await client.wait_for('reaction_add', check=check, timeout = 30)

  except TimeoutError:
    await message.channel.send(embed = discord.Embed(title = "rip", description = "You ran out of time.\n\n**If the game has already ended but no one is checking it off, ping a __mod__.**"))

  await message.channel.send(embed=discord.Embed(title="Thanks for playing!",description="This channel will close in 15 seconds."))

  for i in returnedDict['voiceChannels']:
    for j in i.members:
      await j.move_to(waitingRoom)

  time.sleep(15)
  for i in returnedDict['deletings']:
    await i.delete()

  await returnedDict['laMsg'].reply(embed=discord.Embed(title=f'Game ID: ``{gid}`` has ended. (Gamemode: 2v2)',description=f"__Team 1:__\n**1.** {returnedDict['team1'][0]}\n**2.** {returnedDict['team1'][1]}\n\n__Team 2:__\n**1.**{returnedDict['team2'][0]}\n**2.**{returnedDict['team2'][0]}"))

  await client.close();