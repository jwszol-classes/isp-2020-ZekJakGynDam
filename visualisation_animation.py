
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation
from PIL import Image
from query_dynamo import list_airplanes
def visualization():
    airplane_image_path = "src/airplane.png"
    airplane_image = Image.open(airplane_image_path)
 
    # Map initialization
    fig, ax = plt.subplots()
    fig.canvas.toolbar.pack_forget()
    # plt.subplots_adjust(left=-.02, right=1, top=1, bottom=0)

    # coordinates of cities
    x_city = [18.633333, 21.033333, 19.95, 16.091666, 17.033333, 18.76666]
    y_city = [54.366666, 52.2, 50.05, 52.416666, 51.116666, 53.483333]
    city_name = ["Gdańsk", "Warszawa", "Kraków", "Poznań", "Wrocław", "Grudziądz"]


    # creating map
    map_plot = Basemap(projection='mill',llcrnrlat=49,urcrnrlat=55,
                        llcrnrlon=14.116667,urcrnrlon=24.15,resolution='f')

    x_E, _   = map_plot(24.15, 0)
    x_W, _   = map_plot(14.116667, 0)
    _,   y_N = map_plot(0, 55)
    _,   y_S = map_plot(0, 49)
    # print(x_E,x_W,y_N,y_S)
    distance_E_W = x_E - x_W
    distance_N_S = y_N - y_S
    offset_text_city_x = int(5*distance_E_W/400)
    offset_text_city_y = int(5*distance_N_S/400)

    offset_text_airplace_x = int(14*distance_E_W/900)
    offset_text_airplace_y = int(14*distance_N_S/900)

    # map_plot = Basemap(width=1200, height=900, projection='mill',
    #                     llcrnrlat=49,urcrnrlat=55, llcrnrlon=14.116667,urcrnrlon=24.15,resolution='f')

    # map_plot.bluemarble()
    map_plot.drawcoastlines(color='gray')
    map_plot.shadedrelief()
    map_plot.drawcountries(linewidth=1)
    map_plot.drawrivers(color="b")
    # map_plot.drawlsmask(land_color=(0,0,0,0), ocean_color=(255,0,0,255))

    # ploting cities
    for i in range(len(x_city)):
        xo, yo = map_plot(x_city[i], y_city[i])
        plt.plot(xo, yo, 'ro', markersize=5)
        plt.text(xo+offset_text_city_x, yo+offset_text_city_y, city_name[i], fontsize=10)

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

        data=list_airplanes()
        x_p_temp_list = []
        y_p_temp_list = []
        # bearing_list = []
        x_p = data["Longitude"]
        y_p = data["Latitude"]
        # y_p -> dane["wysokosc geograficzna"]
        for i in range(len(x_p)):
            x_p_temp, y_p_temp = map_plot(x_p[i], y_p[i])
            x_p_temp_list.append(x_p_temp)
            y_p_temp_list.append(y_p_temp)
            # bearing_list.append()
        # print(x_p_temp_list,y_p_temp_list)
        artists = []

        plane_name=data["ICAO"]

        for i in range(len(x_p_temp_list)):

            rotated = airplane_image.rotate(data['Heading'][i])
            airplane_image_resized = rotated.resize((16,16))

            airplane_image_resized_arr = np.asarray(airplane_image_resized)

            offsetImage = OffsetImage(airplane_image_resized_arr)

            artists.append(ax.text(x_p_temp_list[i]+offset_text_airplace_x, 
                                   y_p_temp_list[i]+offset_text_airplace_y, plane_name[i], fontsize=10))
            artist = ax.add_artist(AnnotationBbox(offsetImage, (x_p_temp_list[i], y_p_temp_list[i]), frameon=False))
            artists.append(artist)

        ln_planes.set_data(x_p_temp_list, y_p_temp_list)
        artists.append(ln_planes)
        return artists

    ani = FuncAnimation(plt.gcf(), update, init_func=init, interval=100, blit=True)
    # plt.tight_layout(pad=0.05)
    plt.show()


if __name__ == "__main__":
    visualization()
