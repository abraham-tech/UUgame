import socket
import queue
import threading
import pickle
from communication.server import PORT, CommunicationMessage, NetworkData
from pathlib import Path
import sys
path= Path(sys.path[0])
sys.path.append(f"{path.parent}")
from Board import Board
import time
import json


class Client:

    def __init__(self, player_name, server_ip):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._player_name = player_name
        self._read_queue = queue.Queue()
        self._write_queue = queue.Queue()
        self._server.connect((server_ip, PORT))

        # Start read thread
        threading.Thread(target=self._read_server, daemon=True).start()

        # Start write thread
        threading.Thread(target=self._write_server, daemon=True).start()

        self._server.sendall(pickle.dumps(player_name))

    def read(self):
        """
        Used to read income data to the client. If no data is received the thread waits until data is received.
        Data is read as first in, first out
        :return: Data that have arrived from the server
        """
        msg = self._read_queue.get()
        if isinstance(msg.data, Board):
            board = msg.data
            board.draw_board()
            message = json.loads(msg.message) 
            print("\tTurn: " + board.turn.name)
            if (message["msg"] == "Add Piece"):
                while True:
                    try:
                        print("\tPieces left: " + board.turn.get_nr_unplaced_pieces() * (" " + board.turn.sign))
                        f = input("\tSelect place to add a piece: ")
                        board.add_piece(board.turn.get_random_placable_piece(), f)
                        board.update_secured_pieces()
                        secured = board.check_if_secured(board.get_board_pos(f).piece)
                        print("\tTotal moves: " + str(board.turn_counter) + "\n")
                        break
                    except Warning as e:
                        print("\tError: " + str(e) + "\n")
            else:
                while True:
                    try:
                        print("\tYour symbol is [ " + board.turn.sign + " ]")
                        fr = input("\tSelect a piece to move: ")
                        t = input("\tWhere would you like to put it: ")
                        piece = board.get_board_pos(fr).piece
                        board.move_piece(board.turn, piece, t)
                        board.update_secured_pieces()
                        secured = board.check_if_secured(board.get_board_pos(t).piece)
                        print("\tTotal moves: " + str(board.turn_counter) + "\n")
                        break
                    except Warning as e:
                        print("\tError: " + str(e) + "\n")
            if secured:
                while True:
                    try:
                        position = input("\tYou have created a secured line, select one of opponents piece to remove: ")
                        board.remove_piece(position)
                        board.update_secured_pieces()
                        break
                    except Warning as e:
                        print("\tError: " + str(e) + "\n")
            board.turn_over = True
            self.write(NetworkData(board, "Update Board",))
        return msg

    def write(self, data):
        """
        Used to send data to the server
        :data The NetworkData that are to be sent
        :return: None
        """
        return self._write_queue.put(data)

    def _read_server(self):
        while True:
            try:
                raw_data = self._server.recv(4096)
                if not raw_data:
                    self._read_queue.put(NetworkData(
                        None, CommunicationMessage.SERVER_DISCONNECTED))
                    return
                data = pickle.loads(raw_data)
                # Do something with data
                self._read_queue.put(data)
            except:
                return

    def _write_server(self):
        while True:
            data = self._write_queue.get()
            if not data:
                return
            raw_data = pickle.dumps(data)
            self._server.sendall(raw_data)

    def end(self):
        self.write(None)
        self._server.close()
