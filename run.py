##
# -*- coding: utf-8 -*-
##
import pynet

try:
    pynet.bot.add_prebuilt('master')

    cogs = pynet.bot.register_cogs('cogs/')
    print('[%s] Registered %s cogs' %(pynet.utils.human_time(), cogs))
    pynet.bot.run()
finally:
    print('Ran for %s seconds' %(round(pynet.bot.run_age(), 2)))
