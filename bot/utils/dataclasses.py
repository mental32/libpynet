##
# -*- coding: utf-8 -*-
##
import discord
import asyncio
##

class Nexus:
	def __init__(self):
		pass

	async def log(self, *args, **kwargs):
		await self.logging.send(*args, **kwargs)

	def prepare(self, bot):
		'''Called after the bots internal cache is ready'''
		self.bot = bot
		settings = self.bot.settings

		self.guild = discord.utils.get(self.bot.guilds, id=310670709548646403)
		self.channels = enhanced_dict({c.name: c for c in self.guild.channels})

		self.logging = self.channels.logging
		self.live = self.channels.live
