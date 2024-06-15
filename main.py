import json
import brickse
from PyQt6 import QtWidgets, QtGui, QtCore
import urllib.request

from Utils.api_requests import get_themes, get_sets_from_theme, SetInfo
from Utils.api_setup import init_brickse

init_brickse()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BrickBuddy")
        self.setGeometry(100, 100, 1280, 720)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Normal UI components layout
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.ui_layout)

        # Scroll area for the set widgets
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)

        self.load_navbar()
        self.load_theme_dropdown()
        self.load_home_page()

        # Start with default theme
        self.select_default_theme("Castle")

    def load_theme_dropdown(self):
        themes = get_themes()

        self.theme_dropdown = QtWidgets.QComboBox()
        self.theme_dropdown.addItems(themes)
        self.theme_dropdown.currentIndexChanged.connect(self.theme_changed)

        # Title label
        self.title_label = QtWidgets.QLabel("Select Theme:")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Create a layout for the title and dropdown
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.theme_dropdown)

        self.ui_layout.addLayout(title_layout)

    def theme_changed(self):
        selected_theme = self.theme_dropdown.currentText()
        print(f"Selected theme: {selected_theme}")
        self.clear_scroll_layout()
        self.load_sets_from_theme(selected_theme)

    def select_default_theme(self, theme_name):
        index = self.theme_dropdown.findText(theme_name)
        if index != -1:
            self.theme_dropdown.setCurrentIndex(index)

    def load_sets_from_theme(self, theme):
        sets = get_sets_from_theme(theme)
        grid_layout = QtWidgets.QGridLayout()
        row, col = 0, 0  # Start adding widgets from row 0, column 0
        for i, set_info in enumerate(sets):
            set_widget = self.create_set_widget(set_info)
            grid_layout.addWidget(set_widget, row, col)
            col += 1
            if col >= 4:  # Reset column and move to next row after 4 items
                col = 0
                row += 1

        # Add the new grid layout to the scroll layout
        self.scroll_layout.addLayout(grid_layout)

    def load_navbar(self):
        self.navbar_container = QtWidgets.QWidget()
        self.navbar_container.setFixedWidth(100)  # Set the fixed width of the navbar
        self.layout.addWidget(
            self.navbar_container
        )  # Add the navbar to the main layout

        self.navbar_container.setStyleSheet(
            "background-color: gray;"
        )  # Set the background color to gray

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

    def load_home_page(self):
        welcome_label = QtWidgets.QLabel("Welcome to BrickBuddy!")
        welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui_layout.addWidget(welcome_label)
        print("Loading home page")

    def delete_items_of_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.delete_items_of_layout(item.layout())

    def clear_scroll_layout(self):
        print("Clearing scroll layout")
        print("Amount:", self.scroll_layout.count())
        self.delete_items_of_layout(self.scroll_layout)
        print("Amount after:", self.scroll_layout.count())

    def create_set_widget(self, set_data: SetInfo):
        set_widget = QtWidgets.QWidget()
        set_layout = QtWidgets.QVBoxLayout()
        set_widget.setLayout(set_layout)

        # Add shadow effect
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        set_widget.setGraphicsEffect(shadow)

        set_widget.setStyleSheet("background-color: lightgray;")

        set_name = QtWidgets.QLabel(set_data.name)
        set_layout.addWidget(set_name)

        set_image = QtWidgets.QLabel()
        image_url = set_data.image_url
        image_data = urllib.request.urlopen(image_url).read()
        image = QtGui.QImage()
        image.loadFromData(image_data)

        pixmap = QtGui.QPixmap(image)
        set_image.setPixmap(
            pixmap.scaled(
                150,
                150,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        )
        set_layout.addWidget(set_image)

        # Set size policy to expand the widgets and images properly
        set_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        set_image.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        return set_widget

    def load_sets(self):
        print("Loading sets")

    def load_themes(self):
        print("Loading themes")

    def load_collections(self):
        print("Loading collections")

    def load_wishlist(self):
        print("Loading wishlist")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
