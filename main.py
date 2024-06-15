import json
import brickse
from PyQt6 import QtWidgets, QtGui, QtCore
import urllib.request

from Utils.api_requests import get_themes, get_sets_from_theme
from Utils.api_setup import init_brickse

init_brickse()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BrickBuddy")
        self.setGeometry(100, 100, 800, 600)

        self.layout = (
            QtWidgets.QHBoxLayout()
        )  # Changed to QHBoxLayout to accommodate the navbar and main content side by side
        self.setLayout(self.layout)

        # Placeholder for main content
        self.navbar_container = QtWidgets.QWidget()
        self.navbar_container.setFixedWidth(100)  # Set the fixed width of the navbar
        self.layout.addWidget(
            self.navbar_container
        )  # Add the navbar to the main layout

        self.main_content = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_content.setLayout(self.main_layout)
        self.layout.addWidget(self.main_content)

        self.load_navbar()
        self.load_home_page()
        self.load_theme_dropdown()

    def load_theme_dropdown(self):
        themes = get_themes()

        self.theme_dropdown = QtWidgets.QComboBox()
        self.theme_dropdown.addItems(themes)
        self.theme_dropdown.currentIndexChanged.connect(self.theme_changed)

        self.main_layout.addWidget(self.theme_dropdown)

    def theme_changed(self):
        selected_theme = self.theme_dropdown.currentText()
        print(f"Selected theme: {selected_theme}")
        self.load_sets_from_theme(selected_theme)
        # Add any additional logic to handle the theme change here

    def load_sets_from_theme(self, theme):
        print(get_sets_from_theme(theme))

    def load_navbar(self):
        self.navbar_container.setStyleSheet(
            "background-color: gray;"
        )  # Set the background color to blue

        navbar_layout = QtWidgets.QVBoxLayout()
        navbar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.navbar_container.setLayout(navbar_layout)

        self.home_button = QtWidgets.QPushButton("Home")
        self.home_button.clicked.connect(self.load_sets)

        self.wishlist_button = QtWidgets.QPushButton("Wishlist")
        self.wishlist_button.clicked.connect(self.load_sets)

        self.collections_button = QtWidgets.QPushButton("Collections")
        self.collections_button.clicked.connect(self.load_themes)

        navbar_layout.addWidget(self.home_button)
        navbar_layout.addWidget(self.wishlist_button)
        navbar_layout.addWidget(self.collections_button)

    def load_sets(self):
        print("Loading sets")

    def load_themes(self):
        print("Loading themes")

    def load_collections(self):
        print("Loading collections")

    def load_wishlist(self):
        print("Loading wishlist")

    def load_home_page(self):
        self.main_layout.addWidget(QtWidgets.QLabel("Welcome to BrickBuddy!"))
        print("Loading home page")

    def create_set_widget(self, set_data):
        set_widget = QtWidgets.QWidget()
        set_layout = QtWidgets.QVBoxLayout()
        set_widget.setLayout(set_layout)

        set_name = QtWidgets.QLabel(set_data["name"])
        set_layout.addWidget(set_name)

        set_image = QtWidgets.QLabel()
        image_url = set_data["set_img_url"]
        image_data = urllib.request.urlopen(image_url).read()
        image = QtGui.QImage()
        image.loadFromData(image_data)
        set_image.setPixmap(QtGui.QPixmap(image))
        set_layout.addWidget(set_image)

        return set_widget


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
