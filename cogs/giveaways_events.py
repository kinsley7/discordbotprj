import discord, asyncio, time, re
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import datetime
import random
import pdb

class giveaways_events(commands.Cog):
	"""giveaway and event commands (only certain roles can use)"""
	def __init__(self, bot : commands.Bot) :
		self.bot = bot
	
	
	#create giveaways
	@app_commands.command(name="giveaway", description="create a giveaway!")
	@app_commands.describe(reward="what is being given away",winners="how many winners there are", expires="when the giveaway expires.(s for seconds, m for minutes, h for hours. ex: 5h = 5 hours or 3h30m = 3.5h)", info="extra information about the giveaway",roles="if the giveaway is for specific roles, @ them here")
	@commands.has_any_role("admin")
	async def giveaway(self, interaction: discord.Interaction, reward: str, winners:int, expires:str, info:str="", roles:str=""):
		'''this commands creates giveaways'''
		allowed_mentions = discord.AllowedMentions(everyone= True)
		try:
			if expires.endswith('h'):
				num = float(expires[:-1]) 
				seconds = num * 3600
			elif expires.endswith('m'):
				num = float(expires[:-1]) 
				seconds = num * 60
			elif expires.endswith('s'):
				num = float(expires[:-1]) 
				seconds = num
			else:
				await interaction.response.send_message(content="time not properly formatted. please put h,m,or s at the end.",ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(content="time not properly formatted. please put h,m,or s at the end.",ephemeral=True)

		expiry_time = int(time.time()) + round(seconds) 

		if winners <= 0:
			await interaction.response.send_message(content="cannot start a giveaway with 0 winners",ephemeral=True)
		elif winners == 1:
			if roles != "":
				giveaway_embed = discord.Embed(
					color=discord.Color.blurple(),
					title="a giveaway has started!",
					description=f"{winners} member with the {roles} role(s) can win **{reward}**!\n{info}\nexpires <t:{expiry_time}:R>"
				)
				giveaway_embed.set_footer(text="react with '🎫' for a chance to win!")
				
				await interaction.response.send_message(content= "<@&1162394113459617915>" , embed=giveaway_embed, allowed_mentions=allowed_mentions)

				giveaway_msg = await interaction.original_response()
				await giveaway_msg.add_reaction("🎫")
			else:
				giveaway_embed = discord.Embed(
					color=discord.Color.blurple(),
					title="a giveaway has started!",
					description=f"{winners} member can win **{reward}**!\n{info}\nexpires <t:{expiry_time}:R>"
				)
				giveaway_embed.set_footer(text="react with '🎫' for a chance to win!")
				
				await interaction.response.send_message(content= "<@&1162394113459617915>" , embed=giveaway_embed, allowed_mentions=allowed_mentions)

				giveaway_msg = await interaction.original_response()
				await giveaway_msg.add_reaction("🎫")

			await giveaways_events.edit_message_once_expired(seconds, expiry_time, giveaway_msg, winners, reward)

		else:
			if roles != "":
				giveaway_embed = discord.Embed(
					color=discord.Color.blurple(),
					title="a giveaway has started!",
					description=f"{winners} members with the {roles} role(s) can win **{reward}**!\n{info}\nexpires <t:{expiry_time}:R>"
				)
				giveaway_embed.set_footer(text="react with '🎫' for a chance to win!")
				
				await interaction.response.send_message(content= "<@&1162394113459617915>" , embed=giveaway_embed, allowed_mentions=allowed_mentions)

				giveaway_msg = await interaction.original_response()
				await giveaway_msg.add_reaction("🎫")
			else:
				giveaway_embed = discord.Embed(
					color=discord.Color.blurple(),
					title="a giveaway has started!",
					description=f"{winners} members can win **{reward}**!\n{info}\nexpires <t:{expiry_time}:R>"
				)
				giveaway_embed.set_footer(text="react with '🎫' for a chance to win!")
				
				await interaction.response.send_message(content= "<@&1162394113459617915>" , embed=giveaway_embed, allowed_mentions=allowed_mentions)

				giveaway_msg = await interaction.original_response()
				await giveaway_msg.add_reaction("🎫")

			await giveaways_events.edit_message_once_expired(seconds, expiry_time, giveaway_msg, winners, reward)

	#for the giveaway reactions
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		
		if payload.member.id != 1162147603828461783: #if the user id that reacted is not the bot... 
			if str(payload.emoji) == "🎫":
				channel = self.bot.get_channel(payload.channel_id)
				if channel is not None:
					message = await channel.fetch_message(payload.message_id)
					if message is not None and message.embeds: # need to split the lines up and find if the message @s/mentions any roles in the 1st line of the description
						embed = message.embeds[0]
						lines = embed.description.split('\n')
						role_ids = []
						line = lines[0]
						role_ids.extend(int(role_id[3:-1]) for role_id in re.findall(r'<@&\d+>', line)) # the "r'<@&\d+>'" regular expression matches strings that start with ‘<@&’ followed by one or more digits (‘\d+’) and end with ‘>’.
						
						if len(role_ids) != 0:
							if not any(role.id in role_ids for role in payload.member.roles):
								await channel.send(content=f"{payload.member.mention} you do not have the correct role to enter the giveaway.", delete_after=120)
								await message.remove_reaction(payload.emoji, payload.member)
							else:
								pass
						else: 
							pass

	#this method changes the giveaway message when it expires and picks and displays the winners
	@staticmethod						
	async def edit_message_once_expired(delay, expired_time, message, num_winners, reward):
		winners = []
		await asyncio.sleep(delay)
		if num_winners == 1:
			expired_embed = discord.Embed(
				title="this giveaway has expired!",
				description= f"it expired <t:{expired_time}:R> \n{num_winners} winner won **{reward}**!"
			)
		else:
			expired_embed = discord.Embed(
				title="this giveaway has expired!",
				description= f"it expired <t:{expired_time}:R> \n{num_winners} winners won **{reward}**!"
			)
		await message.edit(embed=expired_embed)
		try:
			message = await message.channel.fetch_message(message.id)

			# Get the first reaction which is the '🎉' just incase there are other reactions added. we only want the giveaway reaction
			reaction = message.reactions[0]

			# Get the users who reacted
			users = [user async for user in reaction.users() if not user.bot]  # Exclude the bot

			# Select winners randomly 
			winners = random.sample(users, min(num_winners, len(users)))

			# Announce winners
			if len(winners) > 1:
				winner_mentions = ', '.join(winner.mention for winner in winners[:-1]) + ' & ' + winners[-1].mention
			elif len(winners) == 1:
				winner_mentions = winners[0].mention


			
			if len(winners) == 0:
				message_winner = ""
				winner_embed = discord.Embed(
					color= discord.Color.dark_blue(),
					title="nobody won 😔",
					description=f"no user entered the **{reward}** giveaway!"
				)
				winner_embed.set_image(url="https://media.tenor.com/6vexN7dl0FUAAAAC/anime-k-on.gif")

			elif len(winner_mentions) == 1:
				message_winner = f"wou win {winner_mentions}!"
				winner_embed = discord.Embed(
					color= discord.Color.dark_green(),
					title="⊹˚congratulations! ˚⊹",
					description=f"the winner of **{reward}** is {winner_mentions} 🥳"
				)
				winner_embed.set_footer(text=f"dm the giveaway creator to claim your reward!🎉")
				winner_embed.set_image(url="https://media.tenor.com/RxGETpJZvusAAAAC/luigi-you-win.gif")

			else:
				message_winner = f"you win {winner_mentions}!"
				winner_embed = discord.Embed(
					color= discord.Color.dark_green(),
					title="⊹˚congratulations! ˚⊹",
					description=f"the winners of **{reward}** are {winner_mentions} 🥳"
				)
				winner_embed.set_footer(text=f"dm the giveaway creator to claim your reward!🎉")
				winner_embed.set_image(url="https://media.tenor.com/RxGETpJZvusAAAAC/luigi-you-win.gif")

			await message.channel.send(content=message_winner, embed=winner_embed)
			await message.clear_reactions()
		except Exception as e:
			print(e) #for testing

	@app_commands.command(name="event", description="plan an event!")
	@app_commands.describe(date="the day it happens (mm/dd/yyyy)", time="the time it happens (include am/pm)", location="where it happens", description="event details")
	@commands.has_any_role("admin")
	async def event(self, interaction: discord.Interaction, date: str, time: str, location: str, description: str=""):
		try:
			event_datetime = datetime.datetime.strptime(f"{date} {time}", "%m/%d/%Y %I:%M %p")
		except Exception as e:
			await interaction.response.send_message("Invalid date or time format. Please use MM/DD/YYYY HH:MM AM/PM.")
			print(e)
			return
		
		unix_timestamp = int(event_datetime.timestamp())

		formatted_time = f"<t:{unix_timestamp}:f>"

		allowed_mentions = discord.AllowedMentions(everyone= True)

		embed = discord.Embed(title="An event has been planned!", description=f"**Location**\n{location}\n**Description**\n{description}")
		embed.add_field(name="Date and Time", value=formatted_time)

		await interaction.response.send_message(content="<@&1162526323500134521>", allowed_mentions=allowed_mentions, embed=embed)
		#event_message = f"**Event Planned!** \n\n**Date/Time\n**{event_datetime.strftime('%m/%d/%Y %I:%M %p')}\n**Location\n**{location}\n**Description\n**{description}"			

	@commands.Cog.listener()
	async def on_ready(self):
		print("giveawayevents is ready")


async def setup(bot) -> None:
	guildid = 1158823336177061978
	await bot.add_cog(giveaways_events(bot), guilds=[discord.Object(id=guildid)])