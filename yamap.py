import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from interface import Ui_MainWindow
from io import BytesIO
from PIL import Image


class YaMap(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_adres = "Санкт-Петербург, Адмирала Коновалова, д.6, к.2"
        self.spn = 0.002
        self.map_type = 'map'
        self.find_toponim()
        self.load_map()
        self.setFocusPolicy(Qt.StrongFocus)

    def initUI(self):
        self.setupUi(self)
        self.find_btn.clicked.connect(self.search)
        self.shema_btn.clicked.connect(self.shema)
        self.sputnik_btn.clicked.connect(self.sputnik)
        self.gibrid_btn.clicked.connect(self.gibrid)

    def keyPressEvent(self, event):

        # движ
        if event.key() == Qt.Key_Up:
            if float(self.y) + self.spn < 90:
                self.y = str(float(self.y) + self.spn)
                self.load_map()
        if event.key() == Qt.Key_Down:
            if float(self.y) - self.spn > -90:
                self.y = str(float(self.y) - self.spn)
                # print('.....')
            self.load_map()
        if event.key() == Qt.Key_Right:
            if float(self.x) + self.spn < 180:
                self.x = str(float(self.x) + self.spn)
                self.load_map()
        if event.key() == Qt.Key_Left:
            if float(self.x) - self.spn > -180:
                # print('.....')
                self.x = str(float(self.x) - self.spn)
                self.load_map()

        # масштаб
        if event.key() == Qt.Key_PageUp:
            if self.spn > 0.00005:
                self.spn /= 2
                self.load_map()
        if event.key() == Qt.Key_PageDown:
            if self.spn < 50.00:
                self.spn *= 2
                self.load_map()

    def search(self):
        self.start_adres = self.find_line.text()
        self.find_toponim()
        self.load_map()

    def shema(self):
        self.map_type = "map"
        self.load_map()

    def sputnik(self):
        self.map_type = "sat"
        self.load_map()

    def gibrid(self):
        self.map_type = "sat,skl"
        self.load_map()

    def find_toponim(self):
        if not self.start_adres:
            return False
        coord_find = self.start_adres
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": coord_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params).json()

        if not response:
            return False

        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        self.x, self.y = toponym_coodrinates.split(" ")

    def load_map(self):
        spn = str(self.spn)

        map_params = {
            "ll": ",".join([self.x, self.y]),
            "spn": ",".join([spn, spn]),
            "l": self.map_type
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        Image.open(BytesIO(response.content)).save('map.png')

        self.img.setPixmap(QPixmap('map.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YaMap()
    ex.show()
    sys.exit(app.exec_())
