from components.cars import Ferrari
from components.cells import Rock, Fuel, Booster
from components.cells.roads import Turn90, Straight, Diagonal
from repo import Repo

r = Repo()
r.create(description="map1", cols=16, rows=16, cellsize=64, bgcolor='green')
r.create(description="map2", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map3", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map4", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map5", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map6", cols=4, rows=4, cellsize=64, bgcolor='green')

r.create(description="F571", rows=10, cols=10, cellsize=64, bg_color='green')
print(r.list())  # F571 will be listed with an id
ogr = r.attach(7, "onur")
tgr = r.attach(7, "tolga")  # these two are the same object
r.components.list()  # lists the available components
# assume all components call Repo.components.register(type, cls)
r.components.register('turn90', Turn90)
r.components.register("straight", Straight)
r.components.register("diagonal", Diagonal)
r.components.register('rock', Rock)
r.components.register("fuel", Fuel)
r.components.register("booster", Booster)
r.components.register("Ferrari", Ferrari)
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

temp = r.components.create('rock')
frr = r.components.create('Ferrari')
frr._DRIVER = "Alonso"

frr._speed = 100

temp.interact(frr)
ogr.place(frr, 0, 128)
frr._position = (0, 128)
frr._angle = 0
frr._speed = 64

ogr.draw()

cv = ogr.view(200, 200, 600, 600)
cd = cv.view(200, 200, 600, 600)
#cv.draw()

frr.start()
frr.tick()
frr.accelerate()

#frr.turn_counterclockwise()
frr.tick()
frr.turn_clockwise()
frr.accelerate()
frr.tick()
frr.stop()

ogr.draw()
frr.tick()

ogr.draw()
