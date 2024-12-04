from threading import Condition, RLock


class Observer:

    def __init__(self):
        self.mut = RLock()
        self.observers = {}

    def register(self, obj, vset):
        ''' A new condition is created per observer and it is
        notified when interest set of the observer changes'''
        with self.mut:
            cond = Condition(self.mut)
            self.observers[obj] = (vset, cond)
        return cond

    def unregister(self, obj):
        with self.mut:
            del self.observers[obj]

    def wait(self, obj):
        with self.mut:
            if obj in self.observers:
                self.observers[obj][1].wait()
