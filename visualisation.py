
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#coordinates of cities
x = [18.633333, 21.033333, 19.95, 16.091666, 17.033333, 18.76666]
y = [54.366666, 52.2, 50.05, 52.416666, 51.116666, 53.483333]
city_name = ["Gdańsk", "Warszawa", "Kraków", "Poznań", "Wrocław", "Grudziądz"]

#coordinates of planes
x_p = [17.1, 22.2, 21.0]
y_p = [50.8, 50.8, 51.2]
plane_name = ["Boeing", "AirbusA", "LockheedL"]

#temporary direction
x_dir = list()
y_dir = list()
dx = 0.01
dy = 0.01
for i in range (len(x_p)):
    xd = np.random.randint(-1, 2)*dx
    yd = np.random.randint(-1, 2)*dy
    if xd == 0 and yd == 0:
        xd = dx
    x_dir.append(xd)
    y_dir.append(yd)

print(x_dir,y_dir)

#creating map
map = Basemap(projection='mill',llcrnrlat=49,urcrnrlat=55,
            llcrnrlon=14.116667,urcrnrlon=24.15,resolution='h')

map.drawcoastlines(color='gray')
map.shadedrelief()
map.drawcountries()

#ploting cities
for i in range(len(x)):
    xo, yo = map(x[i], y[i])
    plt.plot(xo, yo, 'ok', markersize=5)
    plt.text(xo, yo, city_name[i], fontsize=10)

#ploting planes
for k in range(1000):
    if k > 0:
        scat.remove()
        #name.remove()
    xt = list()
    yt = list()
    for i in range(len(x_p)):
        tempx, tempy = map(x_p[i]+k*x_dir[i], y_p[i]+k*y_dir[i])
        xt.append(tempx)
        yt.append(tempy)
    scat = plt.scatter(xt, yt, c='red')
    #name = plt.text(xt + 15000, yt, plane_name[i], fontsize=7)               #plt.text function can't take lists as arguments - rewrite!
    plt.draw()
    plt.pause(0.1)


plt.show()
