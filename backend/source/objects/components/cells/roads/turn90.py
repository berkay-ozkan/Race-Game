from backend.source.objects.components.cells import Road


class Turn90(Road):
    _description = "A 90 degree turn"
    _representation = [
        "turn90-0.png", "turn90-1.png", "turn90-2.png", "turn90-3.png"
    ]

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None,
                 rotation=None) -> None:
        super().__init__(id=id,
                         type="turn90",
                         _MAP=_MAP,
                         row=row,
                         col=col,
                         rotation=rotation)
