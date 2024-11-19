import discord
import datetime
from discord.ext import commands

class new_members(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
			print("Bot is online")

	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = self.bot.get_channel(1162183364837646418) #welcome channel

		img_embed = discord.Embed(
			color=discord.Color.dark_green(),
		)
		img_embed.set_image(url="https://media.tenor.com/1JgZW3hOUgwAAAAC/vert-neptunia.gif")

		welcomemsg_embed = discord.Embed(
			color=discord.Color.blurple(),
			title=f"👾⁺˚⋆₊ Welcome to Our Server ｡°✩₊˚🎮",
			description=f"ଘ(∩^o^)⊃━☆゜\n {member.mention} please read our <#1162398996178935888> and then choose your <#1162371536364240926> —̳͟͞ ⭐"

		)
		welcomemsg_embed.set_author(name=member.name, icon_url=member.avatar.url)
		welcomemsg_embed.set_footer(text="and remember to have fun ✩°｡⋆⸜(˙꒳​˙ )")

		welcomemsg_embed.set_thumbnail(url="https://i.pinimg.com/564x/57/e9/b1/57e9b17d82b34abff93396f3573dd395.jpg")
		welcomemsg_embed.timestamp = datetime.datetime.utcnow() #fix time to show est

		embeds = [img_embed, welcomemsg_embed]
		await channel.send(embeds=embeds)
		


	@commands.command()
	@commands.has_role('admin') #makes the command only usable by users with the admin role
	async def roles(self, ctx):
		
		await ctx.send("# Choose Roles Here:")

		role_platform_embed = discord.Embed(
			color=discord.Color.dark_green(),
			title="what platform do you use?",
			description=f" 🖥️ <@&1162370413964300310> \n💙 <@&1162370555937300583> \n💚 <@&1162370448101740666> \n❤️ <@&1162370622421205014> \n🕹️ <@&1162370654562164826>"
		)
		#role_platform_embed.set_thumbnail(url="https://media.tenor.com/oTfaKIrb2I8AAAAi/minecraft-discord.gif")

		platform_emojis = ["🖥️", "💙","💚","❤️","🕹️"]

		platform = await ctx.send(embed=role_platform_embed)

		for i in range(len(platform_emojis)):
			await platform.add_reaction(platform_emojis[i])
		
		#fav genre
		role_genre_embed = discord.Embed(
			color=discord.Color.fuchsia(),
			title ="what is your favorite genre?",
			description="⚔️<@&1162370725437513891> \n⛰️<@&1162370824037216356> \n🏪<@&1162370866617794610> \n🥊<@&1162370996343406623> \n🧩<@&1162371219589435392> \n👾<@&1162371051804704768>"
		)
		#role_genre_embed.set_thumbnail(url="https://static.wikia.nocookie.net/freddy-fazbears-pizzeria-simulator/images/e/e9/Tumblr_p0ugakbvzB1ush256o1_400.gif")
		genre_emojis = ["⚔️","⛰️","🏪","🥊","🧩","👾"]

		genre = await ctx.send(embed=role_genre_embed)
		
		for i in range(len(genre_emojis)):
			await genre.add_reaction(genre_emojis[i])

		# pings
		role_ping_embed = discord.Embed(
			color=discord.Color.dark_green(),
			title="get pinged for stuff!",
			description="📅<@&1162526323500134521> \n🎫<@&1162394113459617915>"
		)
		#role_ping_embed.set_thumbnail(url="https://64.media.tumblr.com/6cdd2c3b8a0289374cd78ec27bb4b252/07da9ffee3c27d6b-60/s540x810/cfd6c45496926eb9b6a2e85ad0bafb2ef962c651.gif")
		ping_emojis = ["📅","🎫"]

		ping = await ctx.send(embed=role_ping_embed)

		for i in range(len(ping_emojis)):
			await ping.add_reaction(ping_emojis[i])

	@commands.command()
	@commands.has_role('admin') #makes the command only usable by users with the admin role
	async def rules(self,ctx):

		rules_embed = discord.Embed(
			color=discord.Color.fuchsia(),
			title=" ⭐️ our rules:",
			description="⋆｡°✩ \n1. be nice :) \n2. dont be mean :( \n3. have fun \n⋆⭒˚｡⋆"
		)
		rules_embed.set_image(url="https://media.tenor.com/CN8gonXaNK8AAAAC/kirby.gif")

		
		await ctx.send(embed=rules_embed)
		message = await ctx.send("react with ✅ if you understand and gain access to the server")
		await message.add_reaction("✅")
		
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload): #give role based on reaction emoji
		
		rules_msgid = 1162439916987371670

		platform_msgid = 1162541012095344721
		genre_msgid = 1162541022937632860
		ping_msgid = 1162541033612136448

		guild = discord.utils.get(self.bot.guilds, name="csci 2910 server") #i wish i could do this but with an id but so far using a name is the only one that works

		#for the reaction message in #rules↴
		if payload.message_id == rules_msgid: 
			
			if str(payload.emoji) == "✅":
				role = discord.utils.get(guild.roles, name="rule reader")
				await payload.member.add_roles(role)

		#for #roles reactions↴
		if payload.message_id == platform_msgid:

			if str(payload.emoji) == "🖥️":
				role = discord.utils.get(guild.roles, name="pc")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "💙":
				role = discord.utils.get(guild.roles, name="playstation")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "💚":
				role = discord.utils.get(guild.roles, name="xbox")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "❤️":
				role = discord.utils.get(guild.roles, name="switch")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "🕹️":
				role = discord.utils.get(guild.roles, name="other platform")
				await payload.member.add_roles(role)

		if payload.message_id == genre_msgid:
			if str(payload.emoji) == "⚔️":
				role = discord.utils.get(guild.roles, name="fps")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "⛰️":
				role = discord.utils.get(guild.roles, name="platformer")
				await payload.member.add_roles(role)
			
			elif str(payload.emoji) == "🏪":
				role = discord.utils.get(guild.roles, name="rpg")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "🧩":
				role = discord.utils.get(guild.roles, name="puzzle")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "🥊":
				role = discord.utils.get(guild.roles, name="fighting")
				await payload.member.add_roles(role)

			elif str(payload.emoji) == "👾":
				role = discord.utils.get(guild.roles, name="other genre")
				await payload.member.add_roles(role)
	
		if payload.message_id == ping_msgid:
			if str(payload.emoji) =="📅":
				role = discord.utils.get(guild.roles, name="events")
				await payload.member.add_roles(role)

			elif str(payload.emoji) =="🎫":
				role = discord.utils.get(guild.roles, name="giveaways")
				await payload.member.add_roles(role)
	
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload): #removes role from user when reaction is taken away

		platform_msgid = 1162541012095344721
		genre_msgid = 1162541022937632860
		ping_msgid = 1162541033612136448

		guild = discord.utils.get(self.bot.guilds, name="csci 2910 server")
		member = guild.get_member(payload.user_id)

		if payload.message_id == platform_msgid:
			if str(payload.emoji) == "🖥️":
				role = discord.utils.get(guild.roles, name="pc")
				await member.remove_roles(role)

			elif str(payload.emoji) == "💙":
				role = discord.utils.get(guild.roles, name="playstation")
				await member.remove_roles(role)

			elif str(payload.emoji) == "💚":
				role = discord.utils.get(guild.roles, name="xbox")
				await member.remove_roles(role)

			elif str(payload.emoji) == "❤️":
				role = discord.utils.get(guild.roles, name="switch")
				await member.remove_roles(role)

			elif str(payload.emoji) == "🕹️":
				role = discord.utils.get(guild.roles, name="other platform")
				await member.remove_roles(role)

		if payload.message_id == genre_msgid:
			if str(payload.emoji) == "⚔️":
				role = discord.utils.get(guild.roles, name="fps")
				await member.remove_roles(role)

			elif str(payload.emoji) == "⛰️":
				role = discord.utils.get(guild.roles, name="platformer")
				await member.remove_roles(role)
			
			elif str(payload.emoji) == "🏪":
				role = discord.utils.get(guild.roles, name="rpg")
				await member.remove_roles(role)

			elif str(payload.emoji) == "🧩":
				role = discord.utils.get(guild.roles, name="puzzle")
				await member.remove_roles(role)

			elif str(payload.emoji) == "🥊":
				role = discord.utils.get(guild.roles, name="fighting")
				await member.remove_roles(role)

			elif str(payload.emoji) == "👾":
				role = discord.utils.get(guild.roles, name="other genre")
				await member.remove_roles(role)
	
		if payload.message_id == ping_msgid:
			if str(payload.emoji) =="📅":
				role = discord.utils.get(guild.roles, name="events")
				await member.remove_roles(role)

			elif str(payload.emoji) =="🎫":
				role = discord.utils.get(guild.roles, name="giveaways")
				await member.remove_roles(role)


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = self.bot.get_channel(1162183364837646418) #welcome channel

		img_embed = discord.Embed(
			color = discord.Color.dark_blue(),
			title = "goodbye _(:‚‹」∠)_",
			description= f"it's sad to see you go {member.display_name}"
		)
		img_embed.set_image(url="https://i.pinimg.com/originals/cb/d5/59/cbd559f75178f71ea4ea56f4a17010cd.gif")

		await channel.send(embed=img_embed)
		


async def setup(bot):
	await bot.add_cog(new_members(bot))
