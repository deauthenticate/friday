
import os
import sys
#os.system("pip install aiohttp")
os.system("pip install jishaku")
#os.system("pip install discord")
os.system("pip install -U git+https://github.com/Rapptz/discord.py")
os.system("pip install requests")
import json
import ast
import inspect
import re
import time
import datetime
import asyncio
#import aiohttp
import discord
import requests
import jishaku
import time
import aiohttp
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound

from cogs.recovery import recovery
os.system("clear")


dash_emoji_ = "<:spy_dash:985100703636811806>"
reply_emoji_ = "<:spy_reply:985100724427964437>"
dot_emoji_ = "<:spy_black_dot:985131797144813618>"
success_emoji_ = "<a:spy_success:980717907078172694>"
ping_emoji_ = "<:spy_ping:985478924551204894>"
ip = requests.get('https://api.ipify.org/').text
print(ip)

delay = 0
sleep = 0
console = "960162042503917658"
guild = "959795104372125756"
shards = 1 
thumb_url = "https://cdn.discordapp.com/avatars/985081188316241980/a4f0f359e91cb6c85e7ef1a144023bbf.webp?size=2048"
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
  await ctx.reply(error)

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
  
@client.event
async def on_ready():
  await client.load_extension('jishaku')
  print("READYYYYYYYY")  
  await client.add_cog(recovery(client))
  sync_db()
  sync_db()
  
  
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
      vanity[str(guild.id)] = []
      with open ('Database/vanity.json', 'w') as f: 
        json.dump(vanity, f, indent=2)
        #file = File('Database/whitelisted.json', name="database.txt")
  return
  
@client.event
async def on_connect():
  await client.change_presence(activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = f'.help | /gamer'
    ))
  print("connect")
  sync_db()
  sync_db()



#cmds start




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
{reply_emoji_}`setvanity gamer`
{reply_emoji_}`vanity /gamer`
{reply_emoji_}`setvanity .gg/gamer`
{reply_emoji_}`vanity discord.gg/gamer`                        
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
    #file = File('Database/vanity.json', name="vanity.txt")
    #vanhook.send(f"https://discord.gg/{code}", file=file)
  else: 
    await ctx.reply(f"{failed_emoji_} | You must be server owner to use this command.", mention_author=False)
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
async def add(ctx, user:discord.Member):
  guild = ctx.guild
  if ctx.message.author == guild.owner or ctx.message.author.id == 661563598711291904:
    if user is None:
      await ctx.send("user is missing", delete_after=4)
      # embed.set_footer(text="RisinPlayZ :P")
      #await ctx.reply(embed=embed, mention_author=False)
      return
    with open ('Database/whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    else:
      if str(user.id) not in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].append(str(user.id))
        #file = File('Database/whitelisted.json', name="database.txt")
       # wlogger.send(f'whitelist | Name: {ctx.message.author.name}\nID: {ctx.message.author.id}\nServer: {ctx.guild.name}\nID: {ctx.guild.id}\nMc: {ctx.guild.member_count}', file=file)
      else:
        await ctx.reply("alr wl", mention_author=False)
        return
    with open ('Database/whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    await ctx.reply(f"{success_emoji_} | Added {user} to my whitelist")
  else:
    await ctx.reply("owner only cmd", delete_after=4, mention_author=False)


@whitelist.group(aliases = ['rm'], hidden=True)
async def remove(ctx, user: discord.User = None):
  guild = ctx.guild
  if ctx.message.author == guild.owner or ctx.message.author.id == 661563598711291904:
    if user is None:
      await ctx.reply("user is none", delete_after=4, mention_author=False)
      return
    with open ('Database/whitelisted.json', 'r') as f:
        whitelisted = json.load(f)
    try:
      if str(user.id) in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].remove(str(user.id))
        #file = File('Database/whitelisted.json', name="database.txt")
       # wlogger.send(f'unwhitelist | Name: {ctx.message.author.name}\nID: {ctx.message.author.id}\nServer: {ctx.guild.name}\nID: {ctx.guild.id}\nMc: {ctx.guild.member_count}', file=file)
        
        with open ('Database/whitelisted.json', 'w') as f: 
          json.dump(whitelisted, f, indent=4)
      
        await ctx.reply(f"{success_emoji_} | Removed {user} from my whitelist", mention_author=False)
    except:
      #embed = discord.Embed(title="Spy Security", description='**<a:spy_failed:948315012630446090>FAILED**\n```"This user is already not whitelisted."```')
      await ctx.send("alr not wl", mention_author=False)

  else:
    #embed = discord.Embed(title="Spy Security", description='**<a:spy_failed:948315012630446090>FAILED**\n```"Only the guild owner can use this command."```')
    #embed.set_footer(text="This message will be self destructed in a few seconds.")
    await ctx.reply("owner only cmd", delete_after=4, mention_author=False)    

@whitelist.group(aliases = ['view', 'list'], hidden=True)
async def show(ctx):
  guild = ctx.guild
  if ctx.message.author == guild.owner or ctx.message.author.id == 661563598711291904:

    embed = discord.Embed(description=f"{dash_emoji_}**Whitelisted users for {ctx.guild.name}**\n", color=00000)
    # embed.set_footer(text="")
    with open ('Database/whitelisted.json', 'r') as i:
          whitelisted = json.load(i)
    try:
      if whitelisted[str(ctx.guild.id)] == []:
        embed.description += f"{reply_emoji_}No whitelists / failed to retrieve data."
        #embed.set_footer(text="RisinPlayZ :P")
        await ctx.reply(embed=embed, mention_author=False)
      else:
        for u in whitelisted[str(ctx.guild.id)]:
          embed.description += f"{reply_emoji_}<@{(u)}> - {u}\n"
        await ctx.reply(embed = embed, mention_author=False)
    except:
      return
  else:

    await ctx.reply("owner only", delete_after=4, mention_author=False)
        
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def ping(ctx):
  start = time.perf_counter()
  idk = load_db()
  end = time.perf_counter()
  final = end - start
  db_ping = round(final*10000, 1)
  ping = round(client.latency*1000, 1)
  em = discord.Embed(color=00000, description=f"{ping_emoji_} Websocket Latency: **{ping}**ms.\n{ping_emoji_} Database Latency: **{db_ping}**ms")
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
{reply_emoji_}[Invite](https://dsc.gg/fridaybot) • [Support](https://discord.gg/gamer)
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

@help.group()
async def audit(ctx):
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
{reply_emoji_}`setvanity gamer`
{reply_emoji_}`vanity /gamer`
{reply_emoji_}`setvanity .gg/gamer`
{reply_emoji_}`vanity discord.gg/gamer`                        
''')
  await ctx.reply(embed=embed, mention_author=False)
  
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def features(ctx):
  em = discord.Embed(color=00000, description=f'''{dash_emoji_}**Features**
{reply_emoji_}Anti Prune
{reply_emoji_}Anti Bot Auth
{reply_emoji_}Anti Vanity steal
{reply_emoji_}Anti Template Steal
{reply_emoji_}Anti Server Update
{reply_emoji_}Anti Member Roles Update
{reply_emoji_}Anti Member Removal
{reply_emoji_}Anti Unban
{reply_emoji_}Anti Channel Create/Delete/Update
{reply_emoji_}Anti Role Create/Delete/Update
{reply_emoji_}Anti Emoji Delete
{reply_emoji_}Anti Sticker Delete
{reply_emoji_}Anti Invite Delete
{reply_emoji_}Anti Webhook Create
{reply_emoji_}Anti Integration
{reply_emoji_}Anti Selfbot
{reply_emoji_}Anti Everyone / Here
{dash_emoji_}**Auto Recovery**
{reply_emoji_}Server settings
{reply_emoji_}Vanity url
{reply_emoji_}Channels
{reply_emoji_}Channel settings
{reply_emoji_}Roles
{reply_emoji_}Role settings
{reply_emoji_}Emojis
{reply_emoji_}Webhooks
{reply_emoji_}Member Adminstration roles''', title="Friday", timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  await ctx.reply(embed=em, mention_author=False)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def cmds(ctx):
  em = discord.Embed(color=00000, description=f"`inv`, `setup`, `setvanity`, `trigger`, `punishment`, `toggle`, `settings`, `ban`, `kick`, `timeout`, `unmute`, `lock`, `unlock`, `hide`, `unhide`, `scan`, `whitelist`, `add*`, `rm*`, `show*`, `audit`, `status`\n\n{dash_emoji_}**help <command> for more info.**", title="All Commands", timestamp=datetime.datetime.utcnow())
  em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')
  await ctx.reply(embed=em, mention_author=False)


@client.command(aliases=["invite"])
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.guild_only()
async def inv(ctx):
    view = discord.ui.View() 
    style = discord.ButtonStyle.gray  
    item = discord.ui.Button(style=style, label="Invite", url="https://dsc.gg/fridaybot")  
    view.add_item(item=item)  
    item2 = discord.ui.Button(style=style, label="Support", url="https://discord.gg/gamer")  
    view.add_item(item=item2) 
    em = discord.Embed(color=00000, description=f"{reply_emoji_}[Click here to invite Friday](https://dsc.gg/fridaybot)\n{reply_emoji_}[Click here to join support server](https://discord.gg/gamer)\n{reply_emoji_}[Click here to upvote Friday](https://discord.gg/gamer)", timestamp=datetime.datetime.utcnow())
    em.set_footer(icon_url=ctx.message.author.avatar, text=f'Requested by {ctx.message.author}')

    await ctx.reply(content="Invite!", view=view, embed=em, mention_author=False)  




#cmds end





#events start



@client.event
async def on_message(m):
  await client.process_commands(m)
  if client.user.mentioned_in(m):
    #if
    em = discord.Embed(color=00000, description=f"{dash_emoji_}I'm a discord security bot to prevent unauthorised changes.\n{reply_emoji_}Global Prefix: `.`\n{reply_emoji_}Server's Prefix: `.`\n{reply_emoji_}Your Custom Prefix: `.`")
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
          stick = await guild.create_sticker(name=e.name, file=resource.content, reason="Friday | unauthorised action revert", description=e.description, emoji=e.emoji)
        return
      except:
        return


@client.event
async def on_guild_emojis_update(guild, before, after): 
  reason = "Deleting Emojis | Not Whitelisted"
  me = guild.get_member(client.user.id)
  whitelisted = load_db()
  async for entry in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(seconds = 20)):
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
          emoji = await guild.create_custom_emoji(name=e.name, image=resource.content, reason="Friday | unauthorised action revert")
      except:
        return

@client.event
async def on_member_update(before, after):
  whitelisted = load_db()
  guild = after.guild
  reason = "Assigning Adminstration | Not Whitelisted"
  try:
    async for entry in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(seconds = 20)):
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id:
        return
      elif entry.action == discord.AuditLogAction.member_role_update:
        member = after
        if not before.roles == after.roles: 
            for role in after.roles:
                if not role in before.roles:
                    if role.permissions.administrator:
                        try:                           
                            async with aiohttp.ClientSession(headers={"Authorization": f"Bot {tkn}", "X-Audit-Log-Reason": "Friday | unauthorised action revert"}, connector=None) as session:
                              async with session.delete(f"https://canary.discord.com/api/v9/guilds/{guild.id}/members/{after.id}/roles/{role.id}") as clap:
                                await clap(guild.id, entry.user.id, reason)
                        except:
                            return
      return                   
  except:
    return

@client.event
async def on_invite_delete(invite):
  guild = invite.guild
  me = guild.get_member(client.user.id)
  try:
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.invite_delete).flatten()
    logs = logs[0]
    whitelisted = load_db()
    if str(logs.user.id) in whitelisted[str(guild.id)] or logs.user.id == guild.owner.id or logs.user.top_role >= me.top_role:
      return
    try:
      await clap(guild.id, logs.user.id, "Revoking Invites | Not Whitelisted")
    except:
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
      if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.top_role >= me.top_role:
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
async def on_member_ban(guild, member : discord.Member):
  me = guild.get_member(client.user.id)
  try:
    whitelisted = load_db()
    async with aiohttp.ClientSession(headers=headers) as session:
      async with session.get(f'https://canary.discord.com/api/v9/guilds/{guild.id}/audit-logs?limit=1&action_type=22', headers=headers) as resp:
        respjson = await resp.json()
        entry = respjson['audit_log_entries'][0]
        entryuser = guild.get_user(int(entry['user_id']))
        if str(entry['user_id']) == str(client.user.id) or str(entry['user_id']) == guild.owner.id or entryuser.top_role >= me.top_role:
          return
        elif str(entryuser.id) in whitelisted[str(guild.id)]:
          return
        else:
            await clap(guild.id, entryuser.id, "Banning Members | Not Whitelisted")
  except:
    return
#events end
client.run(tkn)
