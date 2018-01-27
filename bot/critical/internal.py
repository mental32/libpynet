##
# -*- coding: utf-8 -*-
# internal.py
##
from ..utils.json_tools import expanded_dict
from ..utils import dataclasses
##

def wrap(bot):
	internal = {
		'home': dataclasses.Nexus(),
		'tasks': [],
		'recv': 0,
		'sent': 0,
	}
	return expanded_dict(internal)

def setup(_bot):
	global bot
	bot = _bot
	bot.internal = wrap(bot)
