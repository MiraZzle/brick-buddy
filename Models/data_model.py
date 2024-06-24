import csv
import os
from PyQt6.QtWidgets import QMessageBox
from Utils.api_requests import SetInfo
from Utils.message_handler import MessageBox

DATA_DIRECTORY = "UserData"
COLLECTIONS_FILE = os.path.join(DATA_DIRECTORY, "collections.csv")
COLLECTED_SETS_FILE = os.path.join(DATA_DIRECTORY, "collected_sets.csv")
WISHLIST_FILE = os.path.join(DATA_DIRECTORY, "wishlist.csv")

class CollectedSet:
    """
    A class representing a collected set.
    """

    def __init__(self, set_info, collection_name, notes):
        self.set_info = set_info
        self.collection_name = collection_name
        self.notes = notes

class Model:
    @staticmethod
    def create_collection(collection_name, collection_description):
        """
        Saves a new collection to the collections file.

        Args:
            collection_name (str): The name of the collection to be saved.
            collection_description (str): The description of the collection.
        """
        if Model.collection_exists(collection_name):
            MessageBox.show_warning("Collection already exists")
            return

        Model.append_to_csv(
            COLLECTIONS_FILE,
            ["collection_name", "collection_description"],
            [collection_name, collection_description],
        )

    @staticmethod
    def save_collected_set(set_data: SetInfo, collection_name, notes):
        """
        Saves a collected set to the collection data file.

        Args:
            set_data (SetInfo): The set information to be saved.
            collection_name (str): The name of the collection to which the set belongs.
            notes (str): Additional notes about the set.
        """
        if Model.set_in_collection(str(set_data.id), collection_name):
            MessageBox.show_warning(
                f"Set {set_data.id} already in collection {collection_name}"
            )
            return

        Model.append_to_csv(
            COLLECTED_SETS_FILE,
            [
                "collection_name",
                "set_id",
                "name",
                "url",
                "brickset_url",
                "year",
                "pieces",
                "notes",
            ],
            [
                collection_name,
                set_data.id,
                set_data.name,
                set_data.image_url,
                set_data.brickset_url,
                set_data.year,
                set_data.pieces,
                notes,
            ],
        )

    @staticmethod
    def remove_from_collection(collection_name, set_id):
        """
        Removes a set from a specific collection.

        Args:
            collection_name (str): The name of the collection.
            set_id (str): The ID of the set to be removed.
        """
        collection_data = Model.get_collection_data(collection_name, as_string=True)
        collection_data = [row for row in collection_data if row[1] != set_id]

        Model.write_to_csv(
            COLLECTED_SETS_FILE,
            [
                "collection_name",
                "set_id",
                "name",
                "url",
                "brickset_url",
                "year",
                "pieces",
                "notes",
            ],
            collection_data,
        )

    @staticmethod
    def get_all_collections() -> list:
        """
        Retrieves all collection names.

        Returns:
            list: A list of collection names.
        """
        return Model.read_csv(COLLECTIONS_FILE, skip_header=True)

    @staticmethod
    def update_wishlisted_set_notes(set_id, notes) -> None:
        """
        Updates notes for a specific set in the wishlist.

        Args:
            set_id (str): The ID of the set.
            notes (str): New notes for the set.
        """
        wishlist_data = Model.get_wishlist_data()
        updated_data = [
            (
                [row[0], row[1], row[2], row[3], row[4], row[5], notes]
                if row[0] == set_id
                else row
            )
            for row in wishlist_data
        ]

        Model.write_to_csv(
            WISHLIST_FILE,
            ["set_id", "name", "url", "brickset_url", "year", "pieces", "notes"],
            updated_data,
        )

    @staticmethod
    def update_collected_set_notes(collection_name, set_id, notes) -> None:
        """
        Updates notes for a specific set in a collection.

        Args:
            collection_name (str): The name of the collection.
            set_id (str): The ID of the set.
            notes (str): New notes for the set.
        """
        collection_data = Model.get_collection_data(collection_name, as_string=True)
        updated_data = [
            (
                [row[0], row[1], row[2], row[3], row[4], row[5], row[6], notes]
                if row[1] == set_id
                else row
            )
            for row in collection_data
        ]

        Model.write_to_csv(
            COLLECTED_SETS_FILE,
            [
                "collection_name",
                "set_id",
                "name",
                "url",
                "brickset_url",
                "year",
                "pieces",
                "notes",
            ],
            updated_data,
        )

    @staticmethod
    def get_collection_data(collection_name, as_string=False) -> list:
        """
        Retrieves all sets in a specific collection.

        Args:
            collection_name (str): The name of the collection.
            as_string (bool): Whether to return data as strings or CollectedSet objects.

        Returns:
            list: A list of sets in the collection.
        """
        collection_data = Model.read_csv(COLLECTED_SETS_FILE, skip_header=True)
        collection_data = [row for row in collection_data if row[0] == collection_name]
        if as_string:
            return collection_data
        return [
            CollectedSet(SetInfo(*row[1:7]), row[0], row[7]) for row in collection_data
        ]

    @staticmethod
    def get_all_collected_sets() -> list:
        """
        Retrieves all collected sets.

        Returns:
            list: A list of collected sets.
        """
        return Model.read_csv(COLLECTED_SETS_FILE, skip_header=True)

    @staticmethod
    def delete_collection(collection_name: str) -> None:
        """
        Deletes a collection from the collections file.
        """
        collections_data = Model.get_all_collections()
        collections_data = [
            row for row in collections_data if row[0] != collection_name
        ]

        Model.write_to_csv(
            COLLECTIONS_FILE,
            ["collection_name", "collection_description"],
            collections_data,
        )

        all_collected_sets = Model.get_all_collected_sets()
        all_collected_sets = [
            row for row in all_collected_sets if row[0] != collection_name
        ]

        Model.write_to_csv(
            COLLECTED_SETS_FILE,
            [
                "collection_name",
                "set_id",
                "name",
                "url",
                "brickset_url",
                "year",
                "pieces",
                "notes",
            ],
            all_collected_sets,
        )

    @staticmethod
    def get_wishlist_data() -> list:
        """
        Retrieves all wishlist items.

        Returns:
            list: A list of wishlist items.
        """
        return Model.read_csv(WISHLIST_FILE, skip_header=True)

    @staticmethod
    def save_to_wishlist(set_data: SetInfo, notes: str) -> None:
        """
        Saves a set to the wishlist.

        Args:
            set_data (SetInfo): The set information to be saved.
            notes (str): Additional notes about the set.
        """
        if Model.set_in_wishlist(str(set_data.id)):
            MessageBox.show_warning(f"Set {set_data.id} already in wishlist")
            return

        Model.append_to_csv(
            WISHLIST_FILE,
            ["set_id", "name", "url", "brickset_url", "year", "pieces", "notes"],
            [
                set_data.id,
                set_data.name,
                set_data.image_url,
                set_data.brickset_url,
                set_data.year,
                set_data.pieces,
                notes,
            ],
        )

    @staticmethod
    def remove_from_wishlist(set_id: str) -> None:
        """
        Removes a set from the wishlist.

        Args:
            set_id (str): The ID of the set to be removed.
        """
        wishlist_data = Model.get_wishlist_data()
        wishlist_data = [row for row in wishlist_data if row[0] != set_id]

        Model.write_to_csv(
            WISHLIST_FILE,
            ["set_id", "name", "url", "brickset_url", "year", "pieces", "notes"],
            wishlist_data,
        )

    @staticmethod
    def collection_exists(collection_name: str) -> bool:
        """
        Checks if a collection exists.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        collections = Model.get_all_collections()
        return any(row[0] == collection_name for row in collections)

    @staticmethod
    def set_in_collection(set_id: str, collection_name: str) -> bool:
        """
        Checks if a set is already in a collection.

        Args:
            set_id (str): The ID of the set.
            collection_name (str): The name of the collection.

        Returns:
            bool: True if the set is in the collection, False otherwise.
        """
        collection_data = Model.get_collection_data(collection_name, as_string=True)
        return any(row[1] == set_id for row in collection_data)

    @staticmethod
    def set_in_wishlist(set_id: str) -> bool:
        """
        Checks if a set is already in the wishlist.

        Args:
            set_id (str): The ID of the set.

        Returns:
            bool: True if the set is in the wishlist, False otherwise.
        """
        wishlist_data = Model.get_wishlist_data()
        return any(row[0] == set_id for row in wishlist_data)

    @staticmethod
    def append_to_csv(file_path: str, headers: list, row: list) -> None:
        """
        Appends a row to a CSV file, creating the file and adding headers if it doesn't exist.

        Args:
            file_path (str): The path to the CSV file.
            headers (list): The headers for the CSV file.
            row (list): The row to append to the CSV file.
        """
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)

    @staticmethod
    def write_to_csv(file_path: str, headers: list, data: list) -> None:
        """
        Writes data to a CSV file, including headers.

        Args:
            file_path (str): The path to the CSV file.
            headers (list): The headers for the CSV file.
            data (list): The data to write to the CSV file.
        """
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(headers)
            writer.writerows(data)

    @staticmethod
    def read_csv(file_path: str, skip_header: bool = False) -> list:
        """
        Reads data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.
            skip_header (bool): Whether to skip the header row.

        Returns:
            list: The data read from the CSV file.
        """
        if not os.path.isfile(file_path):
            return []

        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            if skip_header:
                next(reader, None)
            return [row for row in reader]
