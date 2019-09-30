"""Error handling for the tilesets CLI"""


class TilesetsError(Exception):
    """Base Tilesets error
    Deriving errors from this base isolates module development
    problems from Python usage problems.
    """

    exit_code = 1

    def __init__(self, message):
        """Error constructor
        Parameters
        ----------
        message: str
            Error description
        """
        self.message = message


class TilesetNameError(TilesetsError):
    """Not a valid tileset id
    """
