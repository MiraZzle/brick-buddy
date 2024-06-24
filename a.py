import json
import brickse
from PyQt6 import QtWidgets, QtGui, QtCore
import urllib.request

from Models.data_model import Model, CollectedSet
from Utils.api_requests import get_themes, get_sets_from_theme, SetInfo
from Utils.api_setup import init_brickse


def create_nav_button(text: str, callback: callable) -> QtWidgets.QPushButton:
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
