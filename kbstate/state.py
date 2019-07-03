from kbstate import Event

class State:
    def __init__(self):
        self.events = {}

    def addEvent(self, eventName):
        newEvent = Event(eventName)
        self.events[eventName] = newEvent
        return newEvent

    def removeEvent(self, eventName):
            if eventName in self.events:
                self.events[eventName].removeAllSubscribers()
                del self.events[eventName]

    def next(self, eventName, **args):
        if eventName in self.events:
            self.events[eventName].fire(**args)
        else:
            print('no event found to fire')