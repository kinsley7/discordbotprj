import discord, asyncio
from discord.ext import commands
from discord import app_commands
import random
import pdb

class party_creator(commands.Cog):
	def __init__(self, bot : commands.Bot) :
		self.bot = bot
		
		
	@app_commands.command(name="party_creator", description="create a party and others can react to join!")
	@app_commands.describe(game="name of the game you want to create a party for", members = "number of players you want in the party! (yourself included)", info = "add addition info about your party!")
	async def party_creator(self, interaction: discord.Interaction, game : str, members : int, info:str=""):
		
		
		party_embed = discord.Embed(
				color= random.choice([discord.Color.dark_green(), discord.Color.fuchsia()]),
				title= f"is creating a {game} party with {members} members 🎮",
				description=f"### {info} \n˚ ༘ ೀ⋆｡˚˚\nmembers currently in the party: \n⤷<@{interaction.user.id}>"
			)
		party_embed.set_thumbnail(url="https://media.tenor.com/ml-Znu6s0q0AAAAC/anime-gaming.gif")
		party_embed.set_author(name=interaction.user.name,icon_url=interaction.user.avatar.url)
		party_embed.set_footer(text="react to this message with '🎉' to join!")
		
		await interaction.response.send_message(embed=party_embed)
		party_msg = await interaction.original_response()
		await party_msg.add_reaction("🎉")


	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.id != 1162147603828461783: #if the user id that reacted is not the bot... 
			if str(payload.emoji) == "🎉": #makes sure it is the right emoji
				channel = self.bot.get_channel(payload.channel_id)
				if channel is not None:
					message = await channel.fetch_message(payload.message_id) #grabs message id
					if message is not None and message.embeds: #if the message has an embed
							embed = message.embeds[0] #gets the first embed
							embed.description += f"\n⤷<@{payload.member.id}>" #add this to the description
							await message.edit(embed=embed)
							
						
	
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self,payload):
		if str(payload.emoji) == "🎉": #makes sure it is the right emoji
				channel = self.bot.get_channel(payload.channel_id)
				if channel is not None:
					message = await channel.fetch_message(payload.message_id) #grabs message id from the api

					if message is not None and message.embeds: #if the message has an embed

						embed = message.embeds[0] #get the first embed
						lines = embed.description.split('\n') # Split the description into lines
						lines.reverse()  # Reverse the list of lines
						user_mention = f"⤷<@{payload.user_id}>"
						lines.remove(user_mention)  # Remove the first occurrence of the user's name
						lines.reverse()# Reverse the list of lines back
						embed.description = '\n'.join(lines)# Update the description in the embed
						await message.edit(embed=embed)
						

	@commands.Cog.listener()
	async def on_ready(self):	
		print("partycreator is ready")



async def setup(bot) -> None:
	guildid = 1158823336177061978
	await bot.add_cog(party_creator(bot), guilds=[discord.Object(id=guildid)])