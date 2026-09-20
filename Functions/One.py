import discord, random, time
from discord.ext import commands
from asyncio import run

with open("token.txt") as token:
    TOKEN  = token.read()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

soloMapPool = ["Lighthouse","Airshow","Orchestra","Speedway","Apollo","Crypt"]

async def start1v1(playerlst):
    """1v1 Starting Initialization"""

    await client.login(TOKEN)
    
    transcripts = await client.fetch_channel(902587505319247944) #The Transcripts Channel
    gamesCategory = await client.fetch_channel(907638053982597162) #The GamesCategory Channel
    guild = await client.fetch_guild(901527310107279370) #the literal server
    normRole = guild.get_role(902221222350311434) #the 'registered' role

    with open("GameCount.txt", "r") as f: 
        games = int(f.read()) #game count

    role = await guild.create_role(name=f'game-{games}')
    channel = await guild.create_text_channel(f'1v1-game-{games}', category=gamesCategory)

    await channel.set_permissions(normRole, read_messages = False, read_message_history = False, send_messages = False)
    await channel.set_permissions(role, read_messages = True, read_message_history = True, send_messages = True)
    await channel.set_permissions(guild.get_role(901694174192087081), read_messages = True, read_message_history = True, send_messages = True)
    await channel.set_permissions(guild.get_role(901694160443166812), read_messages = True, read_message_history = True, send_messages = True)
    await channel.set_permissions(guild.get_role(909084700688134166), read_messages = True, read_message_history = True, send_messages = True)
    await channel.set_permissions(guild.get_role(901705859447529512), read_messages = True, read_message_history = True, send_messages = True)

    p1 = playerlst[0].mention
    p2 = playerlst[1].mention

    msg = await transcripts.send(embed=discord.Embed(
        title=f'Game ID: ``{games}`` has started. (Gamemode: 1v1)',
        description=f'__Players involved:__\n**1.** {p1}\n**2.**{p2}'))
    
    vcId = await guild.create_voice_channel(name=f'1v1-{games}',category=gamesCategory)
    vc = await client.fetch_channel(vcId.id)
    await vc.set_permissions(role, view_channel = True,connect = True,speak = True)
    await vc.set_permissions(normRole, view_channel=False,connect=False,speak=False)
    await vc.set_permissions(guild.get_role(901694174192087081), view_channel = True, connect = True,  speak = True)
    await vc.set_permissions(guild.get_role(901694160443166812), view_channel = True, connect = True,  speak = True)
    await vc.set_permissions(guild.get_role(909084700688134166), view_channel = True, connect = True,  speak = True)
    await vc.set_permissions(guild.get_role(901705859447529512), view_channel = True, connect = True,  speak = True)
    await vc.edit(user_limit = 2)

    for player in playerlst:
        await player.add_roles(role)
        await player.move_to(vc)

    await channel.send(f'{role.mention},')

    embed = discord.Embed(
        title=f'Your chosen map to play on is ``{random.choices(soloMapPool)[0]}``',
        description=f'Once you\'re finished with the game, don\'t forget to do **!end**!')
        
    embed.set_footer(text = "Do keep in mind that if both sides agree, you may choose to play on a different map.")
    await channel.send(embed=embed)

    with open("GameCount.txt", "w") as f: 
        f.write(str(games + 1))

    await client.close()
    return {'deletings':[role,channel,vc],'voiceChannels':[vc],'players':[p1,p2],'msg':msg,"playerObjects":playerlst}

async def end1v1(channel, returnedDict):
    """1v1 Ending"""

    await client.login(TOKEN);
    
    waitingRoom = await client.fetch_channel(909083599318425660);
    await channel.send(embed=discord.Embed(title="Thanks for playing!",description="This channel will close in 15 seconds."));

    plMsg = f'__Players involved:__\n**1.** {returnedDict["players"][0]}\n**2.** {returnedDict["players"][1]}'

    for member in returnedDict["playerObjects"]:
        try:
            await member.move_to(waitingRoom);
        except Exception as e:
            print(e);

    GameID = channel.name[9::]
    time.sleep(15)

    for i in returnedDict['deletings']:
        await i.delete()

    await returnedDict['msg'].reply(embed=discord.Embed(title=f'Game ID: ``{GameID}`` has ended. (Gamemode: 1v1)',description=plMsg))
    await client.close();