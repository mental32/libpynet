##
# -*- coding: utf-8 -*-
##
from discord.ext import commands

from . import utils
from .package import Package

class Master:
    '''Master cog, for control over all the other cogs.'''
    def __init__(self):
        self.bot = Package.bot
        self.path = 'cogs'
        self.last_loaded = None

    def _load_extension(self, name):
        try:
            self.bot.load_extension('%s.%s' %(self.path, name))
            self.last_loaded = name
        except Exception as trace:
            self.bot.package.push_event(Exception, trace)
            raise

    def _unload_extension(self, name):
        try:
            self.bot.unload_extension('%s.%s' %(self.path, name))
        except Exception as trace:
            self.bot.package.push_event(Exception, trace)
            raise

    async def __local_check(self, ctx):
        return self.bot.is_owner(ctx.author)

    @commands.group(name='cog', hidden=True)
    async def cog(self, ctx):
        pass

    @cog.command(name='load', aliases=['l'])
    async def load_cog(self, ctx, name):
        self._load_extension(name)

    @cog.command(name='unload', aliases=['u'])
    async def unload_cog(self, ctx, name):
        self._unload_extension(name)

    @cog.command(name='reload', aliases=['r'])
    async def reload_cog(self, ctx, name):
        self._unload_extension(name)
        self._load_extension(name)

    @cog.command(name='setpath', aliases=['sp'])
    async def set_path(self, ctx, *, path):
        self.path = path

    @cog.command(name='list', aliases=['li'])
    async def list_cogs(self, ctx):
        ml = len(repr(max(self.bot.cogs, key=len)))
        pad = lambda s: s + (' ' * (ml - len(s)))

        string = '\n'.join('%s%s' %(pad(name), repr(cog)) for name, cog in self.bot.cogs.items())
        await ctx.send(utils.markdown(string, style='prolog'))
