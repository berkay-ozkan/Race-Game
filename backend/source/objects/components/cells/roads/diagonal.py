from backend.source.objects.components.cells import Road


class Diagonal(Road):
    _description = "A diagonal road"
    _representation = ["diagonal-0.png", "diagonal-1.png"]

    def __init__(self,
                 object_id=None,
                 type=None,
                 id=None,
                 _MAP=None,
                 row=None,
                 col=None,
                 rotation=None) -> None:
        super().__init__(id=id,
                         type="diagonal",
                         _MAP=_MAP,
                         row=row,
                         col=col,
                         rotation=rotation)
