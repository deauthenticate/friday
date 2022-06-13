import os
import json
import discord
import aiohttp
from discord.ext import commands


tkn = os.environ['noo']

class recovery(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {'Authorization': f'Bot {tkn}', 'X-Audit-Log-Reason': ''}
        print("Cog Loaded: Vanity Recovery")

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
      guild = before
      with open("Database/vanity.json") as f:
        resp = json.load(f)
      vanityig = (resp[f'{guild.id}'])
      
