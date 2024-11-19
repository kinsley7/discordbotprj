import json 
import requests
import aiohttp 
import asyncio 
import discord
import re
from discord.ext import commands
from discord import app_commands
from urllib.request import urlopen


""" if i had more time i would add: -xbox game pass games command, -epic games free game rotation cmd, and something for playstation and switch users"""

class apis(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    """!fortnite news => display more recent news
       !fortnite patchnotes => displays most recent patchnotes
       !fortnite dailyshop => displays daily shop"""
    @app_commands.command(name="fortnite-updates", description="see recent posts from epic games and whats in the shop!")
    @app_commands.choices(options=[
         app_commands.Choice(name="display recent news", value=0),
         app_commands.Choice(name="display today's daily shop", value=1)

    ])
    async def fortnite_updates(self, interaction:discord.Interaction, options:app_commands.Choice[int]):
        try:
            
            if options.value == 0:
                import time
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.wait import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.keys import Keys

                num = 0

                button = discord.ui.Button(label="Next", style=discord.ButtonStyle.green)
                button2= discord.ui.Button(label="Back")
                view = discord.ui.View()
                view.add_item(button)
                view.add_item(button2)
                await interaction.response.defer(thinking=True)
                web = webdriver.ChromeOptions()
                web.add_argument('--headless=new')
                web.add_argument('--no-sandbox')
                web.add_argument('--disable-dev-shm-usage')
                #web.add_argument('--disable-gpu')
                web.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0')

                browser = webdriver.Chrome(options=web)
                browser.set_page_load_timeout(30)
                url = "https://www.fortnite.com/news/"
                browser.get(url)

                browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)
                news = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.row")))
                news_items = []
                items = news.find_elements(By.TAG_NAME, 'a')
                #itemsTwo = items.find_elements(By.TAG_NAME, 'a')
                for item in items:
                    # Get the 'grid-image' div
                    grid_item = item.find_element(By.CLASS_NAME,'grid-item')
                    # Get the 'background-image' div within 'grid-image'
                    background_image = grid_item.find_element(By.CLASS_NAME,'background-image')
                    # Get the 'img' tag within 'background-image'
                    img = background_image.find_element(By.TAG_NAME, 'img')
                    # Get the src attribute of the img tag
                    img_src = img.get_attribute('src')

                    href = item.get_attribute('href')
                    title = item.get_attribute('title')

                    # Get the 'grid-content' div
                    grid_content = grid_item.find_element(By.CLASS_NAME, 'grid-content')
                    # Get the date and title within 'grid-content'
                    date = grid_content.find_element(By.TAG_NAME, 'H4').text
                    
                    

                    news_item = {
                        'img_src' : img_src,
                        'date' :  date,
                        'title' : title,
                        'href' : href
                    }

                    news_items.append(news_item)
                    #print(f'Image Src: {img_src}, Date: {date}, Title: {title}, href: {href}')
                
                browser.quit()
                
                await interaction.followup.send(embed=self.fortnite_news_tostring(news_items, num), view=view)
                    

                async def button_callback_next(interaction):
                    nonlocal num
                    if num > (len(news_items)) - 1:
                        num = 0
                    else:
                        num += 1

                    await interaction.response.edit_message(embed=self.fortnite_news_tostring(news_items, num))
                
                try:
                     async def button_callback_back(interaction):
                         nonlocal num
                         if num == 0:
                             num=(len(news_items)) - 1
                         else:
                             num -=1
                         await interaction.response.edit_message(embed=self.fortnite_news_tostring(news_items, num))
                except Exception as e:
                     print(e)


                button.callback=button_callback_next
                button2.callback=button_callback_back
                
            elif options.value==1:
                from datetime import date, timedelta, datetime
                
                today = datetime.utcnow().date()
                yesterday = today - timedelta(1)
                url = "https://fortnite-api.com/v2/cosmetics/br"
                req = requests.get(url)
                content=req.json()
                embed = discord.Embed(
                    title="₊⋆✰New Items in the Shop Today✰⋆₊"
                )
                embed.set_thumbnail(url="https://media.tenor.com/_LZYWQpVIigAAAAi/fortnite.gif")
                embed.set_footer(text="shop is updated daily at 00:00 UTC")
                if content and 'data' in content:
                    for item in content['data']:
                        if 'shopHistory' in item and item['shopHistory'] and 'name' in item:
                            if item['shopHistory'][-1][:-10] == str(today):
                                if len(item['shopHistory']) == 1 or item['shopHistory'][-2][:-10] != str(yesterday):
                                    embed.add_field(name=item['name'], value=f"⤷ {item['type']['displayValue']}, {item['rarity']['displayValue']}\n", inline=True)
                                #embed.set_thumbnail(url=item['images']['icon'])
         

                await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
    

    def fortnite_news_tostring(self, news, num):
        
        embed = discord.Embed(
              title=news[num]['title'],
              description="",
              url=news[num]['href']
         )
        embed.set_footer(text=news[num]['date'])
        embed.set_image(url=news[num]['img_src'])
        return(embed)

    """!steam (gamename) shows information about a game on steam"""
    @app_commands.command(name="steam-search", description="search for a game on steam and display information about it")
    @app_commands.describe(game_name="name of the game on steam. make sure to include punctuation.")
    async def steam_game_search(self, interaction:discord.Interaction, game_name:str):
        #https://wiki.teamfortress.com/wiki/User:RJackson/StorefrontAPI documentation
        games_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        async with aiohttp.ClientSession() as session:
            async with session.get(games_url) as resp:
                games = await resp.json()
                try:
                    try:
                        searched = [game for game in games['applist']['apps'] if game['name'].lower() == game_name.lower().strip()]
                    except:
                        await interaction.response.send_message(content="could not find game. make sure to include punctuation ", ephemeral=True)
                    if searched:
                        appid = searched[0]['appid']
                        app_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
                        async with aiohttp.ClientSession() as session2:
                            async with session2.get(app_url) as resp2:
                                info = await resp2.json()
                                    #background-raw, content_descriptors -> notes, name, short description, genres-> description, release_date -> date, price_overview, discount_percent, category -> description [0]
                                    #if 'is_free' = true then price = 'free'
                                if info:
                                    name = info[f'{appid}']['data']['name']

                                    if info[f'{appid}']['data']['is_free'] == True:
                                        price = 'Free'
                                    else:
                                        price = info[f'{appid}']['data']['price_overview']['final_formatted']

                                    publishers = info[f'{appid}']['data']['publishers']
                                    developers = info[f'{appid}']['data']['developers']
                                    description = info[f'{appid}']['data']['short_description']
                                    img = info[f'{appid}']['data']['header_image']

                                    genre_list = []
                                    for genre in info[f'{appid}']['data']['genres']:
                                        genre_list.append(genre['description'])

                                    category_list= []
                                    for category in info[f'{appid}']['data']['categories']:
                                        category_list.append(category['description'])

                                    release = info[f'{appid}']['data']['release_date']['date']

                                    if price == 'Free':
                                        discount = 'Game is free-to-play'
                                    elif info[f'{appid}']['data']['price_overview']['discount_percent'] == 0:
                                        discount = 'None'
                                    else:
                                        discount = info[f'{appid}']['data']['price_overview']['discount_percent']
                                    await interaction.response.send_message(embed=self.steam_search_tostring(name,appid,price,description,publishers,developers,img,genre_list,category_list,release,discount))
                                else:
                                    await interaction.response.send_message(content="Game does not have app details", ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(content="could not find game. make sure to include punctuation and check spelling ", ephemeral=True)
                    print(e)

    def steam_search_tostring(self, name, appid, price, description, publishers, developers, img, genres, category, release, discount):
        
        embed = discord.Embed(
            color=discord.Color.blue(),
            title=name,
            description= description,
            url=f"https://s.team/a/{appid}"
        )
        embed.add_field(name="Current Price", value=f"⤷ {price}", inline=True)

        if price != 'Free':
            embed.add_field(name="On sale?", value=f'⤷ Yes! {discount}% off.' if discount != 'None' else '⤷ No 😔')
        
        embed.add_field(name="Release Date", value=f"⤷ {release}")
        embed.add_field(name="Developed by", value=f"⤷ {(', '.join(developers))}", inline=True)
        embed.add_field(name="Published by", value=f"⤷ {(', '.join(publishers))}", inline=True)
        embed.add_field(name="Genres", value=f"⤷ {(', '.join(genres))}", inline=True)
        embed.add_field(name="Categories", value=f"⤷ {(', '.join(category[:2]))}", inline=True)

        embed.set_image(url=img)
        return embed


    @app_commands.command(name="steam-news", description="search for a game on steam and display the news & community posts for it")
    @app_commands.describe(game_name="name of the game on steam. make sure to include punctuation.")
    async def steam_game_news(self, interaction:discord.Interaction, game_name:str):         
         #huuge file with names and ids:
         #https://api.steampowered.com/ISteamApps/GetAppList/v2/
         games_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
         #await interaction.response.defer(thinking=True, ephemeral=True)
         button = discord.ui.Button(label="Next", style=discord.ButtonStyle.green)
         button2= discord.ui.Button(label="Back")
         view = discord.ui.View()
         view.add_item(button)
         view.add_item(button2)

         try:
            async with aiohttp.ClientSession() as session:
                async with session.get(games_url) as resp:
                    games = await resp.json()
                    searched = [game for game in games['applist']['apps'] if game['name'].lower() == game_name.lower().strip()]
                    if not searched:
                            await interaction.response.send_message(content="could not find game. make sure to include punctuation", ephemeral=True)
                        
                    num = 0
                    if searched != None:
                            appid = searched[0]['appid']
                            news_url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2?appid={appid}&count=5&feeds=steam_community_announcements,steam_community_blog"
                            print(news_url)
                            async with aiohttp.ClientSession() as session2:
                                async with session2.get(news_url) as resp2:
                                    news = await resp2.json()
                                    #print(news)
                                    if news != None:
                                        await interaction.response.send_message(embed=self.steam_news_tostring(news,num,searched[0]['name']), view=view)
                                    else:
                                        await interaction.response.send_message(content="there are no posts for this game currently", ephemeral=True)

                    else:
                            await interaction.response.send_message(content="could not find game. make sure to include punctuation and check spelling ", ephemeral=True)
                            print(e)

            async def button_callback_next(interaction):
                    nonlocal num
                    if num >= (len(news['appnews']['newsitems'])) - 1:
                        num = 0
                    else:
                        num += 1
                
                    await interaction.response.edit_message(embed=self.steam_news_tostring(news, num, searched[0]['name']))
                
                
            async def button_callback_back(interaction):
                nonlocal num
                if num == 0:
                     num = (len(news['appnews']['newsitems'])) - 1
                else:
                    num -=1

                await interaction.response.edit_message(embed=self.steam_news_tostring(news, num, searched[0]['name']))
            
            button.callback=button_callback_next
            button2.callback=button_callback_back

         except Exception as e:
             await interaction.response.send_message(content="could not find game. make sure to include punctuation and check spelling ", ephemeral=True)
             print(e)

    def steam_news_tostring(self, news, num, name):
        from datetime import datetime
        date = news['appnews']['newsitems'][num]['date']
        lines = news['appnews']['newsitems'][num]['contents'].split('\n')
        lines = lines[1:]
        first_8_lines = lines[:8]
        s = '\n'.join(first_8_lines)
        s = re.sub(r'\[.*?\]', '', s)
        #s = s.replace('\n', ' ')
        embed = discord.Embed(
            title=news['appnews']['newsitems'][num]['title'],
            description=f"{s}\nClick link to continue reading...",
            url=news['appnews']['newsitems'][num]['url']
        )
        embed.set_author(name=f"{name} {news['appnews']['newsitems'][num]['feedlabel']}")
        embed.set_footer(text=f"{datetime.utcfromtimestamp(float(date))} UTC")
        #embed.set_image(url=news['appnews']['newsitems'][num]['url'])
        return embed
        


    @app_commands.command(name="minecraft-updates", description="see recent posts from mojang!")
    @app_commands.choices(options= [
         app_commands.Choice(name="display news", value=0),
         app_commands.Choice(name="display Java Edition patch notes", value=1),
         #app_commands.Choice(name="search for a player (requires a name)", value=2)
         ])
    async def minecraft_updates(self, interaction:discord.Interaction, options:app_commands.Choice[int]):
            """displays minecraft updates using the mojang json files"""
            #i used bing ai and these links : https://www.reddit.com/r/learnpython/comments/i4xd79/comment/g0mzzs0/ , https://realpython.com/python-dicts/ to help me with using api in python
            try:
                if options.value == 0 or options.value == 1:
                        num = 0
                        button = discord.ui.Button(label="Next", style=discord.ButtonStyle.green)
                        button2= discord.ui.Button(label="Back")
                        view = discord.ui.View()
                        view.add_item(button)
                        view.add_item(button2)


                        minecraft_urls = ["https://launchercontent.mojang.com/news.json","https://launchercontent.mojang.com/javaPatchNotes.json"]
                        tostring_functions = [self.news_tostring, self.javaupdates_tostring]
                        url = minecraft_urls[options.value]
                        tostring = tostring_functions[options.value]
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as resp:
                                data = await resp.json()
                                news = data["entries"][num]
                                if options.value == 0:
                                    await interaction.response.send_message(content=f"Here is the recent Minecraft news:",embed=tostring(news), view=view)
                                else:
                                    await interaction.response.send_message(content=f"Here is the recent Minecraft Java Edition patch notes:",embed=tostring(news), view=view)

                        async def button_callback_next(interaction):
                            nonlocal num

                            if num >= len(data['entries']) - 1:
                                num = 0
                            else:
                                num += 1
                        
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as resp:
                                    data = await resp.json()
                                    news=data['entries'][num]
                                    await interaction.response.edit_message(embed=tostring(news))
                        
                        async def button_callback_back(interaction):
                            nonlocal num
                            
                            if num == 0 :
                                num = len(data['entries']) - 1
                            else:
                                num -= 1
                        
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as resp:
                                    data = await resp.json()
                                    news=data['entries'][num]
                                    await interaction.response.edit_message(embed=tostring(news))
                            

                        button.callback=button_callback_next
                        button2.callback=button_callback_back
                
            except Exception as e:
                 print(e)
        

    def news_tostring(self, news):
        embed = discord.Embed(
             title= news["title"],
             description= news["text"],
             url= news["readMoreLink"]
            )
        embed.set_footer(text=news["date"])
        embed.set_author(name=news["category"])
        embed.set_image(url="https://launchercontent.mojang.com" + news["playPageImage"]["url"])
        return embed
               
            
    def javaupdates_tostring(self, news):
        link = (((news['title']).lower()).replace(' ','-'))
        embed = discord.Embed(
                title= news["title"],
                description= "",
                url=f"https://www.minecraft.net/en-us/article/{link}"
                
                )
        embed.set_footer(text=f"Version: {news['version']}")
        embed.set_author(name=f"Minecraft Java Edition {news['type']}")
        embed.set_image(url="https://launchercontent.mojang.com" + news["image"]["url"])
        
        print(embed.url) 
        return embed
    
    @commands.Cog.listener()
    async def on_ready(self):
         print("apis is online")
              
    
            

async def setup(bot) -> None:
	guildid = 1158823336177061978
	await bot.add_cog(apis(bot), guilds=[discord.Object(id=guildid)])
