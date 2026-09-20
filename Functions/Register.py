import requests, discord
from discord.ext import commands

APIKEY = 'a2f9308c-bf8e-4ecf-862c-544085f97e05'
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

with open("token.txt") as token: 
  TOKEN = token.read()

async def register(message):
  client.login(TOKEN)
  ign = message.content.split("!register ", 1)[1]
  discordTag = str(message.author)
  try: 
    UUID = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()['id']
    NAME = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()['name']
  except: 
    await message.channel.send(embed=discord.Embed(title=f'{message.author.mention}, **{ign}** is not a player!'))

  else:

    try:
      hypixelDTag = requests.get(f'https://api.hypixel.net/player?key={APIKEY}&uuid={UUID}').json()['player']['socialMedia']['links']['DISCORD']
    except:
      await message.channel.send(embed = discord.Embed(title="Lol", description = "You don't have your hypixel account linked to your discord account!\n\n__**Read #how-to-register.**__"))

    if hypixelDTag == discordTag:

      role = message.guild.get_role(902221222350311434)
      if role not in message.author.roles:
        await message.author.add_roles(role)

      await message.channel.send(embed=discord.Embed(title=f'You have succesfully registered as ``{ign}``!'))
      await message.author.edit(nick=NAME)
    else:
      await message.channel.send(embed=discord.Embed(title=f'That player is linked to ``{hypixelDTag}``, not you!'))

  await client.close()