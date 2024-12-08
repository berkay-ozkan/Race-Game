from threading import Condition, RLock
from source.singleton import singleton


@singleton
class Monitor:
    """A generic monitor class, decorate
    sync methods with Monitor().sync """

    def __init__(self) -> None:
        self.mlocks = {}

    def sync(monitor_self, method):

        def w(self, *p, **kw):
            if self not in monitor_self.mlocks:
                monitor_self.mlocks[self] = RLock()
            with monitor_self.mlocks[self]:
                return method(self, *p, **kw)

        return w
