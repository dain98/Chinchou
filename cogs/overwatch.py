import discord
from .utils.dataIO import dataIO
from .utils.chat_formatting import escape_mass_mentions
from .utils import checks
from collections import defaultdict
from string import ascii_letters
from random import choice
import discord
import os
import re
import aiohttp
import asyncio
import logging
from discord.ext import commands
try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False
import aiohttp

class Overwatch:
    """Gives you information on your Overwatch account"""

    def __init__(self, bot):
        self.bot = bot
        self.header = {"User-Agent": "User_Agent"}
        self.api = None
        self.user = None

    @commands.command()
    async def ow(self, username, region):
        """Shows information on your Overwatch account. %ow [Battle tag]"""
        url = "https://ow-api.herokuapp.com/profile/pc/us/"
        self.user = username.replace("#", "-")
        if self.user == None:
            await self.bot.say("Please enter your Battle tag!")
            return
        async with aiohttp.ClientSession(headers=self.header) as session:
            fetch = await self.bot.say("Fetching data from Overwatch API...inputted Battle tag is " + username)
            async with session.get(url + self.user) as channel:
                self.api = await channel.json()
                await self.bot.delete_message(fetch)
                if 'username' in self.api:
                    if self.api['competitive']['rank'] == None:
                        await self.statsranked()
                    else:
                        await self.stats()
                else:
                    await self.bot.say("Your Battletag is wrong, try again! If problems persist, contact the owner through %contact.")

    async def stats(self):
        embed=discord.Embed(title="Level " + str(self.api['level']), description="SR " + str(self.api['competitive']['rank']))
        embed.set_author(name="Stats for " + self.api['username'], url='https://www.overbuff.com/players/pc/' + self.user, icon_url=self.api['portrait'])
        embed.set_thumbnail(url=self.api['competitive']['rank_img'])
        embed.add_field(name="Quickplay:", value="_ _", inline=True)
        embed.add_field(name="Games Won:", value=str(self.api['games']['quickplay']['won']), inline=True)
        embed.add_field(name="Competitive:", value="_ _", inline=True)
        embed.add_field(name="Games Played: ", value=str(self.api['games']['competitive']['played']), inline=True)
        embed.add_field(name="_ _", value="_ _", inline=True)
        embed.add_field(name="Game Won: ", value=str(self.api['games']['competitive']['won']), inline=True)
        embed.add_field(name="_ _", value="_ _", inline=True)
        embed.add_field(name="Games Lost:", value=str(self.api['games']['competitive']['lost']), inline=True)
        embed.add_field(name="_ _", value="_ _", inline=True)
        embed.add_field(name="Draws:", value=str(self.api['games']['competitive']['draw']), inline=True)
        await self.bot.say(embed=embed)

    async def statsranked(self):
        embed=discord.Embed(title="Level " + str(self.api['level']))
        embed.set_author(name="Stats for " + self.api['username'], url='https://www.overbuff.com/players/pc/' + self.user, icon_url=self.api['portrait'])
        embed.set_thumbnail(url="http://www.designsbybethann.com/pictures/Flowers/none%20flowers.jpg")
        embed.add_field(name="Quickplay:", value="_ _", inline=True)
        embed.add_field(name="Games Won:", value=str(self.api['games']['quickplay']['won']), inline=True)
        embed.add_field(name="Competitive:", value="_ _", inline=True)
        embed.add_field(name="Games Played: ", value=str(self.api['games']['competitive']['played']), inline=True)
        embed.add_field(name="_ _", value="_ _", inline=True)
        embed.add_field(name="Game Won: ", value=str(self.api['games']['competitive']['won']), inline=True)
        embed.add_field(name="_ _", value="_ _", inline=True)
        embed.add_field(name="Games Lost:", value=str(self.api['games']['competitive']['lost']), inline=True)
        embed.add_field(name="_ _", value="_ _", inline=True)
        embed.add_field(name="Draws:", value=str(self.api['games']['competitive']['draw']), inline=True)
        await self.bot.say(embed=embed)
def setup(bot):
    if soupAvailable:
        bot.add_cog(Overwatch(bot))
    else:
        raise RuntimeError("You need to run 'pip3 install beautifulsoup4'")
