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

    sets = []
    set_names = []
    for set in raw_sets["sets"]:
        set_id = set["setID"]
        set_name = set["name"]
        set_img_url = set["image"]["imageURL"]
        year = set["year"]
        pieces = set["pieces"]

        set_info = SetInfo(set_id, set_name, set_img_url, year, pieces)

        sets.append(set_info)
        set_names.append(set_name)

    return sets


class SetInfo:
    def __init__(
        self, set_id: int, set_name: str, set_img_url: str, year: int, pieces: int
    ):
        self.set_id = set_id
        self.set_name = set_name
        self.set_img_url = set_img_url
        self.year = year
        self.pieces = pieces

    def __str__(self):
        return f"Set ID: {self.set_id}, Set Name: {self.set_name}, Year: {self.year}, Pieces: {self.pieces}, Image URL: {self.set_img_url}"
