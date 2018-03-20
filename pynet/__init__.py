##
# -*- coding: utf-8 -*-
##
from . import (bot, utils)
from .package import Package

__author__ = 'mental'
__version__ = '4.0.0'

if Package.settings is None:
    Package.settings = utils.json_wrapper(Package.settings_fp)

Package.bot = bot.Bot(Package.settings.token)
