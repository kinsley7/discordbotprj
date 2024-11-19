import discord
import asyncio
import sys
import os
from discord.ext import commands


token = ""
bot = commands.Bot(command_prefix='!', intents = discord.Intents.all(), application_id = )

async def setup_hook(): #grabs the commands
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cogs.{filename[:-3]}')

async def on_ready(self):
	print(f'{self.user} has connected')


#removes all slash commands (use "!delete_commands")
@bot.command()
@commands.has_role('admin')
async def delete_commands(ctx):
	bot.tree.clear_commands(guild=None)
	await bot.tree.sync()
	await ctx.send('Commands deleted.')

# syncs slash commands (use everytime you add, delete or update the @app_commands lines by using "!sync". read more here: https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f)
@bot.command(name="sync")
@commands.has_role('admin')
async def sync(ctx):
    synced = await bot.tree.sync(guild= ctx.guild)
    await ctx.send(f"Synced {len(synced)} command(s).")

async def main():
	await setup_hook()
	await bot.start(token)


asyncio.run(main())
