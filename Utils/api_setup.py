import brickse


def read_key() -> str | None:
    with open("./brickset_api_key.txt", "r") as f:
        return f.read().strip()


def init_brickse() -> None:
    brickse.init(read_key())
