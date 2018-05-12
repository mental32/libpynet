##
# -*- coding: utf-8 -*-
##

def ensure_presence(func):
    def decorate(*args, **kwargs):
        event_type = args[0]

        if event_type not in Package.events:
            Package.events[event_type] = []

        if event_type not in Package.dispatchers:
            Package.dispatchers[event_type] = []

        return func(*args, **kwargs)
    return decorate


class Package:
    bot = None
    settings = None
    settings_fp = 'settings.json'
    events = {Exception: []}
    dispatchers = {Exception: []}

    @staticmethod
    @ensure_presence
    def on_event(event_type):
        '''decorator for internal event dispatch'''
        def decorate(func):
            Package.dispatchers[event_type].append(func)
        return decorate

    @staticmethod
    @ensure_presence
    def push_event(event_type, data):
        Package.events[event_type].append(data)

        for dispatcher in Package.dispatchers.get(event_type, []):
            Package.bot.loop.create_task(dispatcher(data))
