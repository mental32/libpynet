##
# -*- coding: utf-8 -*-
# events.py
##
from ..exceptions import NullDestinationError
##

@event(events)
async def on_connect():
	bot.internal.connected = time.time()

@event(events)
async def on_ready():
	bot.internal.home.prepare(bot, guild_id=bot.settings.home_id)

	taken = round(time.time()-bot.settings.tmp.connected, 2)
	embed = discord.Embed(title='Ready', description=markdown('Achieved READY state in {0}ms'.format(taken)), colour=0x36393E)

	with ignored(NullDestinationError):
		await bot.internal.home.log(embed=embed)

	await update_status()

	with ignored(AttributeError):
		# will expect an AttributeError if no internal_overides is provided
		for overide, value in bot.settings.internal_overides.items():
			setattr(bot.internal, overide, value)

	for task in bot.internal.tasks:
		bot.loop.create_task(task.func())

def setup(_bot):
	global bot
	bot = _bot
	for event in events:
		setattr(bot, event.name, event.func)
