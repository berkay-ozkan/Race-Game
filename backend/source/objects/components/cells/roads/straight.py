from backend.source.objects.components.cells import Road


class Straight(Road):
    _description = "A straight road"
    _representation = ["straight-0.png", "straight-1.png"]

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None,
                 rotation=None) -> None:
        super().__init__(id=id,
                         type="straight",
                         _MAP=_MAP,
                         row=row,
                         col=col,
                         rotation=rotation)
