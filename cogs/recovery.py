import os
import json
import discord
import aiohttp
import requests
from discord.ext import commands

def load_db():
  with open('Database/whitelisted.json') as f:
    return json.load(f)



tkn = os.environ['noo']

class recovery(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {'Authorization': f'Bot {tkn}', 'X-Audit-Log-Reason': 'Friday | unauthorized action revert'}
        print("Loaded Cog: [Recovery]")

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
      guild = before
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.guild_update:
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:
            await after.edit(name=before.name, verification_level=before.verification_level, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, preferred_locale=before.preferred_locale, rules_channel=before.rules_channel, public_updates_channel=before.public_updates_channel, reason="Friday | unauthorized action revert") 
          except:
            return


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
      guild = channel.guild
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:
            await channel.delete(reason="Friday | unauthorized action revert") 
          except:
            return


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
      guild = channel.guild
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:    
            await channel.clone(reason="Friday | unauthorized action revert")
          except:
            return



    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
      guild = before.guild
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:    
            await after.edit(name=before.name, reason="Spy Security | Auto Reinstate", overwrites=before.overwrites)
          except:
            return



    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
      guild = role.guild
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:    
            await role.delete(reason="Friday | unauthorized action revert")
          except:
            return



    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
      guild = role.guild
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:    
            await guild.create_role(name=role.name, color=role.color, permissions=role.permissions, hoist=role.hoist, mentionable=role.mentionable, reason="Friday | unauthorized action revert")
          except:
            return




    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
      guild = role.guild
      role = before
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          try:    
            await after.edit(name=role.name, permissions=role.permissions, colour=role.colour, hoist=role.hoist, mentionable=role.mentionable, reason="Friday | unauthorized action revert")
          except:
            return




    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
      guild = channel.guild
      me = guild.get_member(self.client.user.id)
      async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create):
          whitelisted = load_db()
          if str(entry.user.id) in whitelisted[str(guild.id)] or entry.user.id == guild.owner.id or entry.user.id == self.client.user.id:
            return
          async with aiohttp.ClientSession(headers=headers, connector=None) as session:
            try:    
              k = await channel.webhooks()
              for idk in k:
                async with session.delete(f'https://canary.discord.com/api/v9/webhooks/{idk.id}') as h:
                  return h.status
              overwrite = channel.overwrites_for(channel.guild.default_role)
              overwrite.read_messages = False
              await channel.set_permissions(channel.guild.default_role, overwrite=overwrite, reason="channel hidden coz of hook creation, to prevent pings.")
            except:
              return
