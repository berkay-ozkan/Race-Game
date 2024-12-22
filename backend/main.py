from backend.source.objects.components.cells import Rock, Fuel, Booster
from backend.source.objects.components.cells.roads import Turn90, Straight, Diagonal
from backend.source.objects.components import Car
from backend.source.repo import Repo
from threading import Thread
from time import time, sleep

r = Repo()

r.create(description="map1", cols=16, rows=16, cellsize=64, bgcolor='green')
r.create(description="map2", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map3", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map4", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map5", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map6", cols=4, rows=4, cellsize=64, bgcolor='green')

id = r.create(description="F571",
              rows=10,
              cols=10,
              cellsize=64,
              bg_color='green')
print(r.list())  # F571 will be listed with an id
ogr = r.attach(id, "onur")
tgr = r.attach(id, "tolga")  # these two are the same object
cv = ogr.view(0, 0, 100, 100, 'berkay')
cd = cv.view(200, 200, 600, 600, 'berkay')
r.components.list()  # lists the available components
# assume all components call Repo.components.register(type, cls)
r.components.register('turn90', Turn90)
r.components.register('turn90', Turn90)
r.components.register("straight", Straight)
r.components.register("diagonal", Diagonal)
r.components.register('rock', Rock)
r.components.register("fuel", Fuel)
r.components.register("booster", Booster)
r.components.register("car", Car)
rt = r.components.create('turn90')
ogr[(1, 1)] = rt
rt.rotation = 0
for j in range(2, 8):
    ogr[(1, j)] = r.components.create('straight')
    ogr[(1, j)].rotation = 0
dt = r.components.create('turn90')
dt.rotation = 1
ogr[(1, 8)] = dt
for i in range(2, 8):
    ogr[(i, 1)] = r.components.create('straight')
    ogr[(i, 8)] = r.components.create('straight')
    ogr[(i, 1)].rotation = 1
    ogr[(i, 8)].rotation = 1
rt = r.components.create('turn90')
ogr[(8, 1)] = rt
rt.rotation = 3
for j in range(2, 8):
    ogr[(8, j)] = r.components.create('straight')
    ogr[(8, j)].rotation = 0
dt = r.components.create('turn90')
dt.rotation = 2
ogr[(8, 8)] = dt
ogr[(8, 3)] = r.components.create('booster')
ogr[(8, 9)] = r.components.create('rock')
ogr[(8, 9)] = r.components.create('rock')
ogr[(8, 9)] = r.components.create('rock')
ogr[(0, 8)] = r.components.create('rock')
ogr[(1, 0)] = r.components.create('rock')
ogr[(7, 1)] = r.components.create('fuel')

FERRARI_ATTRIBUTES = {
    "model": "Ferrari",
    # Data source: ChatGPT
    "acceleration_rate": 19,
    "fuel_consumption_rate": 0.06,
    "deceleration_rate": 26,
    "steer_rate": 0.25,
    "max_speed": 210,
    "max_fuel": 23
}

frr = r.components.create('car', **FERRARI_ATTRIBUTES)
fr = r.components.create('car', **FERRARI_ATTRIBUTES)
frr._DRIVER = "Alonso"
frr._speed = 63
fr._DRIVER = "Alo"
fr._speed = 62

ogr.place(frr._id, 0, 0, 'ots')
ogr.place(fr._id, 0, 0, 'vusal')
frr._angle = 0
fr._angle = 0
print(ogr.draw())

ogr.start()
sleep(20)
ogr.stop()

print(ogr._leaderboards)
