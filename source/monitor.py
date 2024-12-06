from threading import Condition, RLock


class Monitor:
    """A generic monitor class, derive from this class and
	   call super().__init__()
	   then decorate sync methods with Monitor.sync """

    # Subclass class variables
    _attributes: dict[str, str] = {
        # Instance variables
        "mlock": "RLock",
        "condition": "Condition"
    }

    def __init__(self):
        self.mlock = RLock()

    @classmethod
    def sync(self, method):

        def w(self, *p, **kw):
            with self.mlock:
                return method(self, *p, **kw)

        return w

    def CV(self):
        """Create condition variables with this method to get
		   them share the monitor lock"""
        return Condition(self.mlock)
