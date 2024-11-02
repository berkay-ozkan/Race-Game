from repo import Repo


r = Repo()
r.create(description = "map1", cols = 4, rows = 4, cellsize = 64, bgcolor = 'green')
r.create(description = "map2", cols = 4, rows = 4, cellsize = 64, bgcolor = 'green')
r.create(description = "map3", cols = 4, rows = 4, cellsize = 64, bgcolor = 'green')
r.create(description = "map4", cols = 4, rows = 4, cellsize = 64, bgcolor = 'green')
r.create(description = "map5", cols = 4, rows = 4, cellsize = 64, bgcolor = 'green')
r.create(description = "map6", cols = 4, rows = 4, cellsize = 64, bgcolor = 'green')

for a in r.list():
    print (a)
print(f'a {r.listInUse()}')
u = r.attach(1, 'vusal' )
u = r.attach(2, 'vusal' )

u.description
ugr = r.attach(1, 'berkay')
lii = r.listAttached('vusal')
for a in lii:
    print(a.description)

print(f'a {r.listInUse()}')


r.detach(1, 'vusal')
r.detach(2, 'vusal') 
print(f'a {r.listInUse()}')


lii = r.listAttached('vusal')
for a in lii:
    print(a.description)
r.delete(2)
r.delete(1)
r.delete(6)
for a in r.list():
    print(a)