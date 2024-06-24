import brickse

def read_key() -> str | None:
    """Read the Brickset API key from a file."""
    with open("./brickset_api_key.txt", "r") as f:
        return f.read().strip()

def init_brickse() -> None:
    """Initialize the Brickse API with user key."""
    brickse.init(read_key())
