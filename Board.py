from Singleton import Singleton
from BoardPosition import BoardPosition
from Piece import Piece
from Player import Player
from communicationPlatform.ui.text_ui import bcolors

class Board():
    """
    Defines the Board class
    """
    turn_over = False

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1.color = bcolors.OKGREEN
        self.player_2.color = bcolors.ERROR
        self.turn = player_1
        self.turn_counter = 1
        self.board_positions = None


    def init_board_pos(self):
        """
        Initiates the BoardPositions
        """
        adjacency = [[1,9],[0,4,2],[1,14],[4,10],[3,5,1,7],[4,13],[11,7],[6,4,8],[7,12],[0,10,21],[9,3,11,18],[10,6,15],[8,13,17],[12,5,14,20],[13,2,23],[11,16], [15,17,19], [16,12],[10,19],[18,16,20,22],[19,13],[22,9],[21,19,23],[22,14]]
        positions= [[0,0], [3,0], [6,0], [1,1], [3,1], [5,1], [2,2], [3,2], [4,2],[0,3], [1,3], [2,3], [4,3], [5,3], [6,3], [2,4], [3,4], [4,4], [1,5], [3,5], [5,5], [0,6], [3,6], [6,6]]

        board_positions = []
        for x in range(24):
            bp = BoardPosition(positions[x][0],positions[x][1], adjacency[x])
            board_positions.append(bp)

        self.board_positions = board_positions


    def draw_board(self):
        """
        Draws the game Board in the terminal
        """
        board_pos = self.board_positions

        print(
            f"{board_pos[0].get_piece_symbol()}-A----------------------" + f"{board_pos[1].get_piece_symbol()}-B----------------------" + f"{board_pos[2].get_piece_symbol()}-C")
        print("|                          |                       |")
        print(
            "|       " + f"{board_pos[3].get_piece_symbol()}-D--------------" + f"{board_pos[4].get_piece_symbol()}-E--------------" + f"{board_pos[5].get_piece_symbol()}-F      |")
        print("|       |                  |               |       |")
        print("|       |                  |               |       |")
        print(
            "|       |        " + f"{board_pos[6].get_piece_symbol()}-G-----" + f"{board_pos[7].get_piece_symbol()}-H-----" + f"{board_pos[8].get_piece_symbol()}-I       |       |")
        print("|       |         |                |       |       |")
        print("|       |         |                |       |       |")
        print(
            f"{board_pos[9].get_piece_symbol()}-J----" + f"{board_pos[10].get_piece_symbol()}-K-------" + f"{board_pos[11].get_piece_symbol()}-L             " + f" {board_pos[12].get_piece_symbol()}-M-----" + f"{board_pos[13].get_piece_symbol()}-N----" + f"{board_pos[14].get_piece_symbol()}-O")
        print("|       |         |                |       |       |")
        print("|       |         |                |       |       |")
        print(
            "|       |        " + f"{board_pos[15].get_piece_symbol()}-P-----" + f"{board_pos[16].get_piece_symbol()}-Q-----" + f"{board_pos[17].get_piece_symbol()}-R       |       |")
        print("|       |                  |               |       |")
        print("|       |                  |               |       |")
        print(
            f"|       " + f"{board_pos[18].get_piece_symbol()}-S--------------" + f"{board_pos[19].get_piece_symbol()}-T--------------" + f"{board_pos[20].get_piece_symbol()}-U      |")
        print("|                          |                       |")
        print("|                          |                       |")
        print(f"{board_pos[21].get_piece_symbol()}-V----------------------" + f"{board_pos[22].get_piece_symbol()}-W----------------------" + f"{board_pos[23].get_piece_symbol()}-Z")


    def add_piece(self, piece, position):
        """
        Adds a piece to the Board

        Keyword arguments:
        piece    -- the piece object to add to the board
        position -- the board position ('a' to 'z' except 'x' and 'y') to add a piece to

        !!! Throws exception on incorrect input !!!
        """
        bp = self.get_board_pos(position)

        if bp.piece:
            raise Warning("Invalid board position")
        elif piece.on_board or not piece.is_alive:
            raise Warning("Invalid piece")
        else:
            piece.position = bp
            piece.on_board = True
            bp.piece = piece


    def reset_board(self):
        """
        Removes all pieces from the board, gives the players nine new pieces each,
        resets the turn counter and resets the starting player to player 1
        """
        self.turn_counter = 1
        self.turn = self.player_1

        player1_piece_color = self.player_1.pieces[0].color
        player1_piece_symbol = self.player_1.pieces[0].symbol
        self.player_1.pieces = []
        for _ in range(0, 9):
            self.player_1.pieces.append(Piece(self.player_1.name, player1_piece_color, player1_piece_symbol))

        player2_piece_color = self.player_2.pieces[0].color
        player2_piece_symbol = self.player_2.pieces[0].symbol
        self.player_2.pieces = []
        for _ in range(0, 9):
            self.player_2.pieces.append(Piece(self.player_2.name, player2_piece_color, player2_piece_symbol))

        self.init_board_pos()


    def check_if_secured(self, piece, nr_in_line=3):
        """
        Checks if a piece is secured based on its neighbors (NOT based on piece.is_secured)

        Keyword arguments:
        piece -- the piece object you are checking the security of
        nr_in_line -- the nr of pieces that should be in a line, default is 3

        Returns:
        Whether the piece is secure or not
        """
        if not piece or not piece.position:
            return False
        if (self.pieces_in_line("y", piece) == nr_in_line):
            return True
        if (self.pieces_in_line("x", piece) == nr_in_line):
            return True
        return False


    def pieces_in_line(self, line_axis, piece):
        """
        Count the number of pieces in a row along a line on the board,
        taking into account the piece you are checking the security of

        Keyword arguments:
        line_axis -- the axis the line must be formed along, can be either 'x' or 'y'
        piece -- the piece object you are checking the security of

        Returns:
        The number of pieces in a row
        """

        player = piece.belongs_to
        number_of_pieces_in_line = 0
        current_position = piece.position
        investigations = 0

        while current_position.piece and current_position.piece.belongs_to == player:
            number_of_pieces_in_line += 1
            # Create a list of all adjacent board positions which are viable for forming
            # a secure line, i.e. they all contain a piece of the current player
            viable_adjacent_bps = []
            for bp_index in current_position.adjacent:
                bp = self.board_positions[bp_index]
                if line_axis == "x":
                    bp_correct_axis = bp.y == piece.position.y
                elif line_axis == "y":
                    bp_correct_axis = bp.x == piece.position.x
                if bp.piece and bp.piece.belongs_to == player and bp_correct_axis:
                    viable_adjacent_bps.append(bp)
            # If this list if empty it means a line cannot be formed
            if not viable_adjacent_bps:
                break
            # If this list has two elements it means both the neighbours of the selected
            # piece are the current player's pieces
            if len(viable_adjacent_bps) == 2:
                return 3
            # If this list only has one element we must investigate that element
            # to find out if there is a third piece which would form a secure line
            # We only need to do this once since lines cannot be longer than three pieces
            elif investigations == 0:
                current_position = viable_adjacent_bps[0]
                investigations += 1
            # If we have investigated once but our list still only contains one element,
            # it means our line is only two pieces long
            else:
                break

        return number_of_pieces_in_line


    def update_secured_pieces(self):
        """
        Makes sure all pieces has their is_secured bool correctly set
        """
        for piece in self.player_1.pieces:
            if self.check_if_secured(piece):
                piece.is_secured = True
            else:
                piece.is_secured = False

        for piece in self.player_2.pieces:
            if self.check_if_secured(piece):
                piece.is_secured = True
            else:
                piece.is_secured = False

        # Special condition check
        secured_piece = []
        for piece in self.player_1.pieces:
            if piece.on_board:
                secured_piece.append(piece.is_secured)
        if all(secured_piece):
            for piece in self.player_1.pieces:
                piece.is_secured = False

        # Special condition check
        secured_piece = []
        for piece in self.player_2.pieces:
            if piece.on_board:
                secured_piece.append(piece.is_secured)
        if all(secured_piece):
            for piece in self.player_2.pieces:
                piece.is_secured = False


    def remove_piece(self, position):
        """
        Remove a Piece from the Board

        Keyword arguments:
        position -- the board position ('a' to 'z' except 'x' and 'y') to remove a piece from

        !!! Throws exception on incorrect input !!!
        """
        bp = self.get_board_pos(position)

        if not bp.piece:
            raise Warning("That board position has no piece to remove")

        if bp.piece.belongs_to == self.turn:
            raise Warning("You cannot remove your own pieces")

        if (not bp.piece.is_secured):
            bp.piece.on_board = False
            bp.piece.is_alive = False
            bp.piece.is_secured = False
            bp.piece = None
            return
        raise Warning("Incorrect position input or piece is secured")


    def next_turn(self):
        """
        Changes active player and increases the turn count by 1
        """
        self.turn_counter += 1
        if self.turn == self.player_1:
            self.turn = self.player_2
        else:
            self.turn = self.player_1


    def move_piece(self, player, piece, position):
        """
        Move a player's piece on the board to a new position

        Keyword arguments:
        player -- the player object who's piece we are moving
        piece  -- the piece object to move
        position -- the board position ('a' to 'z' except 'x' and 'y') to move the piece to

        !!! Throws exception on incorrect input !!!
        """
        # Check if piece belongs to player
        if (piece not in player.pieces):
            raise Warning("That is not your piece!")

        # If position is valid and piece belongs to the player
        # Check if piece is neighbour with the position
        new_position = self.get_board_pos(position)
        piece_bp = piece.position
        for adj in piece_bp.adjacent:
            if self.board_positions[adj] is new_position and not new_position.piece:
                piece_bp.piece = None
                new_position.piece = piece
                piece.position = new_position
                return
        raise Warning("You cannot do that")


    def get_board_pos(self, position):
        """
        Converts a board position letter to the correct board position object

        Keyword arguments:
        position -- the board position ('a' to 'z' except 'x' and 'y') to convert

        Returns:
        A board position object

        !!! Throws exception on incorrect input !!!
        """
        positions = "abcdefghijklmnopqrstuvwz"
        # Check if position is valid
        if (position.lower() not in positions):
            raise Warning("That is not a valid position")
        index = positions.index(position)
        return self.board_positions[index]


    def get_position_letter(self, position):
        """
        Converts a board position object to the correct board position letter
        The opposite of get_board_pos()

        Keyword arguments:
        position -- A board position object

        Returns:
        position -- the corresponding board position letter ('a' to 'z' except 'x' and 'y')
        """
        positions = "abcdefghijklmnopqrstuvwz"
        index = self.board_positions.index(position)
        return positions[index]


    def current_player_won(self):
        """
        Check if the player who's turn it is has won the match

        Returns:
        Whether or not the player who's turn it is has won the match
        """
        if self.turn == self.player_1:
            opponent = self.player_2
        else:
            opponent = self.player_1

        pieces_on_board = []
        for piece in opponent.pieces:
            if piece.on_board:
                pieces_on_board.append(piece)

        # If opponent has 2 pieces left the current player wins
        if len(pieces_on_board) == 2:
            return True

        # If opponent cannot move any piece the current player wins
        return len(self.get_movable_pieces(opponent)) == 0


    def get_empty_positions(self):
        """
        Look for valid positions to add a piece to.

        Returns:
        A list with board positions where one can add a piece.
        """
        return [bp for bp in self.board_positions if bp.piece == None]


    def get_movable_pieces(self, player=None):
        """
        Look for movable pieces.

        Keyword arguments:
        player -- the Player object to fetch movable pieces for, default is the player who's turn it currently is (symbolized by None)

        Returns:
        A list with movable pieces.
        """
        if not player or not isinstance(player, Player):
            player = self.turn
        movable_pieces = []
        for piece in player.pieces:
            if piece.on_board:
                for adj in piece.position.adjacent:
                    if self.board_positions[adj].piece == None:
                        movable_pieces.append(piece)
                        break
        return movable_pieces


    def get_removable_pieces(self):
        """
        Look for removable pieces.

        Returns:
        A list with removable pieces from the opponent.
        """
        if self.turn == self.player_1:
            player = self.player_2
        else:
            player = self.player_1

        return [p for p in player.pieces if not p.is_secured and p.on_board and p.is_alive]
