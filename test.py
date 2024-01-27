import unittest
import random
from Board import Board
from Player import Player
from AIPlayer import AIPlayer

class Test(unittest.TestCase):
    """
    Tests for all public Board class methods
    """

    def setUp(self):
        self.p1 = AIPlayer("player1", "#", 1)
        self.p2 = AIPlayer("player2", "@", 1)
        self.b = Board(self.p1, self.p2)
        self.b.init_board_pos()

    def test_add_piece(self):

        # Add piece and make sure it gets added
        self.b.add_piece(self.b.player_1.pieces[1], "z")
        self.assertEqual(self.b.board_positions[23].piece, self.b.player_1.pieces[1])
        self.assertTrue(self.b.board_positions[23].piece.on_board)
        self.assertTrue(self.b.board_positions[23].piece.is_alive)

        # You cannot add a piece where a piece already exists
        with self.assertRaises(Warning): self.b.add_piece(self.b.player_1.pieces[1], "z")

    def test_AI_block_add(self):

        self.b.player_2.difficulty = 2

        # Add piece and make sure it gets added on the correct position
        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_1.pieces[1], "c")
        position = self.b.player_2.get_optimal_add_position(self.b)
        self.b.add_piece(self.b.player_2.pieces[0], self.b.get_position_letter(position))
        self.assertEqual(self.b.get_position_letter(self.b.player_2.pieces[0].position), "b")

        # Block with multiple alternatives
        self.b.move_piece(self.b.player_2, self.b.player_2.pieces[0], "e")
        self.b.add_piece(self.b.player_1.pieces[3], "g")
        self.b.add_piece(self.b.player_1.pieces[4], "i")
        self.b.add_piece(self.b.player_1.pieces[5], "r")
        self.b.add_piece(self.b.player_1.pieces[6], "q")
        position = self.b.player_2.get_optimal_add_position(self.b)
        self.b.add_piece(self.b.player_2.pieces[1], self.b.get_position_letter(position))
        self.assertTrue(self.b.get_board_pos('b') != None or self.b.get_board_pos('h') != None or self.b.get_board_pos('p') != None )

    def test_get_optimal_add_position_AI(self):

        self.b.next_turn()

        self.b.add_piece(self.b.player_2.pieces[0], "a")
        self.b.add_piece(self.b.player_2.pieces[1], "b")
        self.b.add_piece(self.b.player_2.pieces[2], "j")

        # Difficulty 2
        self.b.player_2.difficulty = 2

        for i in range(3, 5):
            bp = self.b.player_2.get_optimal_add_position(self.b)
            self.b.add_piece(self.b.player_2.pieces[i], self.b.get_position_letter(bp))

        self.assertTrue(self.b.check_if_secured(self.b.player_2.pieces[3]))
        self.assertTrue(self.b.check_if_secured(self.b.player_2.pieces[4]))

        # Difficulty 3
        self.b.player_2.difficulty = 3

        # Place so that 2 in line
        for i in range(5, 7):
            bp = self.b.player_2.get_optimal_add_position(self.b)
            self.b.add_piece(self.b.player_2.pieces[i], self.b.get_position_letter(bp))

        self.assertTrue(self.b.check_if_secured(self.b.player_2.pieces[5]))
        self.assertTrue(self.b.check_if_secured(self.b.player_2.pieces[6]))

        # Place to form triplet and block opponent

        self.b.next_turn()
        self.b.player_1.difficulty = 3

        self.b.add_piece(self.b.player_1.pieces[0], "q")
        self.b.add_piece(self.b.player_1.pieces[1], "p")
        self.b.add_piece(self.b.player_1.pieces[2], "t")
        self.b.add_piece(self.b.player_2.pieces[7], "i")
        self.b.add_piece(self.b.player_2.pieces[8], "m")

        self.b.remove_piece(self.b.get_position_letter(self.b.player_2.pieces[5].position))
        self.b.remove_piece(self.b.get_position_letter(self.b.player_2.pieces[6].position))

        bp = self.b.player_1.get_optimal_add_position(self.b)
        self.b.add_piece(self.b.player_1.pieces[3], self.b.get_position_letter(bp))

        # The options are w and r to form a triplet, but only r will block opponent
        self.assertEqual("r", self.b.get_position_letter(self.b.player_1.pieces[3].position))

    def test_check_if_two_in_line(self):

        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_1.pieces[1], "b")
        self.b.add_piece(self.b.player_1.pieces[2], "j")
        self.b.add_piece(self.b.player_1.pieces[3], "z")

        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[0], 2))
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[1], 2))
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[2], 2))
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[3], 2))

    def test_check_if_secured_one_player(self):

        # Check that each piece is secure when a line on the x-axis is formed
        self.b.add_piece(self.b.player_1.pieces[0], "z")
        self.b.add_piece(self.b.player_1.pieces[1], "w")
        self.b.add_piece(self.b.player_1.pieces[2], "v")
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[0]))
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[1]))
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[2]))

        # Check that each piece is secure when a line on the y-axis is formed
        self.b.add_piece(self.b.player_1.pieces[3], "t")
        self.b.add_piece(self.b.player_1.pieces[4], "q")
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[3]))
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[4]))

        # Check that pieces lose security when a line is broken (a player moves a secured piece)
        self.b.move_piece(self.b.player_1, self.b.player_1.pieces[4], "r")
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[3]))
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[4]))
        self.assertTrue(self.b.check_if_secured(self.b.player_1.pieces[1]))

    def test_check_if_secured_two_players(self):

        # Check that each piece is not secure when an opponent's piece blocks the formation of a line on the x-axis
        self.b.add_piece(self.b.player_1.pieces[1], "z")
        self.b.add_piece(self.b.player_2.pieces[2], "w")
        self.b.add_piece(self.b.player_1.pieces[3], "v")
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[1]))
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[2]))
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[3]))

        # Check that each piece is not secure when an opponent's piece blocks the formation of a line on the y-axis
        self.b.add_piece(self.b.player_1.pieces[4], "t")
        self.b.add_piece(self.b.player_1.pieces[5], "q")
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[4]))
        self.assertFalse(self.b.check_if_secured(self.b.player_1.pieces[5]))

    def test_update_secured_pieces_one_player(self):

        # Check that is_secured is updated properly on each piece when a line on the x-axis is formed
        self.b.add_piece(self.b.player_1.pieces[1], "z")
        self.b.add_piece(self.b.player_1.pieces[2], "w")
        self.b.add_piece(self.b.player_1.pieces[3], "v")
        self.b.add_piece(self.b.player_1.pieces[8], "u") # To avoid special condition
        self.assertFalse(self.b.player_1.pieces[1].is_secured)
        self.assertFalse(self.b.player_1.pieces[2].is_secured)
        self.assertFalse(self.b.player_1.pieces[3].is_secured)
        self.b.update_secured_pieces()
        self.assertTrue(self.b.player_1.pieces[1].is_secured)
        self.assertTrue(self.b.player_1.pieces[2].is_secured)
        self.assertTrue(self.b.player_1.pieces[3].is_secured)

        # Check that is_secured is updated properly on each piece when a line on the y-axis is formed
        self.b.add_piece(self.b.player_1.pieces[4], "t")
        self.b.add_piece(self.b.player_1.pieces[5], "q")
        self.assertFalse(self.b.player_1.pieces[4].is_secured)
        self.assertFalse(self.b.player_1.pieces[5].is_secured)
        self.b.update_secured_pieces()
        self.assertTrue(self.b.player_1.pieces[4].is_secured)
        self.assertTrue(self.b.player_1.pieces[5].is_secured)

        # Check that is_secured is updated properly on each piece when a line is broken (a player moves a secured piece)
        self.b.move_piece(self.b.player_1, self.b.player_1.pieces[5], "r")
        self.b.update_secured_pieces()
        self.assertFalse(self.b.player_1.pieces[4].is_secured)
        self.assertFalse(self.b.player_1.pieces[5].is_secured)
        self.assertTrue(self.b.player_1.pieces[2].is_secured)

    def test_update_secured_pieces_all_secured(self):

        # Test the special condition where if all of a player's pieces are secured they all become unsecured
        self.b.add_piece(self.b.player_2.pieces[0], "z")
        self.b.add_piece(self.b.player_2.pieces[1], "w")
        self.b.add_piece(self.b.player_2.pieces[2], "v")
        self.b.update_secured_pieces()
        self.assertFalse(self.b.player_2.pieces[0].is_secured)
        self.assertFalse(self.b.player_2.pieces[1].is_secured)
        self.assertFalse(self.b.player_2.pieces[2].is_secured)
        self.b.remove_piece("z") # Should not crash

    def test_update_secured_pieces_two_players(self):

        # Check that is_secured is not set to true if an opponent's piece blocks the formation of a line on the x-axis
        self.b.add_piece(self.b.player_1.pieces[1], "z")
        self.b.add_piece(self.b.player_2.pieces[2], "w")
        self.b.add_piece(self.b.player_1.pieces[3], "v")
        self.assertFalse(self.b.player_1.pieces[1].is_secured)
        self.assertFalse(self.b.player_2.pieces[2].is_secured)
        self.assertFalse(self.b.player_1.pieces[3].is_secured)
        self.b.update_secured_pieces()
        self.assertFalse(self.b.player_1.pieces[1].is_secured)
        self.assertFalse(self.b.player_2.pieces[2].is_secured)
        self.assertFalse(self.b.player_1.pieces[3].is_secured)

        # Check that is_secured is not set to true if an opponent's piece blocks the formation of a line on the y-axis
        self.b.add_piece(self.b.player_1.pieces[4], "t")
        self.b.add_piece(self.b.player_1.pieces[5], "q")
        self.assertFalse(self.b.player_1.pieces[4].is_secured)
        self.assertFalse(self.b.player_1.pieces[5].is_secured)
        self.b.update_secured_pieces()
        self.assertFalse(self.b.player_1.pieces[4].is_secured)
        self.assertFalse(self.b.player_1.pieces[5].is_secured)

    def test_remove_piece(self):

        # Make sure a piece is properly removed
        self.b.add_piece(self.b.player_2.pieces[1], "z")
        self.b.remove_piece("z")
        self.assertEqual(self.b.board_positions[23].piece, None)
        self.assertFalse(self.b.player_2.pieces[1].on_board)
        self.assertFalse(self.b.player_2.pieces[1].is_alive)
        self.assertFalse(self.b.player_2.pieces[1].is_secured)

        # The removed piece cannot be added to the board again
        with self.assertRaises(Warning): self.b.add_piece(self.b.player_2.pieces[1], "z")

        # Cannot remove piece from a position that does not have a piece on it
        with self.assertRaises(Warning): self.b.remove_piece("a")

        # Cannot remove your own piece
        self.b.add_piece(self.b.player_1.pieces[0], "a")
        with self.assertRaises(Warning): self.b.remove_piece("a")

        # If a piece is secure, it cannot be removed
        self.b.add_piece(self.b.player_2.pieces[2], "z")
        self.b.add_piece(self.b.player_2.pieces[3], "w")
        self.b.add_piece(self.b.player_2.pieces[4], "v")
        self.b.add_piece(self.b.player_2.pieces[5], "u") # To avoid special condition
        self.b.update_secured_pieces()
        with self.assertRaises(Warning): self.b.remove_piece("z")
        self.assertEqual(self.b.board_positions[23].piece, self.b.player_2.pieces[2])
        self.assertTrue(self.b.player_2.pieces[2].on_board)
        self.assertTrue(self.b.player_2.pieces[2].is_alive)
        self.assertTrue(self.b.player_2.pieces[2].is_secured)

        # Cannot remove a piece if position is invalid
        with self.assertRaises(Warning): self.b.remove_piece(",")

    def test_random_remove_piece_AI(self):

        self.b.add_piece(self.b.player_1.pieces[0], "e")
        self.b.add_piece(self.b.player_1.pieces[1], "f")
        self.b.add_piece(self.b.player_1.pieces[2], "g")
        self.b.add_piece(self.b.player_1.pieces[3], "h")
        self.b.add_piece(self.b.player_1.pieces[4], "i")
        self.b.next_turn()
        for _ in range(0, 5):
            piece_to_remove = self.b.player_2.get_optimal_remove(self.b)
            self.b.remove_piece(self.b.get_position_letter(piece_to_remove.position))

    def test_get_optimal_remove_AI(self):

        # Difficulty 2
        self.b.player_2.difficulty = 2
        # Remove piece that opponent can move to form a triplet
        self.b.add_piece(self.b.player_2.pieces[0], "a")
        self.b.add_piece(self.b.player_2.pieces[1], "c")
        self.b.add_piece(self.b.player_2.pieces[2], "e")

        piece_to_remove = self.b.player_2.get_optimal_remove(self.b)
        self.b.remove_piece(self.b.get_position_letter(piece_to_remove.position))

        self.assertTrue(self.b.get_board_pos("e").piece == None)

        # Difficulty 3
        self.b.player_2.difficulty = 3
        # Remove opponent's piece that has formed a line of two pieces
        self.b.add_piece(self.b.player_2.pieces[3], "j")
        piece_to_remove = self.b.player_2.get_optimal_remove(self.b)
        self.b.remove_piece(self.b.get_position_letter(piece_to_remove.position))
        self.b.add_piece(self.b.player_2.pieces[4], "v")

        self.assertFalse(self.b.check_if_secured(self.b.player_2.pieces[3]))

    def test_reset_board(self):

        # Check that turn counter is reset and each of the player's pieces are reset properly
        self.b.add_piece(self.b.player_2.pieces[1], "z")
        self.b.add_piece(self.b.player_2.pieces[0], "w")
        self.b.add_piece(self.b.player_1.pieces[2], "v")
        self.b.remove_piece("z")
        self.b.next_turn()
        self.b.reset_board()
        self.assertEqual(self.b.turn_counter, 1)
        self.assertEqual(self.b.turn, self.b.player_1)

        self.assertFalse(self.b.player_2.pieces[1].on_board)
        self.assertTrue(self.b.player_2.pieces[1].is_alive)
        self.assertFalse(self.b.player_2.pieces[1].is_secured)

        self.assertFalse(self.b.player_2.pieces[0].on_board)
        self.assertTrue(self.b.player_2.pieces[0].is_alive)
        self.assertFalse(self.b.player_2.pieces[0].is_secured)

        self.assertFalse(self.b.player_1.pieces[2].on_board)
        self.assertTrue(self.b.player_1.pieces[2].is_alive)
        self.assertFalse(self.b.player_1.pieces[2].is_secured)

    def test_next_turn(self):

        self.b.next_turn()
        self.assertEqual(self.b.turn_counter, 2)
        self.assertEqual(self.b.turn, self.b.player_2)
        self.b.next_turn()
        self.assertEqual(self.b.turn, self.b.player_1)

    def test_move_piece(self):

        self.b.add_piece(self.b.player_1.pieces[1], "z")
        self.b.add_piece(self.b.player_2.pieces[1], "w")
        self.b.add_piece(self.b.player_1.pieces[2], "v")

        # Do not move if position is not adjacent
        with self.assertRaises(Warning): self.b.move_piece(self.b.player_1, self.b.player_1.pieces[1], "u")
        self.assertEqual(self.b.board_positions[23].piece, self.b.player_1.pieces[1])

        # Do not move if position already has a piece
        with self.assertRaises(Warning): self.b.move_piece(self.b.player_1, self.b.player_1.pieces[1], "w")
        self.assertEqual(self.b.board_positions[23].piece, self.b.player_1.pieces[1])

        # Do not move if invalid position
        with self.assertRaises(Warning): self.b.move_piece(self.b.player_1, self.b.player_1.pieces[1], ",")
        self.assertEqual(self.b.board_positions[23].piece, self.b.player_1.pieces[1])

        # Do not move if trying to move opponent's piece
        with self.assertRaises(Warning): self.b.move_piece(self.b.player_2, self.b.player_1.pieces[1], "o")
        with self.assertRaises(Warning): self.b.move_piece(self.b.player_1, self.b.player_2.pieces[1], "o")
        self.assertEqual(self.b.board_positions[22].piece, self.b.player_2.pieces[1])
        self.assertEqual(self.b.board_positions[23].piece, self.b.player_1.pieces[1])

        # Make sure the position the piece moved to has registered the move
        self.b.move_piece(self.b.player_1, self.b.player_1.pieces[1], "o")
        self.assertEqual(self.b.board_positions[14].piece, self.b.player_1.pieces[1])
        self.assertEqual(self.b.board_positions[23].piece, None)

        # Make sure the piece can move to a new position more than once
        self.b.move_piece(self.b.player_1, self.b.player_1.pieces[1], "z")

        # Test AIPlayer's move 5 times
        self.b.next_turn()
        for _ in range(0, 5):
            (piece, position) = self.b.player_2.get_optimal_move(self.b)
            self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))

    def test_get_optimal_move_AI(self):
        self.b.next_turn()
        self.b.add_piece(self.b.player_2.pieces[0], "a")
        self.b.add_piece(self.b.player_2.pieces[1], "c")
        self.b.add_piece(self.b.player_2.pieces[2], "e")

        # Difficulty 2
        self.b.player_2.difficulty = 2

        # Move to form a triplet
        self.b.update_secured_pieces()
        (piece, position) = self.b.player_2.get_optimal_move(self.b)
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))
        self.assertEqual(self.b.get_position_letter(self.b.player_2.pieces[2].position), "b")

        # Avoid unvalid position and fallback to random move
        self.b.move_piece(self.b.player_2, piece, "e")
        self.b.add_piece(self.b.player_1.pieces[1], "b")
        self.b.update_secured_pieces()
        (piece, position) = self.b.player_2.get_optimal_move(self.b)
        origin = piece.position
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))
        self.assertFalse(self.b.get_position_letter(self.b.player_2.pieces[2].position) == "b")
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(origin))

        # Form a triplet with multiple alternatives
        self.b.add_piece(self.b.player_1.pieces[3], "g")
        self.b.add_piece(self.b.player_1.pieces[4], "i")
        self.b.add_piece(self.b.player_1.pieces[5], "r")
        self.b.add_piece(self.b.player_1.pieces[6], "q")
        self.b.remove_piece("b")
        self.b.update_secured_pieces()
        (piece, position) = self.b.player_2.get_optimal_move(self.b)
        origin = piece.position
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))
        self.assertTrue(self.b.check_if_secured(piece))
        counter = 0
        for piece in self.b.player_2.pieces:
            if self.b.check_if_secured(piece):
                counter += 1
        self.assertEqual(counter, 3)

        # Difficulty 3
        self.b.player_2.difficulty = 3

        self.b.add_piece(self.b.player_2.pieces[3], "k")
        self.b.update_secured_pieces()
        (piece, position) = self.b.player_2.get_optimal_move(self.b)
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))
        self.assertEqual(self.b.get_position_letter(self.b.player_2.pieces[3].position), "j")


    def test_AI_block_move(self):
        self.b.next_turn()
        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_1.pieces[1], "c")
        self.b.add_piece(self.b.player_2.pieces[2], "e")

        self.b.player_2.difficulty = 3

        # Move to block a potential triplet
        (piece, position) = self.b.player_2.get_optimal_move(self.b)
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))

        self.assertEqual(self.b.get_position_letter(self.b.player_2.pieces[2].position), "b")

        # Block with multiple alternatives
        self.b.move_piece(self.b.player_2, piece, "e")
        self.b.add_piece(self.b.player_1.pieces[3], "g")
        self.b.add_piece(self.b.player_1.pieces[4], "i")
        self.b.add_piece(self.b.player_1.pieces[5], "r")
        self.b.add_piece(self.b.player_1.pieces[6], "q")
        self.b.add_piece(self.b.player_2.pieces[6], "l")
        (piece, position) = self.b.player_2.get_optimal_move(self.b)
        self.b.move_piece(self.b.player_2, piece, self.b.get_position_letter(position))
        self.assertTrue(self.b.get_board_pos('b') != None or self.b.get_board_pos('h') != None or self.b.get_board_pos('p') != None )

    def test_current_player_won_no_move(self):

        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_1.pieces[1], "e")
        self.b.add_piece(self.b.player_1.pieces[2], "o")
        self.b.add_piece(self.b.player_2.pieces[0], "b")
        self.b.add_piece(self.b.player_2.pieces[1], "c")
        self.assertTrue(self.b.current_player_won())

    def test_current_player_won_two_pieces_left(self):

        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_1.pieces[1], "b")
        self.b.add_piece(self.b.player_1.pieces[2], "c")
        self.b.add_piece(self.b.player_2.pieces[0], "w")
        self.b.add_piece(self.b.player_2.pieces[1], "z")
        self.assertTrue(self.b.current_player_won())
        self.b.add_piece(self.b.player_2.pieces[2], "v")
        self.assertFalse(self.b.current_player_won())

    def test_get_add_positions(self):

        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_2.pieces[0], "b")
        self.assertTrue(self.b.board_positions[2] in self.b.get_empty_positions())
        self.assertFalse(self.b.board_positions[0] in self.b.get_empty_positions())

    def test_get_movable_pieces(self):

        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_2.pieces[1], "b")
        self.b.add_piece(self.b.player_2.pieces[2], "j")
        self.assertFalse(self.b.player_1.pieces[0] in self.b.get_movable_pieces())
        self.b.next_turn()
        self.assertTrue(self.b.player_2.pieces[1] in self.b.get_movable_pieces())
        self.b.next_turn()
        self.b.remove_piece("b")
        self.assertTrue(self.b.player_1.pieces[0] in self.b.get_movable_pieces())

    def test_get_removable_pieces(self):

        self.b.add_piece(self.b.player_1.pieces[0], "a")
        self.b.add_piece(self.b.player_2.pieces[1], "b")
        self.b.add_piece(self.b.player_2.pieces[2], "j")
        self.assertTrue(self.b.player_2.pieces[1] in self.b.get_removable_pieces())
        self.assertFalse(self.b.player_2.pieces[3] in self.b.get_removable_pieces())
        self.assertFalse(self.b.player_1.pieces[0] in self.b.get_removable_pieces())

    def test_get_random_add_pieces(self):

        (piece, position) = (self.b.player_2.get_random_placable_piece(), self.b.player_2.get_optimal_add_position(self.b))
        self.b.add_piece(piece, self.b.get_position_letter(position))
        self.assertEqual(piece, position.piece)
        (piece, position) = (self.b.player_2.get_random_placable_piece(), self.b.player_2.get_optimal_add_position(self.b))
        self.b.add_piece(piece, self.b.get_position_letter(position))
        self.assertEqual(piece, position.piece)
        (piece, position) = (self.b.player_2.get_random_placable_piece(), self.b.player_2.get_optimal_add_position(self.b))
        self.b.add_piece(piece, self.b.get_position_letter(position))
        self.assertEqual(piece, position.piece)
        (piece, position) = (self.b.player_2.get_random_placable_piece(), self.b.player_2.get_optimal_add_position(self.b))
        self.b.add_piece(piece, self.b.get_position_letter(position))
        self.assertEqual(piece, position.piece)

    def test_get_board_pos(self):

        self.assertEqual(self.b.get_board_pos("a"), self.b.board_positions[0])
        self.assertEqual(self.b.get_board_pos("b"), self.b.board_positions[1])
        self.assertEqual(self.b.get_board_pos("c"), self.b.board_positions[2])
        self.assertEqual(self.b.get_board_pos("d"), self.b.board_positions[3])
        self.assertEqual(self.b.get_board_pos("e"), self.b.board_positions[4])
        self.assertEqual(self.b.get_board_pos("f"), self.b.board_positions[5])
        self.assertEqual(self.b.get_board_pos("g"), self.b.board_positions[6])
        self.assertEqual(self.b.get_board_pos("h"), self.b.board_positions[7])
        self.assertEqual(self.b.get_board_pos("i"), self.b.board_positions[8])
        self.assertEqual(self.b.get_board_pos("j"), self.b.board_positions[9])
        self.assertEqual(self.b.get_board_pos("k"), self.b.board_positions[10])
        self.assertEqual(self.b.get_board_pos("l"), self.b.board_positions[11])
        self.assertEqual(self.b.get_board_pos("m"), self.b.board_positions[12])
        self.assertEqual(self.b.get_board_pos("n"), self.b.board_positions[13])
        self.assertEqual(self.b.get_board_pos("o"), self.b.board_positions[14])
        self.assertEqual(self.b.get_board_pos("p"), self.b.board_positions[15])
        self.assertEqual(self.b.get_board_pos("q"), self.b.board_positions[16])
        self.assertEqual(self.b.get_board_pos("r"), self.b.board_positions[17])
        self.assertEqual(self.b.get_board_pos("s"), self.b.board_positions[18])
        self.assertEqual(self.b.get_board_pos("t"), self.b.board_positions[19])
        self.assertEqual(self.b.get_board_pos("u"), self.b.board_positions[20])
        self.assertEqual(self.b.get_board_pos("v"), self.b.board_positions[21])
        self.assertEqual(self.b.get_board_pos("w"), self.b.board_positions[22])
        self.assertEqual(self.b.get_board_pos("z"), self.b.board_positions[23])

    def test_get_position_letter(self):

        self.assertEqual("a", self.b.get_position_letter(self.b.board_positions[0]))
        self.assertEqual("b", self.b.get_position_letter(self.b.board_positions[1]))
        self.assertEqual("c", self.b.get_position_letter(self.b.board_positions[2]))
        self.assertEqual("d", self.b.get_position_letter(self.b.board_positions[3]))
        self.assertEqual("e", self.b.get_position_letter(self.b.board_positions[4]))
        self.assertEqual("f", self.b.get_position_letter(self.b.board_positions[5]))
        self.assertEqual("g", self.b.get_position_letter(self.b.board_positions[6]))
        self.assertEqual("h", self.b.get_position_letter(self.b.board_positions[7]))
        self.assertEqual("i", self.b.get_position_letter(self.b.board_positions[8]))
        self.assertEqual("j", self.b.get_position_letter(self.b.board_positions[9]))
        self.assertEqual("k", self.b.get_position_letter(self.b.board_positions[10]))
        self.assertEqual("l", self.b.get_position_letter(self.b.board_positions[11]))
        self.assertEqual("m", self.b.get_position_letter(self.b.board_positions[12]))
        self.assertEqual("n", self.b.get_position_letter(self.b.board_positions[13]))
        self.assertEqual("o", self.b.get_position_letter(self.b.board_positions[14]))
        self.assertEqual("p", self.b.get_position_letter(self.b.board_positions[15]))
        self.assertEqual("q", self.b.get_position_letter(self.b.board_positions[16]))
        self.assertEqual("r", self.b.get_position_letter(self.b.board_positions[17]))
        self.assertEqual("s", self.b.get_position_letter(self.b.board_positions[18]))
        self.assertEqual("t", self.b.get_position_letter(self.b.board_positions[19]))
        self.assertEqual("u", self.b.get_position_letter(self.b.board_positions[20]))
        self.assertEqual("v", self.b.get_position_letter(self.b.board_positions[21]))
        self.assertEqual("w", self.b.get_position_letter(self.b.board_positions[22]))
        self.assertEqual("z", self.b.get_position_letter(self.b.board_positions[23]))

    def test_game_loop_3_3(self):

        self.b.player_1.difficulty = 3
        self.b.player_2.difficulty = 3
        run_game_loop(self.b)

    def test_game_loop_3_2(self):

        self.b.player_1.difficulty = 3
        self.b.player_2.difficulty = 2
        run_game_loop(self.b)

    def test_game_loop_3_1(self):

        self.b.player_1.difficulty = 3
        self.b.player_2.difficulty = 1
        run_game_loop(self.b)

    def test_game_loop_2_2(self):

        self.b.player_1.difficulty = 2
        self.b.player_2.difficulty = 2
        run_game_loop(self.b)

    def test_game_loop_2_1(self):

        self.b.player_1.difficulty = 2
        self.b.player_2.difficulty = 1
        run_game_loop(self.b)

    def test_game_loop_1_1(self):

        self.b.player_1.difficulty = 1
        self.b.player_2.difficulty = 1
        run_game_loop(self.b)


def run_game_loop(board):

    pieces = 18

    while pieces > 0:

        optimal_add_bp = board.turn.get_optimal_add_position(board)
        piece_to_add = board.turn.get_random_placable_piece()
        board.add_piece(piece_to_add, board.get_position_letter(optimal_add_bp))
        board.update_secured_pieces()
        secured = board.check_if_secured(piece_to_add)

        if secured:
            piece_to_remove = board.turn.get_optimal_remove(board)
            board.remove_piece(board.get_position_letter(piece_to_remove.position))
            board.update_secured_pieces()

        board.next_turn()

        pieces -= 1

    while board.turn_counter < 300:

        # This is an edge case where the player who's turn it is to make the first move has no
        # movable pieces due to unlucky placements during the adding phase
        if len(board.get_movable_pieces()) == 0:
            if board.turn == board.player_1:
                opponent = board.player_2
            else:
                opponent = board.player_1
            print(f"{opponent} won the match on turn {board.turn_counter}!")
            return

        (piece_to_move, bp_to_move_to) = board.turn.get_optimal_move(board)
        board.move_piece(board.turn, piece_to_move, board.get_position_letter(bp_to_move_to))
        board.update_secured_pieces()
        secured = board.check_if_secured(piece_to_move)

        if secured:
            piece_to_remove = board.turn.get_optimal_remove(board)
            board.remove_piece(board.get_position_letter(piece_to_remove.position))
            board.update_secured_pieces()

        if board.current_player_won():
            print(f"{board.turn.name} won the match on turn {board.turn_counter}!")
            return

        board.next_turn()

    print(f"The game ended in a draw on turn {board.turn_counter}!")


if __name__ == "__main__":
    unittest.main()
