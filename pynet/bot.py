##
# -*- coding: utf-8 -*-
##
import os
import time
import logging

import discord
from discord.ext import commands

from .package import Package

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
    endswith_py = lambda fn: fn.endswith('.py')

    python_files = filter(endswith_py, os.listdir(fp))
    avaliabe_cogs = filter(predicate, python_files)

    return len((*avaliabe_cogs,))

def register_cogs(fp, predicate=None):
    '''register all cogs from a directory'''
    ext_fp = fp.replace('/', '.').replace('\\', '.')
    for filename in os.listdir(fp):
        if filename.endswith('.py'):
            if predicate is not None and not predicate(filename):
                continue

            try:
                Bot._instance.load_extension('%s%s' %(ext_fp, filename[:-3]))
            except Exception as e:
                Bot._instance.package.push_event(Exception, e)
                print(filename, e)

def setup_logger(filename='discord.log'):
    '''Setup the logger for the package'''
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))

    logger.addHandler(handler)

def run():
    '''run then bot'''
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
