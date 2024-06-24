from PyQt6.QtWidgets import QMessageBox


class MessageBox:
    @staticmethod
    def show_warning(message: str):
        """
        Display a warning message using PyQt6.

        Args:
            message (str): The message to display.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Warning")
        msg_box.exec()

    @staticmethod
    def show_info(message: str):
        """
        Display an information message using PyQt6.

        Args:
            message (str): The message to display.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Information")
        msg_box.exec()
