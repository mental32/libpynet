##
# -*- coding: utf-8 -*-
##
import os
import time
import logging

import discord
from discord.ext import commands

from . import prebuilt
from .package import Package

_prebuilt_lookup = {
    'master': prebuilt.Master
}

is_module = lambda fp: os.path.isdir(fp) and '__init__.py' in os.listdir(fp)
endswith_py = lambda fn: fn.endswith('.py')

def remove_command(*args, **kwargs):
    '''create an alias to commands.Bot.remove_command'''
    Bot._instance.remove_command(*args, **kwargs)

def get_statistics():
    '''returns a dict of the bots statistics'''
    bot = Bot._instance
    return {
        'ws_latency': bot.latency,
        'user': bot.user,
        'users': len(bot.users),
        'guilds': len(bot.guilds),
        'emojis': len(bot.emojis),
        'private_channels': len(bot.private_channels),
        'voice_clients': len(bot.voice_clients),
    }

def estimate_cogs(fp, predicate=None):
    predicate = predicate or (lambda arg: True)

    modules = filter(lambda fn: is_module(fp+'/'+fn), os.listdir(fp))
    avaliabe_cogs = filter(endswith_py, os.listdir(fp))

    return len((*avaliabe_cogs,))

def register_cogs(fp, predicate=None):
    '''register all cogs from a directory'''
    count = 0
    predicate = predicate or (lambda arg: True)
    ext_fp = fp.replace('/', '.').replace('\\', '.')

    python_files = filter(endswith_py, os.listdir(fp))
    modules = filter(lambda fn: is_module(fp+'/'+fn), os.listdir(fp))

    for script in filter(predicate, list(python_files) + list(modules)):
        try:
            if script.endswith('.py'):
                script = script[:-3]

            Bot._instance.load_extension('%s%s' %(ext_fp, script))
            count += 1
        except Exception as trace:
            Package.push_event(Exception, trace)
    else:
        return count

def add_prebuilt(*names):
    for name in names:
        try:
            Package.bot.add_cog(_prebuilt_lookup[name]())

        except KeyError as e:
            raise KeyError('No prebuilt found with name: %s' %(name))

        except Exception as e:
            raise

def setup_logger(filename='discord.log'):
    '''Setup the logger for the package'''
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    logger.addHandler(handler)

def run():
    '''run the bot'''
    Bot._start = time.time()
    Bot._instance.run(Package.settings.token)

def run_age():
    '''Return how long the bot has been running.
    If the bot is not running it'll be how long since the Bot object has been instantiated.'''
    return (time.time() - Bot._instance._start)

### Bot #################################################################################
class Bot(commands.Bot):
    _start = None
    _instance = None # Allow global package access to the bot
    package = Package # Allow bot access to the package

    def __init__(self, *args, **kwargs):
        Bot._instance = self
        self._start = time.time()
        super(Bot, self).__init__(*args, **kwargs)

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)
