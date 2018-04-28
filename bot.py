import os

from discord.ext.commands import Bot
from discord import File


class GonaBot(Bot):
    async def on_ready(self):
        user = await self.get_user_info(176411695533522944)
        p = os.path.join(os.getcwd(), 'ruokalista.png')
        file = File(p, 'ruokalista.png')
        if user is not None:
            await user.send(file=file)
            
        channel = self.get_channel(425730888538783745)
        if channel is not None:
            await channel.send(file=file)
            
        await self.logout()
