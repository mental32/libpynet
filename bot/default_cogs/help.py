##
# -*- coding: utf-8 -*-
# help.py
##
import asyncio

import discord

from discord.ext import commands
from discord.errors import (HTTPException, Forbidden, NotFound, InvalidArgument)

class ihelp:
	''' builtin interactive help '''
	def __init__(self, cog, ctx):
		self.cog = cog
		self.ctx = ctx

		self.page = 0
		self.stopped = False
		self.commands = tuple(command for command in cog.bot.commands if not command.hidden)
		self.react_to = {
			'\U000025c0': self.go_back,
			'\U000025b6': self.go_forward,
			'\U0000274c': self.stop,
		}

	@property
	def embed(self):
		em = discord.Embed(title='help', colour=0xFFFFFF)
		em.set_footer(text=_page, icon_url=self.ctx.author.avatar_url)

		return em

	def is_author(r, user):
		return user == self.ctx.author

	async def stop(self):
		self.stopped = True
		await self.message.delete()

	async def go_back(self):
		if self.page-1 <= 0:
			self.page = 0
		else:
			self.page += 1

		await self.message.edit(embed=self.embed)

	async def go_forward(self):
		if self.page+1 == len(self.commands):
			self.page = 0
		else:
			self.page += 1

		await self.message.edit(embed=self.embed)

	async def run(self):
		self.message = await self.ctx.send(embed=self.embed)
		for emoji in self.react_to:
			await self.message.add_reaction(emoji)

		try:

			while not self.stopped:
				reaction, user = self.cog.bot.wait_for('reaction_add', check=self.is_author)

				if str(reaction) in self.react_to:
					await self.react_to[str(reaction)]()

					with ignored(HTTPException, Forbidden, NotFound, InvalidArgument):
						await self.message.remove_reaction(reaction.emoji, user)

				await asyncio.sleep(0.5)

		except Exception as error:
			return error


class help:
	''' help cog for the bot '''
	def __init__(self, bot):
		self.bot = bot

	def format_help(self, command):
		''' returns a discord.Embed object of a command '''
		kwargs = {
			'title': command.name,
			'description': utils.markdown(command.help),
			'timestamp': utils.now(),
			'colour': 0xFFFFFF
		}

		em = discord.Embed(**kwargs)
		return em

	@commands.command()
	async def help(self, ctx, *, command=None):
		'''help [command]
		returns the help docstring of a command'''
		if command is not None:
			return await ctx.send(self.format_help(self.bot.get_command(command)))
		else:
			return await (ihelp(self, ctx).run())

def setup(_bot):
	global bot
	bot = _bot
	bot.add_cog(help(bot))
