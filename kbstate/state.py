from kbstate import Event, Events

class State:
    def __init__(self):
        self.events = {}
        eventslist = [
            Events.set_config
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

    def next(self, eventName, **args):
        if eventName in self.events:
            self.events[eventName].fire(**args)
        else:
            print('no event found to fire')