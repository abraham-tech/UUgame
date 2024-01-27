from communicationPlatform.ui.text_ui import bcolors

class BoardPosition:
    """
    Defines the BoardPosition Class
    """

    def __init__(self, x, y, adjacent, piece=None):
        self.x = x
        self.y = y
        self.adjacent = adjacent
        self.piece = piece

    def __eq__(self, other):
        """
        Enables comparing two BoardPosition objects using the "==" operator.

        Keyword arguments:
        other -- the object to compare with
        """
        if not isinstance(other, BoardPosition):
            return False
        return self.x == other.x and self.y == other.y

    def get_piece_symbol(self):
        """
        Get the symbol of the piece on the current board position

        Returns:
        The piece symbol
        """
        if self.piece == None:
            return "X"
        return f"{bcolors.BOLD}{self.piece.belongs_to.color}{self.piece.symbol}{bcolors.ENDC}"
