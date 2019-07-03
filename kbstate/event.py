class Event:
    def __init__(self, eventName):
        self.name = eventName
        self.subscribers = []

    def addSubscriber(self, subscriberFn):
        if callable(subscriberFn):
            self.subscribers.append(subscriberFn)
        else:
            print('subscriber not callable, not adding')


    def removeSubscriber(self, subscriberFn):
        if subscriberFn in self.subscribers:
            self.subscribers.remove(subscriberFn)
        else:
            print('no matching subscriber found to remove')

    def fire(self, data):
        pass