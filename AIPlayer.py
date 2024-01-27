import random
from Piece import Piece
from Player import Player
import random

class AIPlayer(Player):
    """
    Defines the AIPlayer class
    """


    def __init__(self, name, sign, difficulty):
        Player.__init__(self, name, sign)
        if difficulty < 2:
            self.difficulty = 1
        elif difficulty > 2:
            self.difficulty = 3
        else:
            self.difficulty = 2


    def _get_random_move(self, board):
        """
        Get a random move for the current player

        Keyword arguments:
        board -- the Board object

        Returns:
        A tuple with the Piece to move and the BoardPosition to move to
        """
        movable_pieces = board.get_movable_pieces()
        piece_to_move = random.choice(movable_pieces)
        adjacent = piece_to_move.position.adjacent
        destinations = random.sample(adjacent, k=len(adjacent))
        index = 0
        destination = board.board_positions[destinations[index]]
        while destination.piece:
            index += 1
            destination = board.board_positions[destinations[index]]
        return (piece_to_move, destination)


    def get_optimal_add_position(self, board):
        """
        Difficulty 1: Get a random position to add a piece to
        Difficulty 2:
            1. Get a random position which will result in a triplet after a piece is added
            2. If not possible; Get a random position to add a piece to
        Difficulty 3:
            1. Get a random position which will result in a triplet *and* block the opponent after a piece is added
            2. If not possible; Get a random position which will only result in a triplet after a piece is added
            3. If not possible; Get a random position which will only block the opponent after a piece is added
            4. If not possible; Get a random position which will result in a line of two pieces after a piece is added
            5. If not possible; Get a random position to add a piece to

        Keyword arguments:
        board -- the Board object

        Returns:
        An optimal BoardPosition to add a new piece on based on difficulty
        """
        if self.difficulty == 1:
            return random.choice(board.get_empty_positions())
        elif self.difficulty == 2:
            optimal_add_positions = self._get_optimal_add_positions(board)
            if not optimal_add_positions:
                return random.choice(board.get_empty_positions())
            else:
                return random.choice(optimal_add_positions)
        else:
            optimal_add_positions = self._get_optimal_add_positions(board, block=True)
            if not optimal_add_positions:
                optimal_add_positions = self._get_optimal_add_positions(board)
                if not optimal_add_positions:
                    optimal_add_positions = self._get_optimal_add_positions(board, nr_in_line=1, block=True)
                    if not optimal_add_positions:
                        optimal_add_positions = self._get_optimal_add_positions(board, nr_in_line=2)
                        if not optimal_add_positions:
                            return random.choice(board.get_empty_positions())
            return random.choice(optimal_add_positions)

    
    def _get_optimal_add_positions(self, board, nr_in_line=3, block=False, player=None):
        """
        Check if optimal add positions exist based on the line length you want to form 
        and if you want to block the opponent at the same time

        Keyword arguments:
        board -- the Board object
        nr_in_line -- the line formed after adding a piece should be of this length, default 3
        block -- whether or not to only allow positions that will also block the opponent, default False
        player -- which Player to check optimal add positions for, default is the Player who's turn it currently is (symbolized by None)
        
        Returns:
        A list of optimal add BoardPosition objects or None if no such positions exist
        """
        if not player or not isinstance(player, Player):
            player = board.turn
    
        if player == board.player_1:
            opponent = board.player_2
        else:
            opponent = board.player_1

        if block:
            opponent_optimal_add_positions = self._get_optimal_add_positions(board, player=opponent)
            if not opponent_optimal_add_positions:
                return None

        empty_positions = board.get_empty_positions()
        optimal_add_positions = []

        for bp in empty_positions:
            temp_piece = Piece(player, "@", "@")
            bp_letter = board.get_position_letter(bp)
            board.add_piece(temp_piece, bp_letter)
            if board.check_if_secured(temp_piece, nr_in_line):
                if block:
                    if bp in opponent_optimal_add_positions:
                        optimal_add_positions.append(bp)
                else:
                    optimal_add_positions.append(bp)
            bp.piece = None 

        if len(optimal_add_positions) == 0:
            return None
        else:
            return optimal_add_positions


    def get_optimal_move(self, board):
        """
        Difficulty 1: Get a random piece to move and a random adjacent position to move it to
        Difficulty 2:
            1. Get a random piece to move which will result in a triplet when moved correctly
            2. If not possible; Get a random piece to move and a random adjacent position to move it to
        Difficulty 3:
            1. Get a random piece to move which will result in a triplet when moved to the correct position
            2. If not possible; Get a random piece to move which will block the opponent when moved correctly
            3. If not possible; Get a random piece to move which will result in a line of two pieces when moved correctly
            4. If not possible; Get a random piece to move and a random adjacent position to move it to

        Keyword arguments:
        board -- the Board object

        Returns:
        A tuple with the Piece to move and the optimal BoardPosition to move to
        """        
        if self.difficulty == 1:
            return self._get_random_move(board)
        elif self.difficulty == 2:
            optimal_moves = self._get_optimal_moves(board)
            if not optimal_moves:
                return self._get_random_move(board)
            else:
                return random.choice(optimal_moves)
        else:
            optimal_moves = self._get_optimal_moves(board)
            if not optimal_moves:
                optimal_moves = self._get_optimal_moves(board, block=True)
                if not optimal_moves:
                    optimal_moves = self._get_optimal_moves(board, nr_in_line=2)
                    if not optimal_moves:
                        return self._get_random_move(board)
            return random.choice(optimal_moves)


    def _get_optimal_moves(self, board, nr_in_line=3, block=False, player=None):
        """
        Check if optimal moves exist based on the line length you want to form
        and if you want to block the opponent at the same time

        Keyword arguments:
        board -- the Board object
        nr_in_line -- the line formed after moving a piece should be of this length, default 3
        block -- whether or not to only allow positions that will also block the opponent, default False
        player -- which Player to check optimal moves for, default is the Player who's turn it currently is (symbolized by None)
        
        Returns:
        A list of optimal moves (Piece, BoardPosition) or None if no such moves exist
        """
        default_player = True

        if not player or not isinstance(player, Player):
            player = board.turn
        else:
            default_player = False

        if player == board.player_1:
            opponent = board.player_2
        else:
            opponent = board.player_1

        if block:
            opponent_optimal_add_positions = self._get_optimal_add_positions(board, player=opponent)
            if not opponent_optimal_add_positions:
                return None

        movable_pieces = board.get_movable_pieces(player)
        optimal_moves = []
        all_positions = "abcdefghijklmnopqrstuvwz"

        # We cannot move opponent's pieces so we must assume they are the current player's pieces
        # This is reverted after the search is complete
        if not default_player:
            for p in movable_pieces:
                self.pieces.append(p)

        for p in movable_pieces:
            origin = p.position
            for position_index in origin.adjacent:
                position = board.get_board_pos(all_positions[position_index])
                if not position.piece:
                    board.move_piece(self, p, board.get_position_letter(position))
                    if block:
                        if position in opponent_optimal_add_positions:
                            optimal_moves.append((p, position))
                    else:
                        if board.check_if_secured(p, nr_in_line):
                            if nr_in_line <= 2:
                                if not p.is_secured:
                                    optimal_moves.append((p, position))
                            else:
                                optimal_moves.append((p, position))
                    board.move_piece(self, p, board.get_position_letter(origin))
        
        if not default_player:
            for p in movable_pieces:
                self.pieces.remove(p)

        if len(optimal_moves) == 0:
            return None
        else:
            return optimal_moves

    
    def get_optimal_remove(self, board):
        """
        Difficulty 1: Select a random removable piece from the opponent
        Difficulty 2:   
            1. Randomly select a piece the opponent can move to form a triplet, 
            2. If not possible; Select a random removable piece from the opponent
        Difficulty 3: 
            1. Randomly select a piece the opponent can move to form a triplet,  
            2. If not possible; Randomly select a piece from the opponent that 
                appears in a line of two, 
            3. If not possible; Select a random removable piece from the opponent

        Keyword arguments:
        board -- the Board object

        Returns:
        The optimal Piece to remove from the opponent
        """
        removable_pieces = board.get_removable_pieces()

        if self.difficulty == 1:
            return random.choice(removable_pieces)

        if board.turn == board.player_1:
            opponent = board.player_2
        else:
            opponent = board.player_1

        opponent_optimal_moves = self._get_optimal_moves(board, player=opponent)
        pieces_to_remove = []

        if opponent_optimal_moves:
            for p in removable_pieces:
                for (piece, _) in opponent_optimal_moves:
                    if p == piece:
                        pieces_to_remove.append(p)

        if len(pieces_to_remove) == 0:
            if self.difficulty == 2:
                return random.choice(removable_pieces)
            else:
                for p in removable_pieces:
                    y_in_line = board.pieces_in_line("y", p)
                    x_in_line = board.pieces_in_line("x", p)
                    if y_in_line == 2 or x_in_line == 2:
                        pieces_to_remove.append(p)
                if len(pieces_to_remove) == 0:
                    return random.choice(removable_pieces)
                else:
                    return random.choice(pieces_to_remove)
        else:
            return random.choice(pieces_to_remove)
            