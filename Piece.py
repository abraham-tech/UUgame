class Piece:
    """
    Defines the Piece class
    """

    def __init__(self, player, color, symbol):
        self.belongs_to = player
        self.color = color
        self.symbol = symbol
        self.on_board = False
        self.is_alive = True
        self.is_secured = False
        self.position = None

    def __eq__(self, other):
        """
        Enables comparing two Piece objects using the "==" operator.

        Keyword arguments:
        other -- the object to compare with
        """
        if not isinstance(other, Piece):
            return False
        return self.position == other.position and self.belongs_to == other.belongs_to

    
  
