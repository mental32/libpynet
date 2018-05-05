##
# -*- coding: utf-8 -*-
##
class Package:
    bot = None
    settings = None
    settings_fp = 'settings.json'
    events = {Exception: []}
    dispatchers = {}

    @staticmethod
    def on_event(key):
        '''decorator for internal event dispatch'''
        def decorator(func):
            Package.dispatchers[key].append(func)

        if key not in Package.events:
            Package.events[key] = []

        if key not in Package.dispatchers:
            Package.dispatchers[key] = []

        return decorator

    @staticmethod
    def push_event(event_type, data):
        if event_type not in Package.events:
            Package.events[event_type] = []

        Package.events[event_type].append(data)

        for dispatcher in Package.dispatchers.get(event_type, []):
            Package.bot.loop.create_task(dispatcher(data))
