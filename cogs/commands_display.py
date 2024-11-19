import discord
from discord.ext import commands

class Display(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    @commands.Cog.listener() 
    async def on_ready(self):
        print(f"display is ready")

    @commands.command(name="display", help="Show Commands")
    async def list_commands(self, ctx):
        await ctx.send(f"/steam-news\n!rps (your choice)\n/giveaway\n/event\n")

async def setup(bot) -> None:
    await bot.add_cog(Display(bot))