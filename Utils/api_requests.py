import brickse
import json


def get_themes() -> list[str]:
    """
    Get a list of all LEGO themes names.
    """

    raw_themes = json.loads(brickse.lego.get_themes().read())

    theme_names = []
    for theme in raw_themes["themes"]:
        theme_name = theme["theme"]
        theme_names.append(theme_name)

    return theme_names


def get_sets_from_theme(theme: str) -> list[str]:
    """
    Get a list of all LEGO set names from a specific theme.
    """

    raw_sets = json.loads(brickse.lego.get_sets(theme=theme).read())

    # print(raw_sets)

    sets = []
    placeholder_sets = []

    for _ in range(10):
        placeholder_sets.append(
            SetInfo(
                69,
                "Amazing Set",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/1024px-LEGO_logo.svg.png",
                "google.com",
                2021,
                100,
            ),
        )

    try:
        # raise KeyError("Test error")

        for set in raw_sets["sets"]:
            set_id = set["setID"]
            set_name = set["name"]

            try:
                year = set["year"]
            except KeyError:
                year = None

            try:
                pieces = set["pieces"]
            except KeyError:
                pieces = None

            try:
                brickset_url = set["bricksetURL"]
            except KeyError:
                brickset_url = None

            # some sets don't have an image - use a default image in that case
            try:
                set_img_url = set["image"]["imageURL"]
            except KeyError:
                set_img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/1024px-LEGO_logo.svg.png"

            set_info = SetInfo(
                set_id, set_name, set_img_url, brickset_url, year, pieces
            )

            sets.append(set_info)
    except KeyError as e:
        print("Sets not found")
        print(e)
        return placeholder_sets

    return sets


class SetInfo:

    def __init__(
        self,
        set_id: int,
        set_name: str,
        set_img_url: str,
        brickset_url: str,
        year: int,
        pieces: int,
    ):
        self.id = set_id
        self.name = set_name
        self.image_url = set_img_url
        self.brickset_url = brickset_url
        self.year = year
        self.pieces = pieces

    def __str__(self):
        return f"Set ID: {self.id}, Set Name: {self.name}, Year: {self.year}, Pieces: {self.pieces}, Image URL: {self.image_url}"
