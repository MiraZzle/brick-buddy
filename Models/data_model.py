import csv
import os

DATA_DIRECTORY = "UserData"


class Model:
    """
    A class representing a data model for managing collections, sets, and wishlist items.
    """

    @staticmethod
    def save_new_collection(collection_name):
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
            collections_writer.writerow([collection_name])

    @staticmethod
    def save_collected_set(set_id, collection_name, notes):
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
                if row and row[0] == set_id and row[1] == collection_name:
                    print(f"Set {set_id} already in collection {collection_name}")
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
                collection_data_writer.writerow(["set_id", "collection_name", "notes"])

            collection_data_writer.writerow([set_id, collection_name, notes])

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
            return [row[0] for row in collections_reader if row]

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
            return [row for row in wishlist_reader if row]

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
                if row and row[1] == collection_name
            ]

    @staticmethod
    def save_to_wishlist(set_id, notes):
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
                if row and row[0] == str(set_id):
                    print(f"Set {set_id} already in wishlist")
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
                wishlist_writer.writerow(["setid", "notes"])

            wishlist_writer.writerow([set_id, notes])

    @staticmethod
    def cache_set_data(set_data):
        """
        Caches set data.

        Args:
            set_data (object): The set data to be cached.
        """
        cached_sets_file_path = f"./{DATA_DIRECTORY}/cached_sets.csv"
        file_exists = os.path.isfile(cached_sets_file_path)

        with open(cached_sets_file_path, mode="r", newline="") as set_data_file:
            set_data_reader = csv.reader(set_data_file)
            for row in set_data_reader:
                if row and row[0] == set_data.set_id:
                    print(f"Set {set_data.set_id} already cached")
                    return

        with open(cached_sets_file_path, mode="a", newline="") as set_data_file:
            set_data_writer = csv.writer(
                set_data_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            # Write header if file does not exist
            if not file_exists:
                set_data_writer.writerow(["set_id", "name", "url", "year", "pieces"])

            set_data_writer.writerow(
                [
                    set_data.set_id,
                    set_data.set_name,
                    set_data.set_img_url,
                    set_data.year,
                    set_data.pieces,
                ]
            )
