import discord
from discord.ext import commands

class moderator(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message): #every cogs method has to have self as the first parameter
        if not message.author.bot:
            log_channel = self.bot.get_channel(1161066483850424350) # bots channel id
            await log_channel.send(f"Deleted message by {message.author} in #{message.channel}: {message.content}") #send this message to the log_channel which is the bots channel

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        print(f"An error occurred during {event}: {args[0]}")

    @commands.Cog.listener() # change events to Cog.listener so it can be used in the cogs folder
    async def on_ready(self):
        print(f"moderator class is ready")

async def setup(bot) -> None:
    await bot.add_cog(moderator(bot))