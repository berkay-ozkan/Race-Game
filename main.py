from source.objects.components.cells import Rock, Fuel, Booster
from source.objects.components.cells.checkpoint import Checkpoint
from source.objects.components.cells.roads import Turn90, Straight, Diagonal
from source.objects.components import Car
from source.repo import Repo
from threading import Thread
import time

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
r.components.register('checkpoint', Checkpoint)
cp = r.components.create('checkpoint')
cp1 = r.components.create('checkpoint')
ogr[(1, 1)] = cp
ogr[(1, 2)] = cp1
cp._order = 0
cp1._order = 1
ogr._checkpoints[0] = cp
ogr._checkpoints[1] = cp1
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

temp = r.components.create('rock')
frr = r.components.create('car', **FERRARI_ATTRIBUTES)
frr._DRIVER = "Alonso"

frr._speed = 64

temp._interact(frr)
ogr.place(frr, 0, 0, "onur")

frr._angle = 0
frr._speed = 63
ogr.draw()

cv = ogr.view(200, 200, 600, 600)
cd = cv.view(200, 200, 600, 600)
#cv.draw()

frr.start()
frr.tick()
#ogr.draw()
#frr.accelerate()

#frr.turn_counterclockwise()
frr.tick()

#frr.turn_clockwise()
#frr.accelerate()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()
frr.tick()

frr.tick()
frr.tick()
ogr.draw()
ogr.place(frr, 0, 0, "onur")
frr.tick()
ogr.draw()
print(frr._next_checkpoint._order)
print(f'{frr._next_checkpoint._order} THIS IS ORDER OF FRR')
#print(frr._MAP.grid)
#r.list()
#print(r._objects)
'''
def wait_for_map(repo):
    repo.create_wait()


def wait_for_attach(repo):
    repo.attach_wait()

r.components.register("car", Car)
r.components.register('checkpoint', Checkpoint)
wait_map_thread = Thread(target=wait_for_map, args=(r,))
wait_attach_thread = Thread(target=wait_for_attach, args=(r,))
def create_map(description):
    print(f"Thread starting to create map: {description}")
    map_id = r.create(description = description, cols = 10, rows = 10, cell_size = 5, bg_color ="green")
    print(f"Map created: {description} with ID {map_id}")


def attach_user(map_id, user):
    print(f"Thread starting to attach user: {user} to map {map_id}")
    r.attach(map_id, user)
    print(f"User {user} attached to Map ID {map_id}")



wait_map_thread.start()
wait_attach_thread.start()

attach_thread1 = Thread(target=attach_user, args=(1, "User1"))
attach_thread2 = Thread(target=attach_user, args=(2, "User2"))
create_thread1 = Thread(target=create_map, args=("Map 1",))
create_thread2 = Thread(target=create_map, args=("Map 2",))
attach_thread1.start()
attach_thread2.start()

create_thread1.start()
create_thread2.start()





wait_map_thread.join()
wait_attach_thread.join()
attach_thread1.join()
attach_thread2.join()

create_thread1.join()
create_thread2.join()

print("Final maps in r:", r.list())
print("User1 attached maps:", [m.description for m in r.list_attached("User1")])
print("User2 attached maps:", [m.description for m in r.list_attached("User2")])

m = r.create(description="map6", cols=4, rows=4, cellsize=64, bgcolor='green')
frr = r.components.create('car', **FERRARI_ATTRIBUTES)
cp = r.components.create('checkpoint')
def edit_map():
    time.sleep(1)
    print("car place")
    mp.place(frr, 0, 0, "vusal")

    
    
    mp.draw()
mp = r.attach(m, 'vusal')
edit_thread = Thread(target=edit_map)
edit_thread.start()
edit_thread.join()
print(cp._order)
mp.place(cp, 0, 0, "vusal")
'''
