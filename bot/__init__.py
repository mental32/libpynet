##
# -*- coding: utf-8 -*-
# __init__.py
# Author: Mental
# Start: 15/12/2017@13:55 GMT+0
##
import os
import time
import logging

import .utils
from .exceptions import LibraryError

from discord.ext import commands
##

__version__ = '3.3'
__author__ = 'mental'
__start__ = time.time()

def time_since_init():
	return time.time()-__start__

def run(settings, cogs='cogs', load_default=True):
	# make sure we can load cogs
	assert os.path.exists(cogs), 'cog directory \'{0}\'was not found'.format(cogs)
	assert os.path.isdir(cogs), 'cog directory\'{0}\' is not a directory'.format(cogs)

	# Setup the logger
	logger = logging.getLogger('discord')
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
	handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
	logger.addHandler(handler)

	# initalize base variables
	settings = utils.json_wrapper(fp=settings)
	bot = commands.Bot(command_prefix=settings.prefix)

	# make sure a token is provided
	assert settings.token, 'No token found in {0}'.format(settings)

	if settings.remove_default_help:
		# remove the default help supplied.
		# we will be using our own
		bot.remove_command('help')

	# bind the settings to the bot
	setattr(bot, 'settings', settings)

	for critical_ext in (file[:-3] for file in os.listdir('bot/critical') if file.endswith('.py')):
		try:
			bot.load_extension('bot.critical.'+critical_ext)
		except Exception as e:
			raise LibraryError('\'bot/critical/\' is malformed, please make sure to update the library')

	cogs = cogs.replace('/', '.')
	defaults = [file[:-3] for file in os.listdir('.default_cogs/') if file.endswith('.py')]
	for extension in (file[:-3] for file in os.listdir(cogs) if file.endswith('.py')):
		try:
			if extension in defaults:
				defaults.remove(extension)

			bot.load_extension(cogs+'.'+extension)
		except Exception as e:
			print(e)
	else:
		# load the remaining default cogs if at all.
		if load_default:
			try:
				for default_ext in defaults:
					bot.load_extension('bot.default_cogs.'+default_ext)
			except Exception as e:
				raise LibraryError('Got {0} exception while attempting to load a deafult cog'.format(e))

		bot.run(settings.token)
