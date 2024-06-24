import brickse
import json


def get_themes() -> list[str]:
    """
    Get a list of all LEGO themes names.
    """
    raw_themes = json.loads(brickse.lego.get_themes().read())
    return [theme["theme"] for theme in raw_themes["themes"]]


def get_sets_from_theme(theme: str) -> list[str]:
    """
    Get a list of all LEGO set names from a specific theme.

    Args:
        theme (str): The LEGO theme name.
    """
    raw_sets = json.loads(brickse.lego.get_sets(theme=theme).read())
    print("API called")

    sets = []
    default_img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/LEGO_logo.svg/1024px-LEGO_logo.svg.png"

    for set in raw_sets["sets"]:
        set_id = set.get("setID")
        set_name = set.get("name")
        year = set.get("year")
        pieces = set.get("pieces")
        brickset_url = set.get("bricksetURL")
        set_img_url = set.get("image", {}).get("imageURL", default_img_url)

        set_info = SetInfo(set_id, set_name, set_img_url, brickset_url, year, pieces)
        sets.append(set_info)

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
