import json
import brickse
from PyQt6 import QtWidgets, QtGui, QtCore
import urllib.request

from Utils.api_requests import get_themes, get_sets_from_theme, SetInfo
from Utils.api_setup import init_brickse


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.load_navbar()
        self.setup_main_layout()

        self.load_themes()

        # Start with default theme
        self.select_default_theme("Castle")

    def setup_window(self):
        self.setWindowTitle("BrickBuddy")
        self.setGeometry(100, 100, 1280, 720)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

    def setup_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.main_layout)

        # Normal UI components layout
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.ui_layout)

        # Scroll area for the set widgets
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_content = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setSpacing(
            24
        )  # Set the spacing between widgets in the scroll layout
        self.scroll_content.setLayout(self.scroll_layout)

    def load_title(self, title):
        welcome_label = QtWidgets.QLabel(title)
        welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.ui_layout.addWidget(welcome_label)

    def load_theme_dropdown(self):
        themes = get_themes()

        self.theme_dropdown = QtWidgets.QComboBox()
        self.theme_dropdown.addItems(themes)
        self.theme_dropdown.currentIndexChanged.connect(self.theme_changed)

        # Title label
        self.title_label = QtWidgets.QLabel("Select Theme:")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Create a layout for the title and dropdown
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(self.theme_dropdown)

        self.ui_layout.addLayout(self.title_layout)

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
        self.navbar_layout = QtWidgets.QVBoxLayout()
        self.navbar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.navbar_widget = QtWidgets.QWidget()
        self.navbar_widget.setLayout(self.navbar_layout)
        self.navbar_widget.setFixedWidth(200)
        self.navbar_widget.setStyleSheet("background-color: #333;")

        self.home_button = QtWidgets.QPushButton("🏠 Home")
        self.home_button.clicked.connect(self.load_themes)
        self.style_button(self.home_button)

        self.wishlist_button = QtWidgets.QPushButton("⭐ Wishlist")
        self.wishlist_button.clicked.connect(self.load_wishlist)
        self.style_button(self.wishlist_button)

        self.collections_button = QtWidgets.QPushButton("📋 Collections")
        self.collections_button.clicked.connect(self.load_collections)
        self.style_button(self.collections_button)

        self.navbar_layout.addWidget(self.home_button)
        self.navbar_layout.addWidget(self.wishlist_button)
        self.navbar_layout.addWidget(self.collections_button)

        # Add navbar_widget to the main layout
        self.layout.addWidget(self.navbar_widget)

    def style_button(self, button):
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #555;
            }
            """
        )

    def delete_items_of_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.delete_items_of_layout(item.layout())

    def clear_main_layout(self):
        print("Clearing main layout")
        self.delete_items_of_layout(self.main_layout)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.main_layout)

        # Normal UI components layout
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.ui_layout)

    def clear_scroll_layout(self):
        print("Clearing scroll layout")
        self.delete_items_of_layout(self.scroll_layout)

    def create_set_widget(self, set_data: SetInfo):
        set_widget = QtWidgets.QWidget()
        set_layout = QtWidgets.QVBoxLayout()

        image_layout = QtWidgets.QHBoxLayout()
        info_layout = QtWidgets.QHBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        set_layout.addLayout(image_layout)
        set_layout.addLayout(info_layout)
        set_layout.addLayout(button_layout)

        set_widget.setLayout(set_layout)

        # Add shadow effect
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        set_widget.setGraphicsEffect(shadow)

        set_widget.setStyleSheet("background-color: gray;")

        set_name = QtWidgets.QLabel(set_data.name)
        set_id = QtWidgets.QLabel(str(set_data.id))
        set_pieces = QtWidgets.QLabel(str(set_data.pieces))
        info_layout.addWidget(set_name)
        info_layout.addWidget(set_id)
        info_layout.addWidget(set_pieces)

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
        image_layout.addWidget(set_image)

        wishlist_button = QtWidgets.QPushButton("⭐")
        wishlist_button.setFixedSize(30, 30)
        wishlist_button.clicked.connect(
            lambda: print(f"Added {set_data.name} to wishlist")
        )

        add_to_collection_button = QtWidgets.QPushButton("📋")
        add_to_collection_button.setFixedSize(30, 30)
        add_to_collection_button.clicked.connect(
            lambda: print(f"Added {set_data.name} to collection")
        )

        button_layout.addWidget(add_to_collection_button)
        button_layout.addWidget(wishlist_button)

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
        self.clear_main_layout()
        self.setup_main_layout()

        self.load_title("Themes")
        print("Loading themes")
        self.load_theme_dropdown()

    def load_collections(self):
        self.clear_main_layout()
        self.setup_main_layout()
        self.load_title("Collections")
        print("Loading collections")

    def load_wishlist(self):
        self.clear_main_layout()
        self.setup_main_layout()
        self.load_title("Wislist")
        print("Loading wishlist")


if __name__ == "__main__":
    init_brickse()

    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
