from opensky_api import OpenSkyApi
import numpy as np

class Coordinates:
    ''' Klasa zajmująca się pobraniem z API i przekształceniem współrzędnych do pożądanej postaci '''
    def __init__(self,API):
        self.bounding_box = (49.0273953314, 54.8515359564, 14.0745211117,24.0299857927)
        self.api=API
        self.state = []
        self.coords = []
    def UpdateState(self):
        ''' Wywołuje api do aktualizacji stanu - jeżeli nie podano konta do api, nie należy wywoływać zbyt często '''
        self.state=self.api.get_states(bbox=self.bounding_box).states
    def GetCoordinatesNormalized(self):
        ''' Zwraca unormowane wartości współrzędnych oraz kierunek względem północy magnetycznej (chyba) '''

        norm_coords = np.zeros((len(self.state),3))

        for i in range(len(self.state)):
            norm_coords[i][0] = (self.state[i].latitude-self.bounding_box[0])/(self.bounding_box[1]-self.bounding_box[0])
            norm_coords[i][1] = (self.state[i].longitude-self.bounding_box[2])/(self.bounding_box[3]-self.bounding_box[2])
            norm_coords[i][2] = self.state[i].heading
        
        self.coords=norm_coords
        return norm_coords
if __name__=="__main__":
    api = OpenSkyApi()
    crds = Coordinates(api)
    crds.UpdateState()
    crds.GetCoordinatesNormalized()
    
    print(crds.coords) 
