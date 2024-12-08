from threading import Condition, RLock
from source.singleton import singleton
from source.monitor import Monitor


class ObserverInformation:

    def __init__(self, view_id: int, map_id: int,
                 view_bounds: tuple[tuple[float, float], tuple[float, float]]):
        self.view_id = view_id
        self.map_id = map_id
        self.view_bounds: tuple[tuple[float, float],
                                tuple[float, float]] = view_bounds


@singleton
class Observer:

    def __init__(self):
        super().__init__()
        self.observers = {}

    @Monitor().sync
    def register(self, username, observer_information: ObserverInformation):
        ''' A new condition is created per observer and it is
        notified when interest set of the observer changes'''
        condition = Condition(Monitor().mlocks[self])
        self.observers[username] = (observer_information, condition)
        return condition

    @Monitor().sync
    def unregister(self, username):
        if username in self.observers:
            del self.observers[username]

    @Monitor().sync
    def wait(self, username):
        if username in self.observers:
            self.observers[username][1].wait()
            return self.observers[username][0].view_id

    @Monitor().sync
    def create_notification(self, map_id: int, affected_bounds):
        for observer_information, condition in self.observers.values():
            if map_id == observer_information.map_id and Observer(
            )._rectangles_intersect(observer_information.view_bounds,
                                    affected_bounds):
                condition.notify()

    @staticmethod
    def _rectangles_intersect(
        rectangle1_corners: tuple[tuple[float, float], tuple[float, float]],
        rectangle2_corners: tuple[tuple[float, float], tuple[float, float]]
    ) -> bool:
        r1_top_left, r1_bottom_right = rectangle1_corners
        r1_top, r1_left = r1_top_left
        r1_bottom, r1_right = r1_bottom_right

        r2_top_left, r2_bottom_right = rectangle2_corners
        r2_top, r2_left = r2_top_left
        r2_bottom, r2_right = r2_bottom_right

        if r1_bottom < r2_top or r2_bottom < r1_top:
            return False
        if r1_right < r2_left or r2_right < r1_left:
            return False

        return True
