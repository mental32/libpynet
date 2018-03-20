##
# -*- coding: utf-8 -*-
##
class Package:
    bot = None
    settings = None
    settings_fp = 'settings.json'
    events = {}

    @staticmethod
    def push_event(event_type, data):
        if event_type not in Package.events:
            Package.events[event_type] = []
        Package.events[event_type].append(data)
