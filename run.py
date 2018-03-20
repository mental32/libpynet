##
# -*- coding: utf-8 -*-
##
import pynet

try:
    pynet.bot.register_cogs('cogs/')
    pynet.bot.run()
except Exception as e:
    print('Caught root level exception: %s' %(e))
finally:
    print('Ran for %s seconds' %(round(pynet.bot.run_age(), 2)))
