from repo import Repo
from components.roads import Turn90, Straight, Diagonal, Rock, Fuel, Booster
from components.car import Car
from components.cell import Cell

r = Repo()
r.create(description="map1", cols=16, rows=16, cellsize=64, bgcolor='green')
r.create(description="map2", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map3", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map4", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map5", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map6", cols=4, rows=4, cellsize=64, bgcolor='green')

r.create(description = "F571", rows = 10,cols =10, cellsize = 64,bg_color = 'green')
print(r.list()) # F571 will be listed with an id
ogr = r.attach(7, "onur")
tgr = r.attach(7, "tolga") # these two are the same object
r.components.list() # lists the available components
# assume all components call Repo.components.register(type, cls)
r.components.register('turn90', Turn90)
r.components.register("straight", Straight)
r.components.register("diagonal", Diagonal)
r.components.register('rock', Rock)
r.components.register("fuel", Fuel)
r.components.register("booster", Booster)
r.components.register("Ferrari", Car)
rt = r.components.create('turn90')

ogr[(1,1)] = rt
rt.rotation = 0
for j in range(2,8):
    ogr[(1,j)] = r.components.create('straight')
    ogr[(1,j)].rotation = 0
dt = r.components.create('turn90')
dt.rotation = 1
ogr[(1,8)] = dt
for i in range(2,8):
    ogr[(i,1)] = r.components.create('straight')
    ogr[(i,8)] = r.components.create('straight')
    ogr[(i,1)].rotation = 1
    ogr[(i,8)].rotation = 1
rt = r.components.create('turn90')
ogr[(8,1)] = rt
rt.rotation = 3
for j in range(2,8):
    ogr[(8,j)] = r.components.create('straight')
    ogr[(8,j)].rotation = 0
dt = r.components.create('turn90')
dt.rotation = 2
ogr[(8,8)] = dt
ogr[(8,3)] = r.components.create('booster')
ogr[(8,9)] = r.components.create('rock')
ogr[(8,9)] = r.components.create('rock')
ogr[(8,9)] = r.components.create('rock')
ogr[(0,8)] = r.components.create('rock')
ogr[(1,0)] = r.components.create('rock')
ogr[(7,1)] = r.components.create('fuel')

temp = r.components.create('rock')
frr = r.components.create('Ferrari')
frr._DRIVER = "Alonso"
print(frr._DRIVER)
frr._speed = 100 
frr._position = (1 , 1)
print(frr._speed)
print(frr._position, frr._MAX_SPEED, frr._MAX_FUEL)
temp.interact(frr, 0 ,0)
print(frr._speed)
print(ogr.draw())
cv = ogr.view(200,200,600,600)
print(cv.draw())
cv.remove(dt)
#frr.start()
#frr.tick()
#frr.accel()
#frr.left()
#frr.tick()
#frr.right()
#frr.accell()
#frr.tick()
#frr.stop()
print(cv.draw())

print(ogr.draw())