from PIL import Image
from exif import Image
import gmplot
import os

API_KEY = open('api_key.txt', 'r').read()

class processor:
    def __init__(self):
        return
    
    #edited from https://stackoverflow.com/a/73267185/11142058 
    def translate(self, coords, ref):
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref =='W':
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    def get_location(self, path):
        img = Image(open(str('images/' + path), 'rb'))
        if img.has_exif:
            try:
                img.gps_longitude
                coords = (self.translate(img.gps_latitude,
                        img.gps_latitude_ref),
                        self.translate(img.gps_longitude,
                        img.gps_longitude_ref))
            except AttributeError:
                print ('The Image has no Coordinates')
        else:
            print ('The Image has no Metadata')
            
        return(Point(coords[0], coords[1], img))
    
class Point:
    def __init__(self, longitude, latitude, img):
        self.lng = longitude
        self.lat = latitude
        self.img = img

class Plotter:
    def __init__(self):
        self.lngs = None
        self.lats = None
        self.c_lat = 43.6532
        self.c_lng = -79.3832
        self.map = None

    def set_center(self):
        self.c_lng = sum(self.lngs) / len(self.lngs)
        self.c_lat = sum(self.lats) / len(self.lats)
        self.set_map()

    def set_map(self):
        self.map = gmplot.GoogleMapPlotter(self.c_lat, self.c_lng, 13, apikey=API_KEY)
    
    def set_points(self, points):
        self.lats = [p.lat for p in points]
        self.lngs = [p.lng for p in points]
        self.set_center()
    
    def add_point(self, point):
        self.lngs.append(point.lng)
        self.lats.append(point.lat)
        self.set_center()
        
    def plot_heatmap(self):
        try:
            self.map.heatmap(self.lats, self.lngs)
        except RuntimeError:
            print('No map object initialized.')
    
    def plot_scatter(self):
        try:
            self.map.scatter(self.lats, self.lngs)
        except RuntimeError:
            print('No map object initialized.')
        
    def export(self):
        self.map.draw('map.html')


def main():
    pro = processor()
    points = []
    for img in os.listdir('images'):
        points.append(pro.get_location(img))

    plt = Plotter()
    plt.set_points(points)
    plt.export()
    print(plt.map.get())
    

if __name__ == '__main__':
    main()