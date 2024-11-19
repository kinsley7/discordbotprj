import discord
from discord.ext import commands


class Censor(commands.Cog):
    def __init__(self, bot : commands.Bot):
     self.bot = bot
     self.profanity = ['fuck','shit', 'ass', 'damn', 'fucking', 'shitting', 'hell', 'bastard']

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"censor is ready")
 
    @commands.Cog.listener()
    async def on_message(self, message):
       if any(word in message.content.lower() for word in self.profanity):
          await message.delete()
          await message.channel.send(f"This was deleted due to profanity.")
          


   
async def setup(bot) -> None:
    await bot.add_cog(Censor(bot))

