class OutofBoundSquareError(Exception):
    """Exception raised when a square is not within the board"""
    def __init__(self, key):
        super().__init__(f"Square '{key}' is out of bounds.")
        self.key = key