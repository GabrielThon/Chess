class Direction:
    def __init__(self, dcol: int, drow: int):
        self.dcol = dcol
        self.drow = drow

    def as_tuple(self) -> tuple[int, int]:
        return self.dcol, self.drow

    @classmethod
    def diagonals(cls) -> set["Direction"]:
        return {cls(1, 1), cls(1, -1), cls(-1, 1), cls(-1, -1)}

    @classmethod
    def straights(cls) -> set["Direction"]:
        return {cls(0, 1), cls(0, -1), cls(1, 0), cls(-1, 0)}

    @classmethod
    def knight_jumps(cls) -> set["Direction"]:
        return {cls(1, 2), cls(2, 1), cls(2, -1), cls(1, -2), cls(-1, -2), cls(-2, -1), cls(-2, 1), cls(-1, 2)}
