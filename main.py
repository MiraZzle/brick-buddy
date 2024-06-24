import json
import brickse
from PyQt6 import QtWidgets, QtGui, QtCore
import urllib.request

from Models.data_model import Model, CollectedSet
from Utils.api_requests import get_themes, get_sets_from_theme, SetInfo
from Utils.api_setup import init_brickse


# Constants
WINDOW_TITLE = "BrickBuddy"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
NAVBAR_WIDTH = 200
DEFAULT_THEME = "Bricklink"
SET_DISPLAY_BATCH = 8
COLUMN_COUNT_COLLECTIONS = 4

# Colors
BACKGROUND_COLOR = "#333"
HOVER_COLOR = "#555"
TEXT_COLOR = "white"
SET_WIDGET_BACKGROUND_COLOR = "#1B1B1E"

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setup_default_values()
        self.setup_set_informations()
        self.setup_set_informations()
        self.setup_counts()
        self.setup_window()
        self.load_navbar()
        self.setup_main_layout()
        self.load_themes()

        self.select_default_theme(self.current_theme)

    # ============================ SETUP ============================#

    def setup_default_values(self):
        """Setup default values for the application."""
        self.SET_DISPLAY_BATCH = 8
        self.current_theme = "Bricklink"

    def setup_set_informations(self):
        """Setup information about sets, collections, and themes."""
        self.collections = Model.get_all_collections()
        self.collection_names = [collection[0] for collection in self.collections]
        self.themes = get_themes()
        self.wishlisted_sets = Model.get_wishlist_data()
        self.sets = []
        self.currently_selected_collection = []

    def setup_counts(self) -> None:
        """Setup the counts for the displayed items."""
        self.displayed_sets_count = 0
        self.displayed_wishlist_items_count = 0
        self.displayed_collections_count = 0
        self.displayed_collected_sets_count = 0
        self.current_row = 0
        self.current_col = 0

    def setup_window(self) -> None:
        """Setup the main window properties."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

    def setup_main_layout(self) -> None:
        """Setup the main layout of the window."""
        # Layouts
        self.main_layout = QtWidgets.QVBoxLayout()
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()

        # Scroll area - for inidividual set widgets
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_content = QtWidgets.QWidget()

        # Add layouts to the main layout
        self.layout.addLayout(self.main_layout)
        self.main_layout.addLayout(self.ui_layout)

        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout.setSpacing(24)
        self.scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(self.scroll_area)
        self.scroll_layout.addLayout(self.grid_layout)
        self.scroll_content.setLayout(self.scroll_layout)

    # ============================ UI ELEMENTS ============================#

    def load_navbar(self) -> None:
        """Setup the navigation bar."""
        self.navbar_layout = QtWidgets.QVBoxLayout()
        self.navbar_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Create a widget for the navbar layout - main container
        self.navbar_widget = QtWidgets.QWidget()
        self.navbar_widget.setLayout(self.navbar_layout)
        self.navbar_widget.setFixedWidth(NAVBAR_WIDTH)  # Set fixed width for the navbar
        self.navbar_widget.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")

        self.add_navbar_buttons()

        # Add navbar_widget to the main layout
        self.layout.addWidget(self.navbar_widget)

    def add_navbar_buttons(self) -> None:
        """Add navigation buttons to the navbar."""
        # Create navigation buttons and connect them
        self.home_button = self.create_nav_button("🏠 Home", self.load_themes)
        self.wishlist_button = self.create_nav_button("⭐ Wishlist", self.load_wishlist)
        self.collections_button = self.create_nav_button(
            "📋 Collections", self.load_collections
        )

        # Add buttons to the navbar layout
        self.navbar_layout.addWidget(self.home_button)
        self.navbar_layout.addWidget(self.wishlist_button)
        self.navbar_layout.addWidget(self.collections_button)

    def create_nav_button(self, text: str, callback: callable) -> QtWidgets.QPushButton:
        """Helper function to create styled navigation buttons."""
        button = QtWidgets.QPushButton(text)
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

    # ============================ LOADING ============================#

    def load_title(self, title: str) -> None:
        """Load and display the title."""
        welcome_label = QtWidgets.QLabel(title)

        welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        welcome_label.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )  # Style the title

        self.ui_layout.addWidget(welcome_label)

    def load_page_description(self, description: str) -> None:
        """Load and display the page description."""
        description_label = QtWidgets.QLabel(description)
        description_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        description_label.setStyleSheet("font-size: 16px; color: #BBB;")

        self.ui_layout.addWidget(description_label)

    def load_dropdown_label(self) -> None:
        """Load and display a dropdown label."""
        dropdown_label = QtWidgets.QLabel("Select Theme:")
        dropdown_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        dropdown_label.setStyleSheet("font-size: 16px; color: #BBB;")

        self.title_layout.addWidget(dropdown_label)

    def load_theme_dropdown(self) -> None:
        """Load and display the theme dropdown."""
        self.title_layout = QtWidgets.QHBoxLayout()
        self.theme_dropdown = QtWidgets.QComboBox()

        self.theme_dropdown.addItems(self.themes)  # Populate the dropdown with themes
        self.theme_dropdown.setCurrentText(self.current_theme)  # Set the default theme
        self.theme_dropdown.currentIndexChanged.connect(
            self.theme_changed
        )  # Signal when user changes the theme

        self.title_layout.addWidget(self.theme_dropdown)
        self.load_dropdown_label()
        self.ui_layout.addLayout(self.title_layout)

    def theme_changed(self) -> None:
        """Handle user changing the theme in dropdown."""
        selected_theme = self.theme_dropdown.currentText()  # Get the selected theme
        self.current_theme = selected_theme  # Update the current theme

        # Clear the grid layout and load sets from the selected theme
        self.clear_grid_layout()
        self.current_row = 0
        self.current_col = 0

        # Load sets from the selected theme
        self.load_sets_from_theme(selected_theme)

    def select_default_theme(self, theme_name: str) -> None:
        """Select the default theme in the dropdown.

        Args:
            theme_name (str): The name of the theme to select."""
        index = self.theme_dropdown.findText(theme_name)
        if index != -1:  # If the theme is found
            self.theme_dropdown.setCurrentIndex(index)

    def load_sets_from_theme(self, theme: str) -> None:
        """Load and display sets from the selected theme.

        Args:
            theme (str): The selected theme."""
        self.sets = get_sets_from_theme(theme)  # Update the sets
        self.displayed_sets_count = 0
        self.display_next_sets_batch()  # Display first batch of sets

    # ============================ BATCH DISPLAYING ============================#

    def display_next_sets_batch(self) -> None:
        """Display the next batch of sets from current theme."""
        self.displayed_sets_count += self.display_next_batch(
            self.sets, self.displayed_sets_count, self.create_set_widget, 4
        )

    def display_next_wishlist_batch(self) -> None:
        """Display the next batch of wishlisted sets."""
        print(self.displayed_wishlist_items_count)
        self.displayed_wishlist_items_count += self.display_next_batch(
            self.wishlisted_sets,
            self.displayed_wishlist_items_count,
            self.create_wishlist_set_widget,
            2,
        )

    def display_next_collected_sets_batch(self):
        """Display the next batch of collected sets."""
        self.displayed_collected_sets_count += self.display_next_batch(
            self.currently_selected_collection,
            self.displayed_collected_sets_count,
            self.display_collected_set_widget,
            4,
        )

    def display_next_batch_of_collections(self):
        self.displayed_collections_count += self.display_next_batch(
            self.collections,
            self.displayed_collections_count,
            self.create_collection_widget,
            1,
        )

    def display_next_batch(
        self,
        items_to_display: list,
        displayed_amount: int,
        widget_create_func: callable,
        column_count: int = 4,
    ) -> int:
        """Display the next batch of widgets using the specified widget creation callback."""
        end_index = displayed_amount + self.SET_DISPLAY_BATCH

        for i in range(displayed_amount, min(end_index, len(items_to_display))):
            set_info = items_to_display[i]
            set_widget = widget_create_func(set_info)
            self.grid_layout.addWidget(set_widget, self.current_row, self.current_col)
            self.current_col += 1
            if self.current_col >= column_count:
                self.current_col = 0
                self.current_row += 1

        self.load_more_button.setVisible(end_index < len(items_to_display))
        return end_index

    # ============================ WIDGETS ============================#

    def add_load_more_button(self, display_func):
        """Add the 'Load More' button."""
        self.load_more_button = QtWidgets.QPushButton("Load More")
        self.load_more_button.clicked.connect(display_func)
        self.main_layout.addWidget(self.load_more_button)

    def clear_main_layout(self):
        """Clear the main layout."""
        # print("Clearing main layout")
        self.delete_items_of_layout(self.main_layout)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.main_layout)
        self.grid_layout = QtWidgets.QGridLayout()
        self.main_layout.addLayout(self.ui_layout)

        # Normal UI components layout
        self.ui_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.grid_layout)

    def clear_grid_layout(self):
        """Clear the grid layout."""
        # print("Clearing grid layout")
        self.delete_items_of_layout(self.grid_layout)
        self.current_row = 0
        self.current_col = 0

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

    def create_wishlist_set_widget(self, set_info) -> QtWidgets.QWidget:
        set_data = SetInfo(
            set_id=set_info[0],
            set_name=set_info[1],
            set_img_url=set_info[2],
            brickset_url=set_info[3],
            year=set_info[4],
            pieces=set_info[5],
        )

        set_notes = set_info[6]

        """Create a widget for a single set."""
        set_widget = QtWidgets.QWidget()
        set_layout = QtWidgets.QHBoxLayout()
        image_layout = (
            QtWidgets.QVBoxLayout()
        )  # Changed to QVBoxLayout for better alignment
        info_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        left_side_layout = QtWidgets.QVBoxLayout()
        set_layout.addLayout(left_side_layout)
        set_layout.addLayout(image_layout)

        # Set the stretch factors
        set_layout.setStretch(0, 1)
        set_layout.setStretch(1, 1)

        left_side_layout.addLayout(info_layout)
        left_side_layout.addLayout(button_layout)
        set_widget.setLayout(set_layout)

        # Add shadow effect
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        set_widget.setGraphicsEffect(shadow)
        set_widget.setStyleSheet("background-color: #1B1B1E;")
        set_widget.setMaximumHeight(400)

        # Set details
        set_name = QtWidgets.QLabel(f"📇 Name: {set_data.name}")
        set_id = QtWidgets.QLabel(f"🪪 ID: {set_data.id}")
        set_pieces = QtWidgets.QLabel(f"🧱 Bricks: {set_data.pieces}")

        # add id as link

        set_brickset_url = QtWidgets.QLabel(
            f"🔗 <a href={set_data.brickset_url}>Brickset Link</a>"
        )
        set_brickset_url.setOpenExternalLinks(True)

        info_layout.addWidget(set_name)
        info_layout.addWidget(set_id)
        info_layout.addWidget(set_pieces)
        info_layout.addWidget(set_brickset_url)
        self.style_card_info(info_layout)

        # Set image
        set_image = self.load_set_image(set_data.image_url)
        image_layout.addWidget(set_image)

        # Action buttons
        detail_button = self.create_action_button(
            "🔍 Detail",
            lambda: self.show_wishlist_detail_dialog(set_data, notes=set_notes),
        )
        button_layout.addWidget(detail_button)

        delete_button = self.create_action_button(
            "❌ Delete",
            lambda: self.remove_from_wishlist(set_id=set_data.id, widget=set_widget),
        )
        button_layout.addWidget(delete_button)

        return set_widget

    def remove_from_wishlist(self, set_id: str, widget: QtWidgets.QWidget):
        """Remove a set from the wishlist."""
        print(f"Removing set {set_id} from wishlist")
        Model.remove_from_wishlist(set_id)
        self.remove_widget(widget)

    def remove_widget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the layout."""

        widget.deleteLater()

    def show_wishlist_detail_dialog(self, set_data: SetInfo, notes: str):
        """Display the wishlist detail dialog."""
        dialog = self.create_dialog("Wishlist Detail", 600, 400)
        layout = dialog.layout()

        set_name_label = QtWidgets.QLabel(f"Set Name: {set_data.name}")
        set_id_label = QtWidgets.QLabel(f"Set ID: {set_data.id}")
        set_notes = QtWidgets.QTextEdit()
        set_notes.setPlainText(notes)

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(
            lambda: self.update_wishlisted_set_notes(
                set_data.id, set_notes.toPlainText(), dialog
            )
        )

        layout.addWidget(set_name_label)
        layout.addWidget(set_id_label)
        layout.addWidget(set_notes)
        layout.addWidget(save_button)

        dialog.exec()

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
        self.collections = Model.get_all_collections()
        self.collection_names = [collection[0] for collection in self.collections]

        self.displayed_sets_count = 0
        self.clear_main_layout()
        # self.clear_grid_layout()

        self.current_row = 0
        self.current_col = 0
        self.setup_main_layout()

        self.load_title("Themes")
        self.load_theme_dropdown()
        self.add_load_more_button(self.display_next_sets_batch)
        self.load_sets_from_theme(self.current_theme)

    # ============================ SCENES ============================#

    def load_wishlist(self):
        """Load the wishlist view."""
        self.displayed_wishlist_items_count = 0
        self.clear_main_layout()
        self.setup_main_layout()

        self.wishlisted_sets = Model.get_wishlist_data()

        self.load_title("Wishlist")
        self.add_load_more_button(self.display_next_wishlist_batch)
        self.display_next_wishlist_batch()

    def load_collections(self):
        """Load the collections view."""
        self.collections = Model.get_all_collections()
        self.collection_names = [collection[0] for collection in self.collections]
        self.displayed_collections_count = 0
        self.clear_main_layout()
        self.setup_main_layout()

        self.load_title("Collections")
        self.ui_layout.addWidget(self.display_new_collection_button())
        self.add_load_more_button(self.display_next_batch_of_collections)
        self.display_next_batch_of_collections()
        print("Loading collections")

    def display_sets_from_collection(self, collection_name, collection_description):
        self.clear_main_layout()
        self.setup_main_layout()

        self.displayed_collected_sets_count = 0
        self.currently_selected_collection = Model.get_collection_data(collection_name)

        self.load_title(f"Collection: {collection_name}")
        self.load_page_description(f"Description: {collection_description}")
        self.add_load_more_button(self.display_next_collected_sets_batch)
        self.display_next_collected_sets_batch()

    # ============================ FAVOURITES ============================#

    def display_favourite_window(self, set_data: SetInfo):
        """Display the favourite window for a set."""
        set_id = set_data.id
        set_name = set_data.name

        # Create a dialog window
        dialog = self.create_dialog("Favourite Window", 600, 400)
        layout = dialog.layout()

        # Styling the dialog layout
        dialog.setStyleSheet(
            """
            QDialog {
                background-color: #2C2C2E;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 20px;
            }
            """
        )

        # Create widgets
        set_name_label = QtWidgets.QLabel(f"Set Name: {set_name}")
        set_name_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: white;"
        )

        set_id_label = QtWidgets.QLabel(f"Set ID: {set_id}")
        set_id_label.setStyleSheet("font-size: 16px; color: #BBB;")

        set_notes = QtWidgets.QTextEdit()
        set_notes.setStyleSheet(
            """
            QTextEdit {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                border-radius: 5px;
                padding: 10px;
            }
            """
        )
        set_notes.setPlaceholderText("Add notes here")

        save_button = QtWidgets.QPushButton("Save")
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
            """
        )
        save_button.clicked.connect(
            lambda: self.add_to_favorite(set_data, set_notes.toPlainText(), dialog)
        )

        # Add widgets to the layout
        layout.addWidget(set_name_label)
        layout.addWidget(set_id_label)
        layout.addWidget(set_notes)
        layout.addWidget(save_button)

        dialog.exec()

    def update_wishlisted_set_notes(self, set_id: str, notes: str, dialog):
        """Update the notes for a wishlisted set."""
        print(f"Updating notes for set {set_id}")
        print(f"Notes: {notes}")
        Model.update_wishlisted_set_notes(set_id, notes)
        dialog.close()

    def add_to_favorite(self, set_data: SetInfo, notes: str, dialog: QtWidgets.QDialog):
        """Add a set to favourites."""
        print(f"Adding set {set_data.id} to favourites")
        print(f"Notes: {notes}")

        Model.save_to_wishlist(set_data, notes)
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

        dropdown.addItems(self.collection_names)
        dropdown.setCurrentText(self.collection_names[0])

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
        Model.save_collected_set(set_data, collection_name, notes)
        dialog.close()

    def create_dialog(self, title: str, width: int, height: int) -> QtWidgets.QDialog:
        """Helper function to create and return a dialog."""
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(title)
        dialog.setFixedSize(width, height)
        layout = QtWidgets.QVBoxLayout()
        dialog.setLayout(layout)
        return dialog

    def style_call_to_action_button(self, button: QtWidgets.QPushButton):
        """Style the call to action button."""
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
        """
        )

    def display_new_collection_button(self):
        """Display the 'Create Collection' button."""
        create_button = QtWidgets.QPushButton("Create Collection")
        self.style_call_to_action_button(create_button)
        create_button.clicked.connect(self.create_collection_dialog)
        return create_button

    def create_collection_dialog(self):
        """Create a new collection."""
        dialog = self.create_dialog("Create Collection", 600, 400)
        layout = dialog.layout()

        window_description = QtWidgets.QLabel("Create a new collection")
        collection_name_input = QtWidgets.QLineEdit()
        collection_name_input.setPlaceholderText("Enter collection name")

        collection_description_input = QtWidgets.QTextEdit()
        collection_description_input.setPlaceholderText("Enter collection description")

        save_button = self.create_action_button(
            "💾 Save collection",
            lambda: self.save_collection(
                collection_name_input.text(),
                collection_description_input.toPlainText(),
                dialog,
            ),
        )

        layout.addWidget(window_description)
        layout.addWidget(collection_name_input)
        layout.addWidget(collection_description_input)
        layout.addWidget(save_button)

        dialog.exec()

    def save_collection(self, name, description, dialog: QtWidgets.QDialog):
        """Save the new collection."""
        print(f"Saving collection: {name} - {description}")
        Model.create_collection(name, description)
        dialog.close()
        self.load_collections()

    # ============================ COLLECTIONS ============================#

    def create_collection_widget(self, collection_info: tuple):
        """Show a collection card."""
        collection_name = collection_info[0]
        collection_description = collection_info[1]

        layout = QtWidgets.QVBoxLayout()
        collection_widget = QtWidgets.QWidget()
        collection_widget.setLayout(layout)

        collection_name_label = QtWidgets.QLabel(collection_name)
        delete_button = self.create_action_button(
            "❌ Delete",
            lambda: self.delete_collection(collection_name, collection_widget),
        )
        view_button = self.create_action_button(
            "🔍 View",
            lambda: self.display_sets_from_collection(
                collection_name, collection_description
            ),
        )

        layout.addWidget(collection_name_label)
        layout.addWidget(view_button)
        layout.addWidget(delete_button)

        return collection_widget

    def delete_collection(self, name, widget):
        print(f"Deleting collection: {name}")
        Model.delete_collection(name)
        self.remove_widget(widget)

    def display_collected_set_edit_window(self, collected_set_info: CollectedSet):
        """Display the edit window for a collected set."""
        dialog = self.create_dialog("Edit Collection", 600, 400)
        layout = dialog.layout()

        set_name_label = QtWidgets.QLabel(
            f"Set Name: {collected_set_info.set_info.name}"
        )
        set_id_label = QtWidgets.QLabel(f"Set ID: {collected_set_info.set_info.id}")
        set_notes = QtWidgets.QTextEdit()
        set_notes.setPlainText(collected_set_info.notes)

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(
            lambda: self.update_collected_set(
                collected_set_info, set_notes.toPlainText(), dialog
            )
        )

        layout.addWidget(set_name_label)
        layout.addWidget(set_id_label)
        layout.addWidget(set_notes)
        layout.addWidget(save_button)

        dialog.exec()

    def update_collected_set(
        self, collected_set_info: CollectedSet, notes: str, dialog
    ):
        """Update the notes for a collected set."""
        print(f"Updating notes for set {collected_set_info.set_info.id}")
        print(f"Notes: {notes}")
        Model.update_collected_set_notes(
            collected_set_info.collection_name, collected_set_info.set_info.id, notes
        )
        dialog.close()

    def remove_from_collection(self, collection_name, set_id, widget):
        """Remove a set from a collection."""
        print(f"Removing set {set_id} from collection {collection_name}")
        self.remove_widget(widget)
        Model.remove_from_collection(collection_name, set_id)

    def display_collected_set_widget(self, collected_set_info: CollectedSet):
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
        set_name = QtWidgets.QLabel(f"📇 Name: {collected_set_info.set_info.name}")
        set_id = QtWidgets.QLabel(f"🪪 ID: {collected_set_info.set_info.id}")
        set_pieces = QtWidgets.QLabel(
            f"🧱 Bricks: {collected_set_info.set_info.pieces}"
        )

        set_url = QtWidgets.QLabel(
            f"🔗 <a href='{collected_set_info.set_info.brickset_url}'>Brickset link</a>"
        )
        set_url.setOpenExternalLinks(True)
        set_notes = QtWidgets.QLabel(f"📝 Notes: {collected_set_info.notes}")

        info_layout.addWidget(set_name)
        info_layout.addWidget(set_id)
        info_layout.addWidget(set_pieces)
        info_layout.addWidget(set_url)
        info_layout.addWidget(set_notes)

        self.style_card_info(info_layout)

        # Set image
        set_image = self.load_set_image(collected_set_info.set_info.image_url)
        image_layout.addWidget(set_image)

        # Action buttons
        wishlist_button = self.create_action_button(
            "❌ Remove",
            lambda: self.remove_from_collection(
                collected_set_info.collection_name,
                collected_set_info.set_info.id,
                set_widget,
            ),
        )
        add_to_collection_button = self.create_action_button(
            "✏️ Edit",
            lambda: self.display_collected_set_edit_window(collected_set_info),
        )

        button_layout.addWidget(add_to_collection_button)
        button_layout.addWidget(wishlist_button)

        return set_widget


if __name__ == "__main__":
    init_brickse()

    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
