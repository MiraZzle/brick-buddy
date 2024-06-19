import json
import brickse
from PyQt6 import QtWidgets, QtGui, QtCore
import urllib.request

from Models.data_model import Model
from Utils.api_requests import get_themes, get_sets_from_theme, SetInfo
from Utils.api_setup import init_brickse


# Constants
WINDOW_TITLE = "BrickBuddy"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
NAVBAR_WIDTH = 200

# Colors
BACKGROUND_COLOR = "#333"
HOVER_COLOR = "#555"
TEXT_COLOR = "white"
SET_WIDGET_BACKGROUND_COLOR = "#1B1B1E"

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initial setup
        self.collections = ["My Collection", "Wishlist", "Favourites"]
        self.themes = get_themes()

        self.SET_DISPLAY_BATCH = 8
        self.current_theme = "Bricklink"
        self.sets = []
        self.displayed_sets_count = 0
        self.displayed_favourites_count = 0

        self.setup_window()
        self.load_navbar()
        self.setup_main_layout()

        self.load_themes()

        # Start with default theme
        self.select_default_theme(self.current_theme)

    def setup_window(self):
        """Setup the main window properties."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

    def setup_main_layout(self):
        """Setup the main layout of the window."""
        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.main_layout)

        # UI components layout
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.ui_layout)

        # Scroll area for the set widgets
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_content = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setSpacing(24)
        self.scroll_content.setLayout(self.scroll_layout)

    def load_navbar(self):
        """Setup the navigation bar."""
        self.navbar_layout = QtWidgets.QVBoxLayout()
        self.navbar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Create a widget for the navbar layout - main container
        self.navbar_widget = QtWidgets.QWidget()
        self.navbar_widget.setLayout(self.navbar_layout)
        self.navbar_widget.setFixedWidth(NAVBAR_WIDTH)
        self.navbar_widget.setStyleSheet("background-color: #333;")

        self.home_button = self.create_nav_button("🏠 Home", self.load_themes)
        self.wishlist_button = self.create_nav_button("⭐ Wishlist", self.load_wishlist)
        self.collections_button = self.create_nav_button(
            "📋 Collections", self.load_collections
        )

        # Add buttons to the navbar layout
        self.navbar_layout.addWidget(self.home_button)
        self.navbar_layout.addWidget(self.wishlist_button)
        self.navbar_layout.addWidget(self.collections_button)

        # Add navbar_widget to the main layout
        self.layout.addWidget(self.navbar_widget)

    def create_nav_button(self, text: str, callback: callable) -> QtWidgets.QPushButton:
        """Helper function to create styled navigation buttons."""
        button = QtWidgets.QPushButton(text)
        # Add functionality to the button
        button.clicked.connect(callback)
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
        return button

    def load_title(self, title: str):
        """Load and display the title."""
        welcome_label = QtWidgets.QLabel(title)

        welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.ui_layout.addWidget(welcome_label)

    def load_theme_dropdown(self):
        """Load and display the theme dropdown."""
        self.theme_dropdown = QtWidgets.QComboBox()
        self.theme_dropdown.addItems(self.themes)
        self.theme_dropdown.setCurrentText(self.current_theme)
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
        """Handle theme change event."""
        selected_theme = self.theme_dropdown.currentText()
        print(f"Selected theme: {selected_theme}")
        self.current_theme = selected_theme
        self.clear_scroll_layout()
        self.load_sets_from_theme(selected_theme)

    def select_default_theme(self, theme_name: str):
        """Select the default theme in the dropdown."""
        index = self.theme_dropdown.findText(theme_name)
        if index != -1:
            self.theme_dropdown.setCurrentIndex(index)

    def load_sets_from_theme(self, theme: str):
        """Load sets from the selected theme."""
        self.sets = get_sets_from_theme(theme)
        self.displayed_sets_count = 0
        self.display_next_sets_batch()

    def display_next_sets_batch(self):
        """Display the next batch of sets."""
        self.displayed_sets_count += self.display_next_batch(
            self.sets, self.displayed_sets_count, self.create_set_widget, 4
        )

    def display_next_wishlist_batch(self):
        """Display the next batch of favourites."""
        self.displayed_favourites_count += self.display_next_batch(
            self.sets, self.displayed_favourites_count, self.create_set_widget, 5
        )

    def display_next_batch(
        self, items_to_display, displayed_amount, widget_create_func, column_count=4
    ):
        """Display the next batch of sets."""
        grid_layout = QtWidgets.QGridLayout()
        row, col = 0, 0
        end_index = displayed_amount + self.SET_DISPLAY_BATCH

        for i in range(displayed_amount, min(end_index, len(items_to_display))):
            set_info = items_to_display[i]
            set_widget = widget_create_func(set_info)
            grid_layout.addWidget(set_widget, row, col)
            col += 1
            if col >= column_count:  # Reset column and move to next row after 4 items
                col = 0
                row += 1

        # Add the new grid layout to the scroll layout
        self.scroll_layout.addLayout(grid_layout)

        # Show or hide the load more button based on whether there are more sets to display
        self.load_more_button.setVisible(end_index < len(items_to_display))

        return end_index

    def add_load_more_button(self, display_func):
        """Add the 'Load More' button."""
        self.load_more_button = QtWidgets.QPushButton("Load More")
        self.load_more_button.clicked.connect(display_func)
        self.main_layout.addWidget(self.load_more_button)

    def clear_main_layout(self):
        """Clear the main layout."""
        print("Clearing main layout")
        self.delete_items_of_layout(self.main_layout)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.main_layout)

        # Normal UI components layout
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.ui_layout)

    def clear_scroll_layout(self):
        """Clear the scroll layout."""
        print("Clearing scroll layout")
        self.delete_items_of_layout(self.scroll_layout)

    def delete_items_of_layout(self, layout: QtWidgets.QLayout):
        """Delete items of a given layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.delete_items_of_layout(item.layout())

    def create_set_widget(self, set_data: SetInfo) -> QtWidgets.QWidget:
        """Create a widget for a single set."""
        set_widget = QtWidgets.QWidget()
        set_layout = QtWidgets.QVBoxLayout()
        image_layout = QtWidgets.QHBoxLayout()
        info_layout = QtWidgets.QVBoxLayout()
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
        set_widget.setStyleSheet("background-color: #1B1B1E;")

        # Set details
        set_name = QtWidgets.QLabel(f"📇 Name: {set_data.name}")
        set_id = QtWidgets.QLabel(f"🪪 ID: {set_data.id}")
        set_pieces = QtWidgets.QLabel(f"🧱 Bricks: {set_data.pieces}")

        info_layout.addWidget(set_name)
        info_layout.addWidget(set_id)
        info_layout.addWidget(set_pieces)
        self.style_card_info(info_layout)

        # Set image
        set_image = self.load_set_image(set_data.image_url)
        image_layout.addWidget(set_image)

        # Action buttons
        wishlist_button = self.create_action_button(
            "⭐ Wishlist", lambda: self.display_favourite_window(set_data)
        )
        add_to_collection_button = self.create_action_button(
            "📋 Collect", lambda: self.display_collect_window(set_data)
        )

        button_layout.addWidget(add_to_collection_button)
        button_layout.addWidget(wishlist_button)

        return set_widget

    def load_set_image(self, image_url: str) -> QtWidgets.QLabel:
        """Load and return the set image."""
        set_image = QtWidgets.QLabel()
        image_data = urllib.request.urlopen(image_url).read()
        image = QtGui.QImage()
        image.loadFromData(image_data)
        pixmap = QtGui.QPixmap(image)

        set_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        set_image.setPixmap(
            pixmap.scaled(
                150,
                150,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        )
        set_image.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        return set_image

    def create_action_button(
        self, text: str, callback: callable
    ) -> QtWidgets.QPushButton:
        """Create and style an action button."""
        button = QtWidgets.QPushButton(text)

        button.setFixedHeight(30)
        button.clicked.connect(callback)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """
        )
        return button

    def style_card_info(self, layout: QtWidgets.QVBoxLayout):
        """Style the information in the card."""
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setWordWrap(True)
                widget.setStyleSheet(
                    """
                    font-size: 14px;
                    font-weight: 500;
                    color: white;
                    margin: 5px 0px 5px 0px;
                """
                )

    def load_themes(self):
        """Load and display themes."""
        self.clear_main_layout()
        self.setup_main_layout()

        self.load_title("Themes")
        self.load_theme_dropdown()
        self.add_load_more_button(self.display_next_sets_batch)
        self.load_sets_from_theme(self.current_theme)

    def load_wishlist(self):
        """Load the wishlist view."""
        self.displayed_favourites_count = 0
        self.clear_main_layout()
        self.setup_main_layout()
        self.load_title("Wishlist")
        self.display_next_wishlist_batch()
        self.load_more_button.clicked.disconnect()
        self.load_more_button.clicked.connect(self.display_next_wishlist_batch)
        print("Loading wishlist")

    def load_collections(self):
        """Load the collections view."""
        self.clear_main_layout()
        self.setup_main_layout()
        self.load_title("Collections")
        print("Loading collections")

    def display_favourite_window(self, set_data: SetInfo):
        """Display the favourite window for a set."""
        set_id = set_data.id
        set_name = set_data.name

        # Create a dialog window
        dialog = self.create_dialog("Favourite Window", 600, 400)
        layout = dialog.layout()

        # Create widgets
        set_name_label = QtWidgets.QLabel(f"Set Name: {set_name}")
        set_id_label = QtWidgets.QLabel(f"Set ID: {set_id}")
        set_notes = QtWidgets.QTextEdit()
        save_button = QtWidgets.QPushButton("Save")

        set_notes.setPlaceholderText("Add notes here")

        save_button.clicked.connect(
            lambda: self.add_to_favorite(set_data, set_notes.toPlainText(), dialog)
        )

        # Add widgets to the layout
        layout.addWidget(set_name_label)
        layout.addWidget(set_id_label)
        layout.addWidget(set_notes)
        layout.addWidget(save_button)

        dialog.exec()

    def add_to_favorite(self, set_data: SetInfo, notes: str, dialog: QtWidgets.QDialog):
        """Add a set to favourites."""
        print(f"Adding set {set_data.id} to favourites")
        print(f"Notes: {notes}")

        Model.save_to_wishlist(set_data.id, notes)
        dialog.close()

    def display_collect_window(self, set_data: SetInfo):
        """Display the collection window for a set."""
        set_id = set_data.id
        set_name = set_data.name

        dialog = self.create_dialog("Collection Window", 600, 400)
        layout = dialog.layout()

        set_name_label = QtWidgets.QLabel(f"Set Name: {set_name}")
        set_id_label = QtWidgets.QLabel(f"Set ID: {set_id}")
        dropdown = QtWidgets.QComboBox()
        theme_label = QtWidgets.QLabel("Select Collection:")

        dropdown.addItems(self.collections)
        dropdown.setCurrentText(self.collections[0])

        set_notes = QtWidgets.QTextEdit()
        set_notes.setPlaceholderText("Add notes here")

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(
            lambda: self.add_to_collection(
                set_data, set_notes.toPlainText(), dialog, dropdown.currentText()
            )
        )

        layout.addWidget(set_name_label)
        layout.addWidget(set_id_label)
        layout.addWidget(theme_label)
        layout.addWidget(dropdown)
        layout.addWidget(set_notes)
        layout.addWidget(save_button)

        dialog.exec()

    def add_to_collection(
        self,
        set_data: SetInfo,
        notes: str,
        dialog: QtWidgets.QDialog,
        collection_name: str,
    ):
        """Add a set to a collection."""
        print(f"Adding set {set_data.id} to collection")
        print(f"Notes: {notes}")
        print(f"Collection: {collection_name}")
        dialog.close()

    def create_dialog(self, title: str, width: int, height: int) -> QtWidgets.QDialog:
        """Helper function to create and return a dialog."""
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(title)
        dialog.setFixedSize(width, height)
        layout = QtWidgets.QVBoxLayout()
        dialog.setLayout(layout)
        return dialog


if __name__ == "__main__":
    init_brickse()

    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
