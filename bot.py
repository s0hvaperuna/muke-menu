import os

from discord.ext.commands import Bot
from discord import File
import json


with open(os.path.join(os.getcwd(), 'config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)


class GonaBot(Bot):
    async def send2users(self, file):
        for user in config.get('users', []):
            try:
                user = await self.get_user_info(user)
                if user is not None:
                    await user.send(file=file)

            except discord.HTTPException as e:
                print('Failed to send to user %s\n' % user, e)
                
    async def send2channels(self, file):
        for channel in config.get('channels', []):
            try:
                channel = self.get_channel(channel)
                if channel is not None:
                    await channel.send(file=file)
            except discord.HTTPException as e:
                print('Failed to send to channel %s\n' % channel, e)

    async def on_ready(self):
        p = os.path.join(os.getcwd(), 'ruokalista.png')
        file = File(p, 'ruokalista.png')
        await self.send2users(file)
        await self.send2channels(file)
            
        await self.logout()
