from repo import Repo
from components.roads import Turn90, Straight, Diagonal

r = Repo()
r.create(description="map1", cols=16, rows=16, cellsize=64, bgcolor='green')
r.create(description="map2", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map3", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map4", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map5", cols=4, rows=4, cellsize=64, bgcolor='green')
r.create(description="map6", cols=4, rows=4, cellsize=64, bgcolor='green')

for a in r.list():
    print(a)
print(f'a {r.listInUse()}')
u = r.attach(1, 'vusal')
uu = r.attach(2, 'vusal')

u.description
ugr = r.attach(1, 'berkay')
ugi = r.attach(6, 'berkay')

r2 = Repo()

r.components.register('turn90', Turn90)
r.components.register('straight', Straight)
st = r.components.create('straight')
tr = r.components.create('turn90')
trr = r.components.create('turn90')
tr2 = r.components.create('straight')
tr3 = r.components.create('turn90')
tr3.rotation = 3
lii = r2.list_attached('vusal')
for a in lii:
    print(a.description + '2')
r.detach(1, 'vusal')
r.detach(2, 'vusal')
print(f'a {r.listInUse()}')

print(ugi.grid[1][0])

lii = r.list_attached('vusal')
for a in lii:
    print(a.description)
r.delete(2)
r.delete(1)
r.delete(6)
for a in r.list():
    print(a)

print(tr.draw())
print(tr2.draw())
print(tr.draw())

ugra = r.objects[1]
r.create(description="F571", cols=10, rows=10, cellsize=64, bgcolor='green')
#r.list() # F571 will be listed with an id
ogr = r.attach(7, "onur")
tgr = r.attach(7, "tolga")  # these two are the same object
#r.components.list() # lists the available components
# assume all components call r.components.register(type, cls)
rt = r.components.create('turn90')
ogr[(1, 1)] = rt
rt.rotation = 0

for j in range(2, 8):
    ogr[(1, j)] = r.components.create('straight')
    ogr[(1, j)].rotation = 0
dt = r.components.create('turn90')
dt.rotation = 1
ogr[(1, 8)] = dt
r.components.register('diagonal', Diagonal)
diag = r.components.create('diagonal')
for i in range(2, 8):
    ogr[(i, 1)] = r.components.create('straight')
    ogr[(i, 8)] = r.components.create('straight')
    ogr[(i, 1)].rotation = 1
    ogr[(i, 8)].rotation = 1
#rt = r.components.create('turn90')
#ogr[(8,1)] = rt
rt.rotation = 3
#ogr.remove(rt)
print(rt.col)
for j in range(2, 8):
    ogr[(8, j)] = r.components.create('straight')
    ogr[(8, j)].rotation = 0
dt = r.components.create('turn90')
dt.rotation = 2
ogr[(8, 8)] = dt
ogw = ogr.view(0, 0, 5, 5)
ogw.remove(rt)
print(ogr.draw())
print(ogw.draw())
print(ogr.draw())
