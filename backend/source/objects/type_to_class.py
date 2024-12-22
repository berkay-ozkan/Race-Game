from backend.source.objects.components.car import Car
from backend.source.objects.components.cells.booster import Booster
from backend.source.objects.components.cells.fuel import Fuel
from backend.source.objects.components.cells.roads.diagonal import Diagonal
from backend.source.objects.components.cells.roads.straight import Straight
from backend.source.objects.components.cells.roads.turn90 import Turn90
from backend.source.objects.components.cells.rock import Rock

type_to_class = {
    "car": Car,
    "booster": Booster,
    "fuel": Fuel,
    "rock": Rock,
    "diagonal": Diagonal,
    "straight": Straight,
    "turn90": Turn90
}
