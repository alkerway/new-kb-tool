from .eventnames import Events
from kbstate import Event
from kbutils import ConfigUtil

class State:
    def __init__(self):
        self.config = ConfigUtil()
        self.events = {}
        eventslist = [
            'set_config',
            'transaction_drop_event',
            'remove_category',
            'update_category_total',
            'update_category_title'
        ]
        for event in eventslist:
            self.addEvent(event)

    def addEvent(self, eventName):
        newEvent = Event(eventName)
        self.events[eventName] = newEvent
        return newEvent

    def removeEvent(self, eventName):
        if eventName in self.events:
            self.events[eventName].removeAllSubscribers()
            del self.events[eventName]

    def addSubscriber(self, eventName, subscriberFn):
        self.events[eventName].addSubscriber(subscriberFn)

    def removeSubscriber(self, eventName, subscriberFn):
        self.events[eventName].removeSubscriber(subscriberFn)

    def next(self, eventName, *args):
        if eventName in self.events:
            self.events[eventName].fire(*args)
        else:
            print('no event found to fire')

    def getConfig(self):
        return self.config.getConfig()

    def setConfig(self, cfg):
        self.config.setConfig(cfg)