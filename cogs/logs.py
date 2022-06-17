import os
import json
import discord
import aiohttp
from dhooks import Webhook, File
import datetime
from discord.ext import commands


tkn = os.environ['noo']

reply_emoji_ = "<:spy_reply:985100724427964437>"

#with open('av.jpg', 'rb') as f:
    #img = f.read() 
  
def get_hook(server:str):
  with open("Database/hooks.json") as f:
    resp = json.load(f)
  hookig = (resp[f'{server}'])
  return Webhook(hookig)
def load_db():
  with open('Database/whitelisted.json') as f:
    return json.load(f)
    
class logging(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {'Authorization': f'Bot {tkn}', 'X-Audit-Log-Reason': ''}
        print("Loaded Cog: [Logging]")

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = before
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.guild_update:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)   

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = member.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.member_prune or entry.action == discord.AuditLogAction.kick:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          if entry.action == discord.AuditLogAction.member_prune:
            hook.send("@everyone", embed=em)
            return
          hook.send(embed=em)   


    @commands.Cog.listener()
    async def on_member_join(self, member):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = member.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.bot_add:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          if entry.target.public_flags.verified_bot:
            verif = True
          else:
            verif = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Verified: {verif}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send("@everyone", embed=em)  

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.ban:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.unban:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)
          
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.emoji_delete:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)


    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.sticker_delete:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)



    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = channel.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.channel_create:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = channel.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.channel_delete:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = before.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.channel_update:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)



    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = role.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.role_create or entry.user.id == self.client.user.id:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)



    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = role.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.role_delete:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)



    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = before.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.role_update:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)


    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = invite.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.invite_delete:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)



    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = channel.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.webhook_create:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
          em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
          em.set_footer(text="Friday")
          hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
          hook.send(embed=em)



    @commands.Cog.listener()
    async def on_message(self, msg):
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = msg.guild
      if msg.mention_everyone:
        whitelisted = load_db()
        if str(msg.author.id) in whitelisted[str(guild.id)] or msg.author.id == guild.owner.id or msg.author.id == self.client.user.id:
          wl = True
        else:
          wl = False
        log = f'''{reply_emoji_} User: {msg.author} - \( `{msg.author.id}` \)
{reply_emoji_}Action: mention_everyone
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target Channel: {msg.channel.name}
{reply_emoji_}Message: {msg.content}
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
        em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
        em.set_footer(text="Friday")
        hook = get_hook(str(guild.id))
        #hook.modify(name=f'Friday | {guild.name}', avatar=img)
        hook.send(embed=em)




    @commands.Cog.listener()
    async def on_member_update(self, before, after):
      member = before
      unix = discord.utils.format_dt(datetime.datetime.utcnow(), 'R')
      guild = member.guild
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.member_role_update:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            wl = True
          else:
            wl = False
          if not before.roles == after.roles:
            for role in after.roles:
              if not role in before.roles:
                if role.permissions.administrator:
                  log = f'''{reply_emoji_} User: {entry.user} - \( `{entry.user.id}` \)
{reply_emoji_}Action: {entry.action}
{reply_emoji_}Happened: {unix}
{reply_emoji_}Target: {entry.target}
{reply_emoji_}Reason: {entry.reason}
{reply_emoji_}Role: {role}
{reply_emoji_}Role Perms: Administrator
{reply_emoji_} Whitelisted: {wl}'''.replace("AuditLogAction.", "")        
                  em = discord.Embed(color=00000, description=log, timestamp=datetime.datetime.utcnow())
                  em.set_footer(text="Friday")
                  hook = get_hook(str(guild.id))
          #hook.modify(name=f'Friday | {guild.name}', avatar=img)
                  hook.send(embed=em)
