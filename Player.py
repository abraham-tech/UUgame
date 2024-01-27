import random
from Piece import Piece

class Player:
    """
    Defines the Player class
    """

    def __init__(self, name, sign):
        self.name = name
        self.number_of_wins = 0
        self.number_of_losses = 0
        self.sign = sign
        self.color = None
        self.pieces = []
        for _ in range(0, 9):
            self.pieces.append(Piece(self, sign, sign))

    def __repr__(self):
        """
        Allows to get a string representation of the Player class.
        """
        return f"My name is {self.name}"

    def __eq__(self, other):
        """
        Enables comparing two Player objects using the "==" operator.

        Keyword arguments:
        other -- the object to compare with
        """
        if not isinstance(other, Player):
            return False
        return self.name == other.name

    def get_random_placable_piece(self):
        """
        Get a random piece which has not yet been placed on the board

        Returns:
        A random placable piece
        """
        return random.choice([p for p in self.pieces if (not p.on_board) and p.is_alive])
    
    def get_nr_unplaced_pieces(self):
        """
        Get the number of pieces the player has not yet placed on the board

        Returns:
        The number of pieces
        """
        return len([p for p in self.pieces if (not p.on_board) and p.is_alive])
