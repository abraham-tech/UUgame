from Board import Board
from Player import Player
from AIPlayer import AIPlayer
from communication.server import Server, CommunicationMessage, NetworkData
import time
import json

class GameT():

    def __init__(self, match_type=None, player_1=None, player_2=None, comm=None):
        self.settings = None # Until we have a Settings class
        self.player_1 = player_1
        self.player_2 = player_2
        self.comm = comm
        self.turn = player_1
        self.match_type = match_type

    def ai_player_loop(self):
        client = None
        if self.match_type == "ha" or self.match_type == "pa":
            human_player = Player(self.player_1.username, "#")
            ai_player = AIPlayer(self.player_2.username, "@", self.player_2.get_difficulty())
            b = Board(human_player, ai_player)
            if self.match_type == "pa":
                client = self.player_1
        if self.match_type == "ah" or self.match_type == "ap":
            human_player = Player(self.player_2.username, "#")
            ai_player = AIPlayer(self.player_1.username, "@", self.player_1.get_difficulty())
            b = Board(ai_player, human_player)
            if self.match_type == "ap":
                client = self.player_2

        b.init_board_pos()
        
        pieces = 18
        while pieces > 0:

            secured = False

            if b.turn == human_player:
                msg = {"msg": "Add Piece"}
                msg = json.dumps(msg)
                self.comm.write(NetworkData(b, msg, b.turn.name))
                while not b.turn_over:
                    if client:
                        if client.username == b.turn.name:
                            r = self.comm.read()
                            if r.message == "Update Board":
                                b = r.data
            else:
                optimal_add_bp = b.turn.get_optimal_add_position(b)
                piece_to_add = b.turn.get_random_placable_piece()
                b.add_piece(piece_to_add, b.get_position_letter(optimal_add_bp))
                secured = b.check_if_secured(piece_to_add)
                b.update_secured_pieces()
                if secured:
                    piece_to_remove = b.turn.get_optimal_remove(b)
                    b.remove_piece(b.get_position_letter(piece_to_remove.position))
                    b.update_secured_pieces()

            b.next_turn()
            b.turn_over = False
            pieces -= 1

        if len(b.get_movable_pieces()) == 0:
            return self.player_2

        while b.turn_counter <= 300:

            secured = False

            if b.turn == human_player:
                msg = {"msg": "Move Piece"}
                msg = json.dumps(msg)
                self.comm.write(NetworkData(b, msg, b.turn.name))
                while not b.turn_over:
                    if client:
                        if client.username == b.turn.name:
                            r = self.comm.read()
                            if r.message == "Update Board":
                                b = r.data
            else:
                (piece_to_move, bp_to_move_to) = b.turn.get_optimal_move(b)
                b.move_piece(b.turn, piece_to_move, b.get_position_letter(bp_to_move_to))
                secured = b.check_if_secured(piece_to_move)
                b.update_secured_pieces()
                if secured:
                    piece_to_remove = b.turn.get_optimal_remove(b)
                    b.remove_piece(b.get_position_letter(piece_to_remove.position))
                    b.update_secured_pieces()

            if b.current_player_won():
                if self.player_1.username == b.turn.name:
                    return self.player_1
                else:
                    return self.player_2

            b.next_turn()
            b.turn_over = False

        return None


    def ai_ai_loop(self):
        white_temp_ai = AIPlayer(self.player_1.username, "#", self.player_1.get_difficulty())
        black_temp_ai = AIPlayer(self.player_2.username, "@", self.player_2.get_difficulty())
        b = Board(white_temp_ai, black_temp_ai)
        b.init_board_pos()
        # add pieces
        i = 0   
        while i < 9:
            j = 0
            while j < 2:
                position = b.turn.get_optimal_add_position(b)
                b.add_piece(b.turn.pieces[i], b.get_position_letter(position))
                b.update_secured_pieces()
                if b.turn.pieces[i].is_secured:
                    piece = b.turn.get_optimal_remove(b)
                    b.remove_piece(b.get_position_letter(piece.position))
                    b.update_secured_pieces()
                b.next_turn()
                j += 1
            i += 1
        # check if white player can make any moves
        if len(b.get_movable_pieces()) == 0:
            return self.player_2
        # move pieces
        while b.turn_counter <= 300:
            piece, position = b.turn.get_optimal_move(b)
            b.move_piece(b.turn, piece, b.get_position_letter(position))
            b.update_secured_pieces()
            if piece.is_secured:
                piece = b.turn.get_optimal_remove(b)
                b.remove_piece(b.get_position_letter(piece.position))
                b.update_secured_pieces()
            if b.current_player_won():
                if self.player_1.username == b.turn.name:
                    return self.player_1
                else:
                    return self.player_2
            b.next_turn()
        return None

    def player_loop(self):
        b = Board(Player(self.player_1.username, "#"), Player(self.player_2.username, "@"))
        b.init_board_pos()
        counter1 = 9
        counter2 = 9
        client = self.player_1 if self.match_type == "ph" else self.player_2

        while (True):
           
            if self.turn.username == self.player_1.username:
                counter1 -= 1 
            else:
                counter2 -= 1

            if counter1 >= 0 and counter2 >= 0:
                msg = {"msg": "Add Piece"}
                msg = json.dumps(msg)
                self.comm.write(NetworkData(b, msg, self.turn.username))
            else:
                msg = {"msg": "Move Piece"}
                msg = json.dumps(msg)
                self.comm.write(NetworkData(b, msg, self.turn.username))

            opponent = self.player_1 if self.turn == self.player_2 else self.player_2 

            while not b.turn_over:
                if client == self.turn or self.match_type == "pp":
                    r = self.comm.read()
                    if r.message == "Update Board":
                        b = r.data

            if counter1 < 0 and counter2 < 0 and b.current_player_won():
                return self.turn

            self.turn = opponent

            if b.turn_counter > 300:
                return None

            b.next_turn()
            b.turn_over = False
            


