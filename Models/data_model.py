import csv
import os
import urllib.request

from Utils.api_requests import SetInfo

DATA_DIRECTORY = "UserData"


class Model:
    """
    A class representing a data model for managing collections, sets, and wishlist items.
    """

    @staticmethod
    def create_collection(collection_name, collection_description):
        """
        Saves a new collection to the collections file.

        Args:
            collection_name (str): The name of the collection to be saved.
        """
        collections_file_path = f"./{DATA_DIRECTORY}/collections.csv"
        file_exists = os.path.isfile(collections_file_path)

        with open(collections_file_path, mode="a", newline="") as collections_file:
            collections_writer = csv.writer(
                collections_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            # Write header if file does not exist
            if not file_exists:
                collections_writer.writerow(["collection_name"])

        with open(collections_file_path, mode="r", newline="") as collections_file:
            collections_reader = csv.reader(collections_file)
            existing_collections = [row[0] for row in collections_reader if row]
            if collection_name in existing_collections:
                print("Collection already exists")
                return

        with open(collections_file_path, mode="a", newline="") as collections_file:
            collections_writer = csv.writer(
                collections_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            collections_writer.writerow([collection_name, collection_description])

    @staticmethod
    def save_collected_set(set_data: SetInfo, collection_name, notes):
        """
        Saves a collected set to the collection data file.

        Args:
            set_id (str): The ID of the set to be saved.
            collection_name (str): The name of the collection to which the set belongs.
            notes (str): Additional notes about the set.
        """
        collections_file_path = f"./{DATA_DIRECTORY}/collected_sets.csv"
        file_exists = os.path.isfile(collections_file_path)

        with open(collections_file_path, mode="r", newline="") as collection_data_file:
            collection_data_reader = csv.reader(collection_data_file)
            for row in collection_data_reader:
                if row and row[1] == set_data.id and row[0] == collection_name:
                    print(f"Set {set_data.id} already in collection {collection_name}")
                    return

        with open(collections_file_path, mode="a", newline="") as collection_data_file:
            collection_data_writer = csv.writer(
                collection_data_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            # Write header if file does not exist
            if not file_exists:
                # set_id,name,url,year,pieces,notes,collection_name
                collection_data_writer.writerow(
                    [
                        "collection_name",
                        "set_id",
                        "name",
                        "url",
                        "brickset_url",
                        "year",
                        "pieces",
                        "notes",
                    ]
                )

            collection_data_writer.writerow(
                [
                    collection_name,
                    set_data.id,
                    set_data.name,
                    set_data.image_url,
                    set_data.brickset_url,
                    set_data.year,
                    set_data.pieces,
                    notes,
                ]
            )

    @staticmethod
    def get_all_collections():
        """
        Retrieves all collection names.

        Returns:
            list: A list of collection names.
        """
        collections_file_path = f"./{DATA_DIRECTORY}/collections.csv"
        if not os.path.isfile(collections_file_path):
            return []

        with open(collections_file_path, mode="r") as collections_file:
            collections_reader = csv.reader(collections_file)
            next(collections_reader, None)  # Skip header
            return [row for row in collections_reader]

    @staticmethod
    def get_collection_data(collection_name):
        """
        Retrieves all sets in a specific collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            list: A list of sets in the collection.
        """
        collected_sets_file_path = f"./{DATA_DIRECTORY}/collected_sets.csv"
        if not os.path.isfile(collected_sets_file_path):
            return []

        with open(collected_sets_file_path, mode="r") as collection_data_file:
            collection_data_reader = csv.reader(collection_data_file)
            next(collection_data_reader, None)  # Skip header
            return [
                row
                for row in collection_data_reader
                if row and row[0] == collection_name
            ]

    @staticmethod
    def get_wishlist_data():
        """
        Retrieves all wishlist items.

        Returns:
            list: A list of wishlist items.
        """
        wishlist_file_path = f"./{DATA_DIRECTORY}/wishlist.csv"
        if not os.path.isfile(wishlist_file_path):
            return []

        with open(wishlist_file_path, mode="r") as wishlist_file:
            wishlist_reader = csv.reader(wishlist_file)
            next(wishlist_reader, None)  # Skip header
            return [row for row in wishlist_reader]

    @staticmethod
    def save_to_wishlist(set_data: SetInfo, notes):
        """
        Saves a set to the wishlist.

        Args:
            set_id (str): The ID of the set to be saved.
            notes (str): Additional notes about the set.
        """
        wishlist_file_path = f"./{DATA_DIRECTORY}/wishlist.csv"
        file_exists = os.path.isfile(wishlist_file_path)

        with open(wishlist_file_path, mode="r", newline="") as wishlist_file:
            wishlist_reader = csv.reader(wishlist_file)
            for row in wishlist_reader:
                if row and row[0] == str(set_data.id):
                    print(f"Set {set_data.id} already in wishlist")
                    return

        with open(wishlist_file_path, mode="a", newline="") as wishlist_file:
            wishlist_writer = csv.writer(
                wishlist_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            # Write header if file does not exist
            if not file_exists:
                # set_id,name,url,year,pieces,notes
                wishlist_writer.writerow(
                    ["set_id", "name", "url", "brickset_url", "year", "pieces", "notes"]
                )

            wishlist_writer.writerow(
                [
                    set_data.id,
                    set_data.name,
                    set_data.image_url,
                    set_data.brickset_url,
                    set_data.year,
                    set_data.pieces,
                    notes,
                ]
            )

    @staticmethod
    def remove_from_wishlist(set_id):
        wishlist_file_path = f"./{DATA_DIRECTORY}/wishlist.csv"
        wishlist_data = Model.get_wishlist_data()

        with open(wishlist_file_path, mode="w", newline="") as wishlist_file:
            wishlist_writer = csv.writer(
                wishlist_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            wishlist_writer.writerow(
                ["set_id", "name", "url", "brickset_url", "year", "pieces", "notes"]
            )

            for row in wishlist_data:
                if row[0] != set_id:
                    wishlist_writer.writerow(row)
