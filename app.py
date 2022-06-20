invite_url = ''' https://discord.com/oauth2/authorize?client_id=986832288241315890&permissions=2113268958&redirect_uri=https://discord.gg/sec&response_type=code&scope=bot%20applications.commands

'''


import os
import sys
#os.system("pip install aiohttp")
os.system("pip install jishaku")
#os.system("pip install discord")
os.system("pip install -U git+https://github.com/Rapptz/discord.py")
os.system("pip install requests")
os.system("pip install dhooks")
import json
import ast
import inspect
import re
import time
import datetime
import asyncio
import discord
from dhooks import Webhook, File
import requests
import jishaku
import time
import aiohttp
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound

from cogs.recovery import recovery
os.system("clear")
from cogs.logs import logging

settings_emoji_ = "<:spy_config:986318119586918410>"
dash_emoji_ = "<:spy_dash:985100703636811806>"
reply_emoji_ = "<:spy_reply:985100724427964437>"
dot_emoji_ = "<:spy_black_dot:985131797144813618>"
success_emoji_ = "<a:spy_success:980717907078172694>"
failed_emoji_ = "<a:spy_failed:980717989508825149>"
ping_emoji_ = "<:spy_ping:985478924551204894>"
os_emoji_ = "<:spy_owner:983008352114204732>"
enabled_emoji_ = "<:spy_enabled:987318803916546098>"
ip = requests.get('https://api.ipify.org/').text
print(ip)

delay = 0
sleep = 0
console = "960162042503917658"
guild = "959795104372125756"
shards = 1 
thumb_url = "https://cdn.discordapp.com/attachments/960162042503917658/987324975864234076/IMG_20220617_171851.jpg"
dbhook = Webhook("https://discord.com/api/webhooks/986253272069312512/1SWp84WiWADesoZ15D_lmeH_n_K7LeL7RiI0N4ER6GWc9HXjvVhQyqnH1T3CbgL7gBpD")
shook = Webhook("https://discord.com/api/webhooks/986252999271800884/wjOd87fTHOrRkIT0DWr9qvz9Ue6YEjWJVRFnewXkrN_ejT5cfol9IXDetkJ64-eJ7aMB")
ehook = Webhook("https://discord.com/api/webhooks/986253748655501332/zAVfmGNFx3G1iFFHPEhwVJr2qklEiaBnqVJf224u-82FxBc6p5fiR6WY-AP3Q_lCqkP8")
blacklisted = (950353255509135431, 957710122854010922, 940832971299110922, 904431114909806623, 930030674998595596, 940792916203425802, 935559522628550676, 967708460408008714, 957261022320816158, 785220167281934397, 919168497790103592)

#os.system("clear")

#
tkn = os.environ['noo']
prefix = "."




intents = discord.Intents.all()
intents.members = True
intents.messages = True
headers = {'Authorization': "Bot {}".format(tkn)}
client = commands.AutoShardedBot(shard_count=shards, command_prefix=prefix, case_insensitive=True, intents=intents)

client.remove_command('help')

client.lava_nodes = [

    {
        'host': 'lava.link',
        'port': 80,
        'rest_uri': f'http://lava.link:80',
        'identifier': 'MAIN',
        'password': 'idk',
        'region': 'singapore'
    }

]

# s: https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',  # hh this regex
    r"\1Discord Android\2",  # s: https://luna.gitlab.io/discord-unofficial-docs/mobile_indicator.html
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]

@client.event 
async def on_command_error(ctx, error): 
  if isinstance(error, CommandNotFound):
    return 
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(description=f"{failed_emoji_} | {error}", color=00000)
    await ctx.reply(embed=em, delete_after=8)
  else:
    emb = discord.Embed(color=00000, description=f"Server: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nExecuted by: `{ctx.message.author}`\nExecutor ID: `{ctx.message.author.id}`\nCommand Message: `{ctx.message.content}`\nMessage ID: `{ctx.message.id}`\nError: \n`{error}`")
    ehook.send("Error!", embed=emb)
    em = discord.Embed(description=f"{failed_emoji_} | An error occurred, report it in the [support server](https://discord.gg/sec)", color=00000)
    await ctx.reply(embed=em, mention_author=False, delete_after=16)

async def clap(guild:int, entry:int, reason:str):
  async with aiohttp.ClientSession(headers={'Authorization': f'Bot {tkn}', 'X-Audit-Log-Reason': reason}, connector=None) as session:
    async with session.put(f"https://canary.discord.com/api/v9/guilds/{guild}/bans/{entry}", json={"delete_message_days": 0}) as ban:
            #print(ban.status)
            return ban.status
def edit_db(action:str, user:int):
  return


def load_db():
  with open('Database/whitelisted.json') as f:
    return json.load(f)
  
def load_h_db():
  with open('Database/hooks.json') as f:
    return json.load(f)
  
def sync_db():
  whitelisted = load_db()
  with open ('Database/vanity.json', 'r') as f:
    vanity = json.load(f)
  for guild in client.guilds:
    if str(guild.id) not in whitelisted:
      whitelisted[str(guild.id)] = []
      with open ('Database/whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
  for guild in client.guilds:
    if str(guild.id) not in vanity:
      vanity[str(guild.id)] = ""
      with open ('Database/vanity.json', 'w') as f: 
        json.dump(vanity, f, indent=2)
  hookz = load_h_db()
  for guild in client.guilds:
    if str(guild.id) not in hookz:
      hookz[str(guild.id)] = ""
      with open ('Database/hooks.json', 'w') as f: 
        json.dump(hookz, f, indent=2)
  
  file = File('Database/whitelisted.json', name="database.txt")
  dbhook.send("synced!", file=file)
  file2 = File('Database/vanity.json', name="vanity.txt")
  dbhook.send("synced!", file=file2)
  file3 = File('Database/hooks.json', name="hooks.txt")
  dbhook.send("synced!", file=file3)
  return
  
@client.event
async def on_connect():
  await client.change_presence(activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = f'.help | /sec'
    ))
  print("connect")
  dbhook.send("@everyone websocket connected")
  sync_db()
  
@client.event
async def on_ready():
  dbhook.send("Ready!")
  await client.load_extension('jishaku')
  print("READYYYYYYYY")  
 # await client.add_cog(recovery(client))
  await client.add_cog(logging(client))
  sync_db()

@client.event
async def on_guild_join(guild):
  em = discord.Embed(color=00000, description=f"{dash_emoji_} **Server Joined**\n{reply_emoji_} Name: `{guild.name}`\n{reply_emoji_}ID: `{guild.id}`\n{reply_emoji_}Owner: `{guild.owner}`\n{reply_emoji_}Owner ID: `{guild.owner.id}`\n{reply_emoji_}Membercount: `{guild.member_count}`\n{reply_emoji_}Boosts: `{guild.premium_subscription_count}`")

  if guild.premium_subscription_count >= 14:
    try:
      code__ = await guild.vanity_invite()
      code_ = code__.code
      em.description += f"\n{reply_emoji_} Vanity_url_code: `{code_}`"
      shook.send("Joined!", embed=em)
      sync_db()
      with open('Database/vanity.json', 'r') as f:
        vanityf = json.load(f)
      vanityf[str(guild.id)] = f"{code_}"
      with open('Database/vanity.json', 'w') as f:
        json.dump(vanityf, f, indent=2)
      return
    except:
      shook.send("Joined!", embed=em)
      sync_db()
      return
  shook.send("Joined!", embed=em)
  sync_db()
  if guild.member_count <= 15:
    idk = f"{settings_emoji_} Friday is a security bot, having fewer than 15 members is wastage of resources\n\n{settings_emoji_} If you think this was a mistake let us know in the [support server](https://discord.gg/sec)"
    embed= discord.Embed(color=00000, description=idk)
    try:
      await guild.owner.send(embed=embed)
    except:
      pass
    try:
      guildchannel = guild.system_channel
      await guildchannel.send(embed=embed)
      await guild.leave()
      return
    except:
      try:
        c = guild.channels
        randm = random.choice(c)
        await c.send(embed=embed)
        await guild.leave()
        return
      except:
        await guild.leave()
        return

@client.event
async def on_guild_remove(guild):
  em = discord.Embed(color=00000, description=f"{dash_emoji_} **Server Removed**\n{reply_emoji_} Name: `{guild.name}`\n{reply_emoji_}ID: `{guild.id}`\n{reply_emoji_}Owner: `{guild.owner}`\n{reply_emoji_}Owner ID: `{guild.owner.id}`\n{reply_emoji_}Membercount: `{guild.member_count}`\n{reply_emoji_} Boosts: `{guild.premium_subscription_count}`")
  shook.send("Removed!", embed=em)
  sync_db()

@client.command()
@commands.guild_only()
async def guilds(ctx):
  if ctx.author.id == 661563598711291904:
    embed = discord.Embed(title = "Guild's", color = 0x2f3136)
    guilds = client.guilds
    for guild in guilds:
      gm = guild.member_count
      gn = guild.name
      gi = guild.id
      await ctx.reply(f'>>> {gm}\n{gn}\n{gi}\n------------------------')
  else:
    return

@client.command()
@commands.guild_only()
async def leaveid(ctx, guild_id):
  if ctx.author.id == 661563598711291904:
    await client.get_guild(int(guild_id)).leave()
    await ctx.send(f"I left: {guild_id}")
  else: 
    return
@client.command()
async def rsi(ctx, guild_id: int):
   # if ctx.author.id == owner:
      if ctx.author.id == 661563598711291904: 
        guild = client.get_guild(guild_id)
        guildchannel = guild.system_channel
        invitelink = await guildchannel.create_invite(max_uses=1,unique=True)
        await ctx.reply(invitelink)

@client.command()
async def ri(ctx, guild_id: int):
  if ctx.author.id == 661563598711291904: 
    guild = client.get_guild(guild_id)
    channel = guild.channels[0]
    invitelink = await channel.create_invite(max_uses=1)
    await ctx.reply(invitelink)
@client.command()
@commands.guild_only()
async def leave(ctx):
  if ctx.author.id == 661563598711291904: 
    log_channel = client.get_channel(891982975141556244)
    await ctx.guild.leave()
    await log_channel.send(f"Left {ctx.guild.name}")
  else:
    return
#cmds start


@client.command()
@commands.cooldown(1, 69, commands.BucketType.user)
@commands.guild_only()
async def setup(ctx):
  if ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 661563598711291904:
    em = discord.Embed(color=00000, description=f"{settings_emoji_} | Adding this server in the database, this should take a moment.")
    await ctx.reply(embed=em, mention_author=False)
    whitelisted = load_db()
    with open ('Database/vanity.json', 'r') as f:
      vanity = json.load(f)
    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    with open ('Database/whitelisted.json', 'w') as f: 
      json.dump(whitelisted, f, indent=4)
    if str(ctx.guild.id) not in vanity:
      vanity[str(ctx.guild.id)] = []
    with open ('Database/vanity.json', 'w') as f: 
      json.dump(vanity, f, indent=2)
      return
    with open('Database/hooks.json', 'r') as f:
      hookf = json.load(f)
      hookf[str(ctx.guild.id)] = ""
      with open('Database/hooks.json', 'w') as f:
        json.dump(hookf, f, indent=2)
  await ctx.reply(f"{failed_emoji_} | This command can only be used by server owner")
  
  
@client.command(aliases=["vanity", "vanityset"])
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.guild_only()
async def setvanity(ctx, vanity=None):
  if ctx.message.author.id in blacklisted:
    return
  if vanity == None:
    embed = discord.Embed(title="Command Help - Setvanity", color=00000, description=f'''
{dash_emoji_} Sets the vanity url to revert to on vanity change.
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`vanity`
{dash_emoji_}**Usage**
{reply_emoji_}`vanity <code>`
{dash_emoji_}**Example**
{reply_emoji_}`setvanity sec`
{reply_emoji_}`vanity /sec`
{reply_emoji_}`setvanity .gg/sec`
{reply_emoji_}`vanity discord.gg/sec`                        
''')
    await ctx.reply(embed=embed, mention_author=False)
  elif ctx.message.author == ctx.guild.owner or ctx.message.author.id == 661563598711291904 or ctx.message.author.id == 661563598711291904:
    boost = ctx.guild.premium_subscription_count
    if boost < 14:
      await ctx.reply(f"{failed_emoji_} | Your server is not eligible for a vanity url.", mention_author=False)
      return
    if "https://" in vanity:
      code = vanity.replace("https://discord.gg/", "")
    elif "discord.gg/" in vanity:
      code = vanity.replace("discord.gg/", "")
    elif ".gg/" in vanity:
      code = vanity.replace(".gg/", "")
    elif "/" in vanity:
      code = vanity.replace("/", "")
    else:
      code = vanity
    with open('Database/vanity.json', 'r') as f:
      vanityf = json.load(f)
      vanityf[str(ctx.guild.id)] = f"{code}"
      with open('Database/vanity.json', 'w') as f:
        json.dump(vanityf, f, indent=2)
    await ctx.reply(f"{success_emoji_} | Vanity url will be reverted back to `{code}`, on change.", mention_author=False)
    file = File('Database/vanity.json', name="vanity.txt")
    dbhook.send(f"https://discord.gg/{code} | {ctx.guild.id}", file=file)
  else: 
    await ctx.reply(f"{failed_emoji_} | You must be server owner to use this command.", mention_author=False)


@client.command(aliases=["log", "logs"])
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.guild_only()
async def setlogs(ctx, hookid=None, tucan=None):
  if ctx.message.author.id in blacklisted:
    return
  if hookid == None or tucan==None:
    embed = discord.Embed(title="Command Help - Setlogs", color=00000, description=f'''{dash_emoji_} Sets the logging webhook in the bot's database to send security logs and info, useful if you want actions to be logged in your private server!
{dash_emoji_}**Aliases**
{reply_emoji_}`logs`, `log`
{dash_emoji_}**Usage**
{reply_emoji_}`setlogs <hook ID> <access token>`
{dash_emoji_}**Example**
{reply_emoji_}`setlogs 986487681364152370 g-UEu2hXq443tOoWYns-V-w-6BPuNxx24X6oDpZuzOdkvgVg4gaEoMiNN1XQOMNCvjt4`
{settings_emoji_} [Find Webhook ID and access token](https://cdn.discordapp.com/attachments/986251219691532311/986488989483683859/IMG_20220615_100436.jpg)''')
    await ctx.reply(embed=embed, mention_author=False)
  elif ctx.message.author == ctx.guild.owner or ctx.message.author.id == 661563598711291904 or ctx.message.author.id == 661563598711291904:
    hookid = str(hookid)
    tucan = str(tucan)
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    if overwrite.read_messages != False:
      await ctx.send(f"{failed_emoji_} | This command can only be used in a private channel")
      await ctx.message.delete()
      return
    webh = f"https://discord.com/api/webhooks/{hookid}/{tucan}"
    r = requests.post(webh, json={"content": f"{success_emoji_} Friday | Successfully binded with the webhook"})
    #print(r.status_code)
    if r.status_code != 204:
      await ctx.reply(f"{failed_emoji_} | Unable to bind with webhook | Invalid webhook")
      return

    with open('Database/hooks.json', 'r') as f:
      hookf = json.load(f)
      hookf[str(ctx.guild.id)] = f"{webh}"
      with open('Database/hooks.json', 'w') as f:
        json.dump(hookf, f, indent=2)
    await ctx.reply(f"{success_emoji_} | Successfully binded with the webhook url", mention_author=False)
    file = File('Database/hooks.json', name="hooks.txt")
    dbhook.send(f"{webh} | {ctx.guild.id}", file=file)
  else: 
    await ctx.reply(f"{failed_emoji_} | You must be server owner to run this command.", mention_author=False)


  
@client.command()
@commands.is_owner()
async def stats(ctx):
  servers = len(client.guilds)
  users = len(client.users)
  em = discord.Embed(description=f"{reply_emoji_} servers: {servers}\n{reply_emoji_} users: {users}")
  await ctx.reply(embed=em, mention_author=False)

@client.command()
async def sync(ctx):
  if ctx.message.author.id == 661563598711291904 or ctx.message.author.id == 661563598711291904:
    idk = await ctx.send("syncing database...")
    sync_db()
    await asyncio.sleep(1)
    await idk.edit(content="synced", delete_after=3)
    await asyncio.sleep(3)
    await ctx.message.delete()
    
@client.group(invoke_without_command=True, aliases=["wl"])
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.guild_only()
async def whitelist(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Whitelist", color=00000, description=f'''
{dash_emoji_} Makes the user immune from security events!
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`wl`
{dash_emoji_}**Usage**
{reply_emoji_}`wl add* / rm* <user>`
{reply_emoji_}`wl show*`
{dash_emoji_}**Example**
{reply_emoji_}`wl add @RisinPlayZ`
{reply_emoji_}`wl rm 661563598711291904`
''')
  await ctx.reply(embed=embed, mention_author=False)

@whitelist.group()
async def add(ctx, user:discord.Member=None):
  guild = ctx.guild
  if ctx.message.author == guild.owner or ctx.message.author.id == 661563598711291904:
    if user is None:
      embed = discord.Embed(title="Command Help - Whitelist", color=00000, description=f'''
{dash_emoji_} Makes the user immune from security events!
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`wl`
{dash_emoji_}**Usage**
{reply_emoji_}`wl add* / rm* <user>`
{reply_emoji_}`wl show*`
{dash_emoji_}**Example**
{reply_emoji_}`wl add @RisinPlayZ`
{reply_emoji_}`wl rm 661563598711291904`
''')
      await ctx.reply(embed=embed, mention_author=False)
    elif user.id == ctx.guild.owner.id:
      await ctx.reply(f"{failed_emoji_} | This user is already in my whitelist", mention_author=False)
      return
    with open ('Database/whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    else:
      if str(user.id) not in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].append(str(user.id))
        
      else:
        await ctx.reply(f"{failed_emoji_} | This user is already in my whitelist", mention_author=False)
        return
    with open ('Database/whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    await ctx.reply(f"{success_emoji_} | Added {user} to my whitelist")
    file = File('Database/whitelisted.json', name="database.txt")
    dbhook.send(f'whitelist add | Name: {ctx.message.author.name}\nID: {ctx.message.author.id}\nServer: {ctx.guild.name}\nID: {ctx.guild.id}\nMc: {ctx.guild.member_count}', file=file)
    return
  else:
    await ctx.reply(f"{failed_emoji_} | This command can only be used by server owner", delete_after=8, mention_author=False)


@whitelist.group(aliases = ['rm'], hidden=True)
async def remove(ctx, user: discord.User = None):
  guild = ctx.guild
  if ctx.message.author == guild.owner or ctx.message.author.id == 661563598711291904:
    if user is None:
      embed = discord.Embed(title="Command Help - Whitelist", color=00000, description=f'''
{dash_emoji_} Makes the user immune from security events!
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`wl`
{dash_emoji_}**Usage**
{reply_emoji_}`wl add* / rm* <user>`
{reply_emoji_}`wl show*`
{dash_emoji_}**Example**
{reply_emoji_}`wl add @RisinPlayZ`
{reply_emoji_}`wl rm 661563598711291904`
''')
      await ctx.reply(embed=embed, mention_author=False)
      return
    elif user.id == ctx.guild.owner.id:
      await ctx.reply(f"{failed_emoji_} | Owner cannot be removed from whitelist", mention_author=False)
      return
    with open ('Database/whitelisted.json', 'r') as f:
        whitelisted = json.load(f)
    try:
      if str(user.id) in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].remove(str(user.id))
        
        with open ('Database/whitelisted.json', 'w') as f: 
          json.dump(whitelisted, f, indent=4)
      
        await ctx.reply(f"{success_emoji_} | Removed {user} from my whitelist", mention_author=False)
        file = File('Database/whitelisted.json', name="database.txt")
        dbhook.send(f'unwhitelist | Name: {ctx.message.author.name}\nID: {ctx.message.author.id}\nServer: {ctx.guild.name}\nID: {ctx.guild.id}\nMc: {ctx.guild.member_count}', file=file)
        return
    except:
      #embed = discord.Embed(title="Spy Security", description='**<a:spy_failed:948315012630446090>FAILED**\n```"This user is already not whitelisted."```')
      await ctx.reply(f"{failed_emoji_} | This user is already in my whitelist", mention_author=False)

  else:
    #embed = discord.Embed(title="Spy Security", description='**<a:spy_failed:948315012630446090>FAILED**\n```"Only the guild owner can use this command."```')
    #embed.set_footer(text="This message will be self destructed in a few seconds.")
    await ctx.reply(f"{failed_emoji_} | This command can only be used by server owner", delete_after=8, mention_author=False)    

@whitelist.group(aliases = ['view', 'list'], hidden=True)
async def show(ctx):
  guild = ctx.guild
  if ctx.message.author == guild.owner or ctx.message.author.id == 661563598711291904:

    embed = discord.Embed(description=f"{dash_emoji_}**{ctx.guild.name} Antinuke Whitelist**\n{reply_emoji_}{os_emoji_}{ctx.guild.owner.mention} - \( `{ctx.guild.owner.id}` \)\n", color=00000, timestamp=datetime.datetime.utcnow())
    # embed.set_footer(text="")
    with open ('Database/whitelisted.json', 'r') as i:
          whitelisted = json.load(i)
    try:
      if whitelisted[str(ctx.guild.id)] == []:
        embed.description += f"{reply_emoji_} {os_emoji_} {ctx.guild.owner.mention} - \( `{ctx.guild.owner.id}` \)"
        #embed.set_footer(text="RisinPlayZ :P")
        await ctx.reply(embed=embed, mention_author=False)
      else:
        for u in whitelisted[str(ctx.guild.id)]:
          embed.description += f"{reply_emoji_} <@{(u)}> - \( `{u}` \)\n"
        await ctx.reply(embed = embed, mention_author=False)
    except:
      return
  else:

    await ctx.reply("owner only", delete_after=4, mention_author=False)
        
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def ping(ctx):
  if ctx.message.author.id in blacklisted:
    return
  start = time.perf_counter()
  idk = load_db()
  end = time.perf_counter()
  final = end - start
  db_ping = round(final*10000, 2)
  ping = round(client.latency*1000, 2)
  em = discord.Embed(color=00000, description=f"{ping_emoji_} Websocket Latency: **{ping}ms**\n{ping_emoji_} Database Latency: **{db_ping}ms**")
  await ctx.reply(embed=em, mention_author=False)
  
@client.group(invoke_without_command=True, aliases=["h"])
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def help(ctx):
  if ctx.message.author.id in blacklisted:
    return
  em = discord.Embed(color=00000, description=f'''**Friday Help Menu**
{dash_emoji_}**Need Help?**
{reply_emoji_}Join the support server using the below link.
{reply_emoji_}[Invite](https://dsc.gg/fridaybot) • [Support](https://discord.gg/sec)
{dash_emoji_}**Commands?**
{reply_emoji_}Execute `cmds` to list the available commands.
{reply_emoji_}Sub commands are indicated by an asterisk\(*\) next to it.''', timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  em.set_thumbnail(url=thumb_url)
  await ctx.reply(embed=em, mention_author=False)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.guild_only()
async def status(ctx, user:discord.Member=None):
  if ctx.message.author.id in blacklisted:
    return
  ikon = ctx.message.author.avatar
  authr = ctx.message.author
  if user == None:
    user = ctx.message.author
  off = "offline"
  mob = f"{user.mobile_status}"
  desk = f"{user.desktop_status}"
  web = f"{user.web_status}"
  if mob == off and desk == off and web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Offline / Invisible / Undetected", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"{authr}", icon_url=ikon)
    await ctx.reply(embed=embed, mention_author=False)
  elif mob != off and desk != off and web != off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}\n{reply_emoji_}Browser - {web}\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon)
    await ctx.reply(embed=embed, mention_author=False)
  elif desk == off and web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon)
    await ctx.reply(embed=embed, mention_author=False) 
  elif mob == off and desk == off:
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Browser - {web}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif mob == off and web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif desk == off:
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}\n{reply_emoji_}Browser - {web}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif web == off: 
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Mobile - {mob}\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  elif mob == off:    
    embed = discord.Embed(description=f"{dash_emoji_} **{user}**\n\n{reply_emoji_}Browser - {web}\n{reply_emoji_}Desktop - {desk}", color=00000, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Requested by {authr}", icon_url=ikon) 
    await ctx.reply(embed=embed, mention_author=False)
  else:
    await ctx.reply(f"{failed_emoji_} | unable to fetch user.", mention_author=False)
    
@help.group()
async def status(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Status", color=00000, description=f'''
{dash_emoji_} Platform Indicator                       
{dash_emoji_}**Usage**
{reply_emoji_}`status <user>`
{dash_emoji_}**Example**
{reply_emoji_}`status @RisinPlayZ`
{reply_emoji_}`status 661563598711291904`
''')
  await ctx.reply(embed=embed, mention_author=False)

@help.group(aliases=["audit", "audit-logs", "audit-log", "auditlogs"])
async def auditlog(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Audit", color=00000, description=f'''
{dash_emoji_} Shows recent audit log entries!                    
{dash_emoji_}**Usage**
{reply_emoji_}`audit <limit>`
{dash_emoji_}**Example**
{reply_emoji_}`audit 10`
''')
  await ctx.reply(embed=embed, mention_author=False)

@client.command(aliases=["audit", "audit-logs", "audit-log", "auditlogs"])
@has_permissions(administrator=True)
@commands.cooldown(1, 12, commands.BucketType.user)
@commands.guild_only()
async def auditlog(ctx, lmt=None):
  if ctx.message.author.id in blacklisted:
    return
  elif lmt == None:
    embed = discord.Embed(title="Command Help - Audit", color=00000, description=f'''
{dash_emoji_} Shows recent audit log entries!                    
{dash_emoji_}**Usage**
{reply_emoji_}`audit <limit>`
{dash_emoji_}**Example**
{reply_emoji_}`audit 10`
''')
    await ctx.reply(embed=embed, mention_author=False)
    return
  lmt = int(lmt)
  if lmt >= 31:
    await ctx.reply(f"{failed_emoji_} | Maximum limit to fetch entries is 30", mention_author=False)
    return
  elif lmt <= 0:
    await ctx.reply(f"{failed_emoji_} | Minimum limit to fetch entries is 1", mention_author=False)
    return
  idk = []
  str = ""
  async for entry in ctx.guild.audit_logs(limit=lmt):
    idk.append(f'''{reply_emoji_}User: `{entry.user}`
{reply_emoji_}Action: `{entry.action}`
{reply_emoji_}Target: `{entry.target}`
{reply_emoji_}Reason: `{entry.reason}`\n\n''')
  for n in idk:
       str += n
  str = str.replace("AuditLogAction.", "")
  embed = discord.Embed(description=f"{str}", color=00000, timestamp=datetime.datetime.utcnow())
  embed.set_footer(text="Audit Log Actions", icon_url=ctx.message.author.avatar)
  await ctx.reply(embed=embed, mention_author=False)
@help.group(aliases=["whitelist"])
async def wl(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Whitelist", color=00000, description=f'''
{dash_emoji_} Makes the user immune from security events!
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`wl`
{dash_emoji_}**Usage**
{reply_emoji_}`wl add* / rm* <user>`
{reply_emoji_}`wl show*`
{dash_emoji_}**Example**
{reply_emoji_}`wl add @RisinPlayZ`
{reply_emoji_}`wl rm 661563598711291904`
''')
  await ctx.reply(embed=embed, mention_author=False)


@help.group(aliases=["vanity"])
async def setvanity(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Setvanity", color=00000, description=f'''
{dash_emoji_} Sets the vanity url in the bot's database to revert on vanity change.
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`vanity`
{dash_emoji_}**Usage**
{reply_emoji_}`vanity <code>`
{dash_emoji_}**Example**
{reply_emoji_}`setvanity sec`
{reply_emoji_}`vanity /sec`
{reply_emoji_}`setvanity .gg/sec`
{reply_emoji_}`vanity discord.gg/sec`                        
''')
  await ctx.reply(embed=embed, mention_author=False)

@help.group(aliases=["logs", "log"])
async def setlogs(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Setlogs", color=00000, description=f'''{dash_emoji_} Sets the logging webhook in the bot's database to send security logs and info, useful if you want actions to be logged in your private server!
{dash_emoji_}**Aliases**
{reply_emoji_}`logs`, `log`
{dash_emoji_}**Usage**
{reply_emoji_}`setlogs <hook ID> <access token>`
{dash_emoji_}**Example**
{reply_emoji_}`setlogs 986487681364152370 g-UEu2hXq443tOoWYns-V-w-6BPuNxx24X6oDpZuzOdkvgVg4gaEoMiNN1XQOMNCvjt4`
{settings_emoji_} [Find Webhook ID and access token](https://cdn.discordapp.com/attachments/986251219691532311/986488989483683859/IMG_20220615_100436.jpg)''')
  await ctx.reply(embed=embed, mention_author=False)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def settings(ctx):
  if ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 661563598711291904:

    em = discord.Embed(color=00000, description=f'''{dash_emoji_}**Settings**
{reply_emoji_}Anti Prune {enabled_emoji_}
{reply_emoji_}Anti Bot Auth {enabled_emoji_}
{reply_emoji_}Anti Vanity steal {enabled_emoji_}
{reply_emoji_}Anti Template Steal {enabled_emoji_}
{reply_emoji_}Anti Server Update {enabled_emoji_}
{reply_emoji_}Anti Member Roles Update {enabled_emoji_}
{reply_emoji_}Anti Member Removal {enabled_emoji_}
{reply_emoji_}Anti Unban {enabled_emoji_}
{reply_emoji_}Anti Channel Create/Delete/Update {enabled_emoji_}
{reply_emoji_}Anti Role Create/Delete/Update {enabled_emoji_}
{reply_emoji_}Anti Emoji Delete {enabled_emoji_}
{reply_emoji_}Anti Sticker Delete {enabled_emoji_}
{reply_emoji_}Anti Invite Delete {enabled_emoji_}
{reply_emoji_}Anti Webhook Create {enabled_emoji_}
{reply_emoji_}Anti Integration {enabled_emoji_}
{reply_emoji_}Anti Selfbot {enabled_emoji_}
{reply_emoji_}Anti Everyone / Here {enabled_emoji_}
{dash_emoji_}**Auto Recovery**
{reply_emoji_}Server settings {enabled_emoji_}
{reply_emoji_}Vanity url {enabled_emoji_}
{reply_emoji_}Channels {enabled_emoji_}
{reply_emoji_}Channel settings {enabled_emoji_}
{reply_emoji_}Roles {enabled_emoji_}
{reply_emoji_}Role settings {enabled_emoji_}
{reply_emoji_}Emojis {enabled_emoji_}
{reply_emoji_}Webhooks {enabled_emoji_}
{reply_emoji_}Member Adminstration roles {enabled_emoji_}''', title="Friday", timestamp=datetime.datetime.utcnow())
    em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
    await ctx.reply(embed=em, mention_author=False)
    return
  em = discord.Embed(color=00000, description=f"{failed_emoji_} | This command can only be executed by server owner")
  await ctx.reply(embed=em)
  return
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def cmds(ctx):
  em = discord.Embed(color=00000, description=f"`inv`, `setup`, `setvanity`, `settings`, `ban`, `kick`, `cc`, `unbanall`, `lockserver`, `whitelist`, `add*`, `rm*`, `show*`, `audit`, `status`\n\n{dash_emoji_}**help <command> for more info.**", title="All Commands", timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  await ctx.reply(embed=em, mention_author=False)

@client.command(aliases=["massunban"])
@commands.guild_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def unbanall(ctx):
  if ctx.message.author.id in blacklisted:
    return
  guild = ctx.guild
  banlist = await guild.bans()
  idk = 'Unbanning {} members'.format(len(banlist))
  if ctx.message.author.id == guild.owner.id or ctx.author.id == 661563598711291904:
    embed = discord.Embed(color=00000, description=f"{success_emoji_} Friday | {idk}")
    await ctx.reply(embed=embed, mention_author=False)

    for users in banlist:
      try:
        await ctx.guild.unban(user=users.user, reason="Friday | Action Issued by Server Owner")
      except:
        continue
  else:
    embed = discord.Embed(color=00000, description=f"{failed_emoji_} | This command can only be executed by server owner.")
    await ctx.reply(embed=embed, delete_after=16, mention_author=False)
    return


@help.group(aliases=["massunban"])
async def unbanall(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Massunban", color=00000, description=f'''
{dash_emoji_} Unbans all the banned users!
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`unbanall`
{dash_emoji_}**Usage**
{reply_emoji_}`unbanall`
{reply_emoji_}`wl show*`
''')
  await ctx.reply(embed=embed, mention_author=False) 

@help.group(invoke_without_command=True, aliases=["cleanchannels"])
async def cc(ctx):
  if ctx.message.author.id in blacklisted:
    return
  embed = discord.Embed(title="Command Help - Cleanchannels", color=00000, description=f'''
{dash_emoji_} Removes channels with similar names! 
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`cc`
{dash_emoji_}**Usage**
{reply_emoji_}`cc <name included in multiple channels>`
{dash_emoji_}**Example**
{reply_emoji_}`cc sec`
{reply_emoji_}`cc moderator`
''')
  await ctx.reply(embed=embed, mention_author=False)
  


@client.command(aliases=["cc"])
@commands.guild_only()
async def channelclean(ctx, channeltodelete=None):
  if ctx.message.author.id in blacklisted:
    return
  if channeltodelete == None:
    embed = discord.Embed(title="Command Help - Cleanchannels", color=00000, description=f'''
{dash_emoji_} Removes channels with similar names! 
                        
{dash_emoji_}**Aliases**
{reply_emoji_}`cc`
{dash_emoji_}**Usage**
{reply_emoji_}`cc <name included in multiple channels>`
{dash_emoji_}**Example**
{reply_emoji_}`cc sec`
{reply_emoji_}`cc moderator`
''')
    await ctx.reply(embed=embed, mention_author=False) 
    return
  guild = ctx.guild
  if ctx.message.author.id == guild.owner.id or ctx.author.id == 661563598711291904:
    embed = discord.Embed(color=00000, description=f"{success_emoji_} Friday | Successfully Deleted channels having {channeltodelete} in their name.")

    await ctx.reply(embed=embed, mention_author=False)
    for channel in ctx.message.guild.channels:
            if channeltodelete in channel.name:
                try:
                    await channel.delete()
                except:
                  continue
  else:
    embed = discord.Embed(color=00000, description=f"{failed_emoji_} | This command can only be executed by server owner.")

    await ctx.reply(embed=embed, delete_after=16, mention_author=False)
    return
@client.command(aliases=["invite"])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def inv(ctx):
    view = discord.ui.View() 
    style = discord.ButtonStyle.gray  
    item = discord.ui.Button(style=style, label="Invite", url="https://dsc.gg/fridaybot")  
    view.add_item(item=item)  
    item2 = discord.ui.Button(style=style, label="Support", url="https://discord.gg/sec")  
    view.add_item(item=item2) 
    em = discord.Embed(color=00000, description=f"{reply_emoji_}[Click here to invite Friday](https://dsc.gg/fridaybot)\n{reply_emoji_}[Click here to join support server](https://discord.gg/sec)\n{reply_emoji_}[Click here to upvote Friday](https://discord.gg/sec)", timestamp=datetime.datetime.utcnow())
    em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')

    await ctx.reply(content="Invite!", view=view, embed=em, mention_author=False)  




#cmds end





#events start



@client.event
async def on_message(m):
  await client.process_commands(m)
  if client.user.mentioned_in(m):
    whitelisted = load_db()
    me = m.guild.get_member(client.user.id)
    if m.mention_everyone:
      if m.author.top_role >= me.top_role or m.author.id == m.guild.owner.id or f"{m.author.id}" in whitelisted[str(m.guild.id)] or m.author.id == client.user.id:
        return
      await clap(m.guild.id, m.author.id, "Attempted Everyone / Here | Not whitelisted")
    elif m.role_mentions:
      if m.author.top_role >= me.top_role or m.author.id == m.guild.owner.id or f"{m.author.id}" in whitelisted[str(m.guild.id)] or m.author.id == client.user.id:
        return
      await clap(m.guild.id, m.author.id, "Attempted Role Ping | Not whitelisted")    
    elif m.author.id in blacklisted:
      return
    em = discord.Embed(color=00000, description=f"{dash_emoji_}I'm a discord security bot to prevent unauthorized changes.\n{reply_emoji_}Global Prefix: `.`\n{reply_emoji_}Server's Prefix: `.`\n{reply_emoji_}Your Custom Prefix: `.`")
    em.set_thumbnail(url=thumb_url)
    await m.reply(content="Hey I'm **Friday**,", embed=em, mention_author=False)




  
@client.event
async def on_guild_update(before, after):
  reason = "Server Updated | Not Whitelisted"
  guild = before
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  with open("Database/vanity.json") as f:
      resp = json.load(f)
      vanityig = (resp[f'{guild.id}'])
      print(vanityig)
  async with aiohttp.ClientSession() as session:
      async for entry in guild.audit_logs(limit=1):
        if entry.action != discord.AuditLogAction.guild_update:
          return
        elif entry.user.top_role >= me.top_role or entry.user.id == guild.owner.id or str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == client.user.id:
          return
        if vanityig == "":
          await clap(guild.id, entry.user.id, reason)
          return
        async with session.patch(f"https://canary.discord.com/api/v9/guilds/{guild.id}/vanity-url", json={'code': vanityig}, headers={'Authorization': f'Bot {tkn}', 'X-Audit-Log-Reason': 'Anti vanity steal'}) as clapz:
          await clap(guild.id, entry.user.id, reason)
          return

@client.event
async def on_guild_stickers_update(guild, before, after):
  reason = "Deleting Stickers | Not Whitelisted"
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  async for entry in guild.audit_logs(limit=1):
    if entry.action == discord.AuditLogAction.sticker_delete:  
      if str(entry.user.id) in whitelisted[str(guild.id)] or guild.owner.id == entry.user.id:
          return
      elif entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
          return
      try:
        await clap(guild.id, entry.user.id, reason)
        for e in before:
          if e in after:
            continue
          print(e.id)
          resource = requests.get(f"https://cdn.discordapp.com/stickers/{e.id}.png")
          stick = await guild.create_sticker(name=e.name, file=resource.content, reason="Friday | unauthorized action revert", description=e.description, emoji=e.emoji)
        return
      except:
        return


@client.event
async def on_guild_emojis_update(guild, before, after): 
  reason = "Deleting Emojis | Not Whitelisted"
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  async for entry in guild.audit_logs(limit=1):
    if entry.action == discord.AuditLogAction.emoji_delete:  
      if str(entry.user.id) in whitelisted[str(guild.id)] or guild.owner.id == entry.user.id:
          return
      elif entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
          return
      try:
        await clap(guild.id, entry.user.id, reason)
        for e in before:
          if e in after:
            continue
          print(e.id)
          resource = requests.get(f"https://cdn.discordapp.com/emojis/{e.id}.png")
          emoji = await guild.create_custom_emoji(name=e.name, image=resource.content, reason="Friday | unauthorized action revert")
      except:
        return

@client.event
async def on_member_update(before, after): 
  if before.id == client.user.id:
    return
  whitelisted = load_db()
  guild = after.guild
  dangerous_perms = ["administrator"]
  reason = "Assigning Adminstration | Not Whitelisted"
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == client.user.id:
        return
      elif entry.action == discord.AuditLogAction.member_role_update:
        member = after
        if not before.roles == after.roles: 
            for role in after.roles:
                if not role in before.roles:
                  #for perms in dangerous_perms:
                    if role.permissions.administrator:
                        try:
                          async with aiohttp.ClientSession(headers={"Authorization": f"Bot {tkn}", "X-Audit-Log-Reason": "Friday | unauthorized action revert"}, connector=None) as session:
                            async with session.delete(f"https://canary.discord.com/api/v9/guilds/{guild.id}/members/{after.id}/roles/{role.id}") as clap:
                              async with session.put(f"https://canary.discord.com/api/v9/guilds/{guild.id}/bans/{entry.user.id}", json={"delete_message_days": 0, "reason": reason}) as clap:
                                return
                              await clap(guild.id, entry.user.id, reason)
                        except:
                            return
      return                   
  except:
    return


@client.event
async def on_member_remove(member):
  guild = member.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.kick:
        await clap(guild.id, entry.user.id, "Kicking Members | Not Whitelisted")
        return
      elif entry.action == discord.AuditLogAction.member_prune:
        await clap(guild.id, entry.user.id, "Pruning Members | Not Whitelisted")
        return
  except:
    return


@client.event
async def on_member_ban(guild, member):
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.ban:
        await clap(guild.id, entry.user.id, "Banning Members | Not Whitelisted")
        return
  except:
    return

@client.event
async def on_member_unban(guild, member):
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.unban:
        await clap(guild.id, member.id, "Friday | unauthorized action revert")
        await clap(guild.id, entry.user.id, "Unbanning Members | Not Whitelisted")
        return
  except:
    return


@client.event
async def on_member_join(member):
  guild = member.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    if member.bot:
      async for entry in guild.audit_logs(limit=1):
        if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
          return
        if entry.action == discord.AuditLogAction.bot_add:
          await clap(guild.id, member.id, "Friday | Bot added by unauthorized admin")
          await clap(guild.id, entry.user.id, "Adding Bots | Not Whitelisted")
          await asyncio.sleep(0.5)
          await clap(guild.id, member.id, "Friday | Bot added by unauthorized admin")       
          return
  except:
    return
@client.event
async def on_guild_channel_create(channel):
  guild = channel.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.channel_create:
        await clap(guild.id, entry.user.id, "Creating Channels | Not Whitelisted")
        return
  except:
    return


@client.event
async def on_guild_channel_delete(channel):
  guild = channel.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.channel_delete:
        await clap(guild.id, entry.user.id, "Deleting Channels | Not Whitelisted")
        return
  except:
    return



@client.event
async def on_guild_channel_update(before, after):
  guild = before.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.channel_update:
        await clap(guild.id, entry.user.id, "Updating Channels | Not Whitelisted")
        return
  except:
    return



@client.event
async def on_guild_role_create(role):
  guild = role.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.role_create:
        await clap(guild.id, entry.user.id, "Creating Roles | Not Whitelisted")
        return
  except:
    return



@client.event
async def on_guild_role_delete(role):
  guild = role.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.role_delete:
        await clap(guild.id, entry.user.id, "Deleting Roles | Not Whitelisted")
        return
  except:
    return



@client.event
async def on_guild_role_update(before, after):
  guild = before.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.role_update:
        await clap(guild.id, entry.user.id, "Creating | Not Whitelisted")
        return
  except:
    return

    


@client.event
async def on_invite_delete(invite):
  guild = invite.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.invite_delete:
        await clap(guild.id, entry.user.id, "Revoking Invites | Not Whitelisted")
        return
  except:
    return




@client.event
async def on_webhooks_update(channel):
  guild = channel.guild
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  try:
    async for entry in guild.audit_logs(limit=1):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role or entry.user.id == client.user.id:
        return
      if entry.action == discord.AuditLogAction.webhook_create:
        await clap(guild.id, entry.user.id, "Creating hooks | Not Whitelisted")
        return
  except:
    return

#events end
client.run(tkn)
