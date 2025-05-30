class OutofBoundSquareError(Exception):
    """Exception raised when a square is not within the board"""
    def __init__(self, key):
        super().__init__(f"Square '{key}' is out of bounds.")
        self.key = key

class InvalidNumberOfKingsError(Exception):
    """Raised when the position doesn't contain 1 king of each color"""
    def __init__(self, nb_kings: dict[str, int]):
        super().__init__(f"Invalid board: must have exactly one white king and one black king., but found {nb_kings["white"]} white king(s) and {nb_kings["black"]} black king(s)")