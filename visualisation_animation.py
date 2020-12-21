
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation


def visualization():
    # Map initialization
    fig = plt.figure()
    axes = fig.add_subplot(1,1,1)
    fig.canvas.toolbar.pack_forget()
    # plt.subplots_adjust(left=-.02, right=1, top=1, bottom=0)

    # coordinates of cities
    x_city = [18.633333, 21.033333, 19.95, 16.091666, 17.033333, 18.76666]
    y_city = [54.366666, 52.2, 50.05, 52.416666, 51.116666, 53.483333]
    city_name = ["Gdańsk", "Warszawa", "Kraków", "Poznań", "Wrocław", "Grudziądz"]


    # creating map
    map_plot = Basemap(projection='mill',llcrnrlat=49,urcrnrlat=55,
                        llcrnrlon=14.116667,urcrnrlon=24.15,resolution='f')

    # map_plot = Basemap(width=1200, height=900, projection='mill',
    #                     llcrnrlat=49,urcrnrlat=55, llcrnrlon=14.116667,urcrnrlon=24.15,resolution='f')

    # map_plot.bluemarble()
    map_plot.drawcoastlines(color='gray')
    map_plot.shadedrelief()
    map_plot.drawcountries()

    # ploting cities
    for i in range(len(x_city)):
        xo, yo = map_plot(x_city[i], y_city[i])
        plt.plot(xo, yo, 'ok', markersize=5)
        plt.text(xo, yo, city_name[i], fontsize=10)

    #coordinates of planes
    x_p = [17.1, 22.2, 21.0]
    y_p = [50.8, 50.8, 51.2]
    plane_name = ["Boeing", "AirbusA", "LockheedL"]

    # Prepare lists for airplane
    x_airplanes, y_airplanes = map_plot(0, 0)


    # Get handles for axes
    ln_planes, = map_plot.plot(x_airplanes, y_airplanes, 'bo', markersize=3)


    def init():
        ln_planes.set_data([], [])
        return ln_planes,

    def update(frame):

        dx = np.random.randint(0, 10)
        dy = np.random.randint(0, 10)
        x_p_temp_list = []
        y_p_temp_list = []
        for i in range(len(x_p)):
            x_p_temp, y_p_temp = map_plot(x_p[i]+dx, y_p[i]+dy)
            x_p_temp_list.append(x_p_temp)
            y_p_temp_list.append(y_p_temp)

        ln_planes.set_data(x_p_temp_list, y_p_temp_list)
        return ln_planes,

    ani = FuncAnimation(plt.gcf(), update, init_func=init, interval=1, blit=True)
    # plt.tight_layout(pad=0.05)
    plt.show()


if __name__ == "__main__":
    visualization()
