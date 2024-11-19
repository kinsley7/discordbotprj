import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener() 
    async def on_ready(self):
        print(f"games class is ready")

    @commands.command(name="rps", help="Play Rock, Paper, Scissors")
    async def rock_paper_scissors(self, ctx, user_choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)

        user_choice = user_choice.lower()

        if user_choice in choices:
            if user_choice == bot_choice:
                result = "It's a tie!"
            elif (
                (user_choice == "rock" and bot_choice == "scissors")
                or (user_choice == "paper" and bot_choice == "rock")
                or (user_choice == "scissors" and bot_choice == "paper")
            ):
                result = "You win!"
            else:
                result = "I win!"
        else:
            result = "Invalid choice. Please choose rock, paper, or scissors."

        await ctx.send(f"You chose {user_choice}, I chose {bot_choice}. {result}")

async def setup(bot) -> None:
    await bot.add_cog(Games(bot))

