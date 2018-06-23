from discord.ext import commands
from .utils.dataIO import dataIO
from string import ascii_letters
from .utils import checks
from .utils.chat_formatting import pagify, box
import os
import discord
import re
import aiohttp
import asyncio
import logging
import time
import sys
try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False

class League:
	"""A Cog for League of Legends Players!"""

	def __init__(self,bot):
		self.summoner = None
		self.region = None
		self.bot = bot
		self.file_path = "data/league/champions.json"
		self.file_path2 = "data/league/summspells.json"
		self.save = dataIO.load_json(self.file_path)
		self.save2 = dataIO.load_json(self.file_path2)
		self.header = {"User-Agent": "User_Agent"}
		self.key = ""
		self.game = []
		self.infoUpdate()

	@commands.command(pass_context=True, no_PM=True)
	async def recentgame(self, ctx, sname, region):
		"""Shows your most recent game"""
		async with aiohttp.ClientSession(headers=self.header) as session:
			fetch = await self.bot.say("Fetching most recent game...")
			if region == "NA":
				region = "NA1"
			if region == "EUW":
				region = "EUW1"
			if region == "EUNE":
				region = "EUN1"
			if region == "OCE":
				region = "OC1"

			res1 = await self.urlHandler("https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + sname + "?api_key=" + self.key)
			if res1 == None:
				return
			res2 = await self.urlHandler("https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(res1['accountId']) + "/recent?api_key=" + self.key)
			if res2 == None:
				return
			gameFound = False
			for var in list(range(20)):
				if res2['matches'][var]['queue'] == 420:
					gameFound = True
					res3 = await self.urlHandler("https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + str(res2['matches'][var]['gameId']) + "?api_key=" + self.key)
					break
			if not gameFound:
				await self.bot.delete_message(fetch)
				await self.bot.say("No ranked games found in the past 20 games.")
				return
			if res3 == None:
				return
			self.game = res3
			self.summoner = sname
			self.region = region
			await self.stats()
			await self.bot.delete_message(fetch)

	async def stats(self):
		if 'Fail' in self.game['teams'][0]['win']:
			self.game['teams'][0]['win'] = "Lose"
		if 'Fail' in self.game['teams'][1]['win']:
		    self.game['teams'][1]['win'] = "Lose"
		embed=discord.Embed(title="Most recent game for " + self.summoner, description=self.game['teams'][0]['win'], color=0x00ffff)
		embed.add_field(name="Blue Team", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][0]['championId'])]['name'] + "(" + self.game['participantIdentities'][0]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][0]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][0]['spell2Id'])]['name'], inline=True)
		result1 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][0]['player']['summonerId']) + "?api_key=" + self.key)
		if result1 == None:
		    return
		embed.add_field(name=result1[0]['tier'] + " " + result1[0]['rank'], value=str(self.game['participants'][0]['stats']['kills']) + "/" + str(self.game['participants'][0]['stats']['deaths']) + "/" + str(self.game['participants'][0]['stats']['assists']) + ", " + str(self.game['participants'][0]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][1]['championId'])]['name'] + "(" + self.game['participantIdentities'][1]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][1]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][1]['spell2Id'])]['name'], inline=True)
		result2 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][1]['player']['summonerId']) + "?api_key=" + self.key)
		if result2 == None:
		    return
		embed.add_field(name=result2[0]['tier'] + " " + result2[0]['rank'], value=str(self.game['participants'][1]['stats']['kills']) + "/" + str(self.game['participants'][1]['stats']['deaths']) + "/" + str(self.game['participants'][1]['stats']['assists']) + ", " + str(self.game['participants'][1]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][2]['championId'])]['name'] + "(" + self.game['participantIdentities'][2]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][2]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][2]['spell2Id'])]['name'], inline=True)
		result3 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][2]['player']['summonerId']) + "?api_key=" + self.key)
		if result3 == None:
		    return
		embed.add_field(name=result3[0]['tier'] + " " + result3[0]['rank'], value=str(self.game['participants'][2]['stats']['kills']) + "/" + str(self.game['participants'][2]['stats']['deaths']) + "/" + str(self.game['participants'][2]['stats']['assists']) + ", " + str(self.game['participants'][2]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][3]['championId'])]['name'] + "(" + self.game['participantIdentities'][3]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][3]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][3]['spell2Id'])]['name'], inline=True)
		result4 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][3]['player']['summonerId']) + "?api_key=" + self.key)
		if result4 == None:
		    return
		embed.add_field(name=result4[0]['tier'] + " " + result4[0]['rank'], value=str(self.game['participants'][3]['stats']['kills']) + "/" + str(self.game['participants'][3]['stats']['deaths']) + "/" + str(self.game['participants'][3]['stats']['assists']) + ", " + str(self.game['participants'][3]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][4]['championId'])]['name'] + "(" + self.game['participantIdentities'][4]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][4]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][4]['spell2Id'])]['name'], inline=True)
		result5 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][4]['player']['summonerId']) + "?api_key=" + self.key)
		if result5 == None:
		    return
		embed.add_field(name=result5[0]['tier'] + " " + result5[0]['rank'], value=str(self.game['participants'][4]['stats']['kills']) + "/" + str(self.game['participants'][4]['stats']['deaths']) + "/" + str(self.game['participants'][4]['stats']['assists']) + ", " + str(self.game['participants'][4]['stats']['goldEarned']) + " Gold", inline=True)
		embed.set_footer(text="Created Using Riot API," + time.asctime(time.localtime(time.time())))
		await self.bot.say(embed=embed)
		embed=discord.Embed(title="_ _", description=self.game['teams'][1]['win'], color=0xff0000)
		embed.add_field(name="Red Team", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][5]['championId'])]['name'] + "(" + self.game['participantIdentities'][5]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][5]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][5]['spell2Id'])]['name'], inline=True)
		result6 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][5]['player']['summonerId']) + "?api_key=" + self.key)
		if result6 == None:
			return
		embed.add_field(name=result6[0]['tier'] + " " + result6[0]['rank'], value=str(self.game['participants'][5]['stats']['kills']) + "/" + str(self.game['participants'][5]['stats']['deaths']) + "/" + str(self.game['participants'][5]['stats']['assists']) + ", " + str(self.game['participants'][5]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][6]['championId'])]['name'] + "(" + self.game['participantIdentities'][6]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][6]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][6]['spell2Id'])]['name'], inline=True)
		result7 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][6]['player']['summonerId']) + "?api_key=" + self.key)
		if result7 == None:
			return
		embed.add_field(name=result7[0]['tier'] + " " + result7[0]['rank'], value=str(self.game['participants'][6]['stats']['kills']) + "/" + str(self.game['participants'][6]['stats']['deaths']) + "/" + str(self.game['participants'][6]['stats']['assists']) + ", " + str(self.game['participants'][6]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][7]['championId'])]['name'] + "(" + self.game['participantIdentities'][7]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][7]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][7]['spell2Id'])]['name'], inline=True)
		result8 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][7]['player']['summonerId']) + "?api_key=" + self.key)
		if result8 == None:
			return
		embed.add_field(name=result8[0]['tier'] + " " + result8[0]['rank'], value=str(self.game['participants'][7]['stats']['kills']) + "/" + str(self.game['participants'][7]['stats']['deaths']) + "/" + str(self.game['participants'][7]['stats']['assists']) + ", " + str(self.game['participants'][7]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][8]['championId'])]['name'] + "(" + self.game['participantIdentities'][8]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][8]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][8]['spell2Id'])]['name'], inline=True)
		result9 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][8]['player']['summonerId']) + "?api_key=" + self.key)
		if result9 == None:
			return
		embed.add_field(name=result9[0]['tier'] + " " + result9[0]['rank'], value=str(self.game['participants'][8]['stats']['kills']) + "/" + str(self.game['participants'][8]['stats']['deaths']) + "/" + str(self.game['participants'][8]['stats']['assists']) + ", " + str(self.game['participants'][8]['stats']['goldEarned']) + " Gold", inline=True)
		embed.add_field(name="_ _", value="_ _", inline=False)
		embed.add_field(name=self.save['data'][str(self.game['participants'][9]['championId'])]['name'] + "(" + self.game['participantIdentities'][9]['player']['summonerName'] + ")", value=self.save2['data'][str(self.game['participants'][9]['spell1Id'])]['name'] + ", " + self.save2['data'][str(self.game['participants'][9]['spell2Id'])]['name'], inline=True)
		result10 = await self.urlHandler("https://" + self.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(self.game['participantIdentities'][9]['player']['summonerId']) + "?api_key=" + self.key)
		if result10 == None:
			return
		embed.add_field(name=result10[0]['tier'] + " " + result10[0]['rank'], value=str(self.game['participants'][9]['stats']['kills']) + "/" + str(self.game['participants'][9]['stats']['deaths']) + "/" + str(self.game['participants'][9]['stats']['assists']) + ", " + str(self.game['participants'][9]['stats']['goldEarned']) + " Gold", inline=True)
		embed.set_footer(text="Created Using Riot API," + time.asctime(time.localtime(time.time())))
		await self.bot.say(embed=embed)

	async def urlHandler(self, url):
	    async with aiohttp.ClientSession(headers=self.header) as session:
	        logging.warning('Using the API!')
	        async with session.get(url) as channel:
	            result = await channel.json()
	            if 'status' in result:
	                if result['status']['status_code'] == 403:
	                    await self.bot.say("Your API key is invalid or has expired. Please update your API key through %riotapi.")
	                else:
	                    await self.bot.say("```Error code " + result['status_code'] + ": " + result['message'] + "```")
	                await self.bot.delete_message(fetch)
	                return
	            return result

	async def infoUpdate(self):
	    CHECK_DELAY = 86400
	    async with aiohttp.ClientSession(headers=self.header) as session:
	        async with session.get("https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=true&api_key=" + self.key) as channel:
	            logging.warning('Using the API!')
	            result = await channel.json()
	            if 'status' in result:
	                if result['status']['status_code'] == 403:
	                    print("Your API key is invalid or has expired. Please update your API key through %riotapi.")
	                else:
	                    print("Error code " + result['status']['status_code'] + ": " + result['status']['message'])
	                return
	            self.save = result
	    async with aiohttp.ClientSession(headers=self.header) as session:
	        async with session.get("https://na1.api.riotgames.com/lol/static-data/v3/summoner-spells?locale=en_US&dataById=true&api_key=" + self.key) as channel:
	            logging.warning('Using the API!')
	            result = await channel.json()
	            if 'status' in result:
	                if result['status']['status_code'] == 403:
	                    print("Your API key is invalid or has expired. Please update your API key through %riotapi.")
	                else:
	                    print("Error code " + result['status']['status_code'] + ": " + result['status']['message'])
	                return
	            self.save2 = result
	    dataIO.save_json(self.file_path, self.save)
	    dataIO.save_json(self.file_path2, self.save2)
	    await asyncio.sleep(CHECK_DELAY)

def check_folders():
	if not os.path.exists("data/league"):
		print("Creating data/league folder...")
		os.makedirs("data/league")


def check_files():
	f = "data/league/champions.json"
	if not dataIO.is_valid_json(f):
		print("Creating empty champions.json...")
	dataIO.save_json(f, {})
	g = "data/league/summspells.json"
	if not dataIO.is_valid_json(g):
		print("Creating empty summspells.json...")
	dataIO.save_json(g, {})

def setup(bot):
	check_folders()
	check_files()
	n = League(bot)
	loop = asyncio.get_event_loop()
	loop.create_task(n.infoUpdate())
	bot.add_cog(n)
