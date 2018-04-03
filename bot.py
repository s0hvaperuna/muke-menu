import os

from discord.ext.commands import Bot
from discord import File


class GonaBot(Bot):
    async def on_ready(self):
        user = await self.get_user_info(176411695533522944)
        if user is not None:
            p = os.path.join(os.getcwd(), 'ruokalista.png')
            await user.send(file=File(p, 'ruokalista.png'))

        await self.logout()
