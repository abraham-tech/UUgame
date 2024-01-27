import socket
import select
import queue
import threading
import pickle
from pathlib import Path
import sys
path= Path(sys.path[0])
sys.path.append(f"{path.parent}")
from enum import Enum
from Board import Board
import time
import json
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 9999  # Arbitrary non-privileged port


class CommunicationMessage(Enum):
    UPDATED_TOURNAMENT = 1
    UPDATED_PLAYERS = 2
    START_GAME = 3
    USER_INPUT = 4
    ERROR = 5
    TOURNAMENT_ENDED = 6
    CLIENT_DATA = 7
    EXISTING_USERNAME_ERROR = 7
    SERVER_DISCONNECTED = 8
    GAME_RESULT = 9
    GAME_MOVE = 10
    GAME_STATE = 11


class NetworkData:
    """
    Class used to encapsulate data that are to be sent using this communication module
    """

    def __init__(self, data, message, receiver="", sender=""):
        """
        :param data: The data that are to be sent
        :param message: The CommunicationMessage associated to the data
        :param receiver: If the data have a specific receivers, the receivers username
        """
        self.data = data
        self.message = message
        self.receiver = receiver
        self.sender = sender


class Server:
    def __init__(self, player_name):
        self._sockets = []  # All sockets
        self._player_from_socket = {}  # Key: socket, value: player name
        self._socket_from_player = {}  # Key: Player name, value: socket
        self._player_name = player_name.strip()
        self._accepting_clients = True
        self._read_queue = queue.Queue()
        self._write_queue = queue.Queue()
        self._max_clients = 8
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((HOST, PORT))
            self.server.listen()
            self._sockets.append(self.server)
        except:
            raise Exception
        # Start read thread
        threading.Thread(target=self._readServer, daemon=True).start()

        # Start write thread
        threading.Thread(target=self._writeServer, daemon=True).start()

    def write(self, data):
        """
        Used send data to all or a specific connected client
        :param data: The data that are to be sent
        """
        self._write_queue.put(data)

    def read(self):
        """
        Used to read income data to the server. If no data is received the thread waits until data is received.
        Data is read as first in, fist out.
        :return: Data that have arrived to the server.
        """
        msg=self._read_queue.get()

        return msg

    def async_input(self):
        threading.Thread(target=self._async_input, daemon=True).start()

    def _async_input(self):
        self._read_queue.put(NetworkData(
            input(), CommunicationMessage.USER_INPUT, "server"))

    def stop_accept(self):
        """
        Used to stop the possibility to connect to the server
        """
        self._accepting_clients = False

    def start_accept(self):
        """
        Used to enable the possibility to connect to the server
        """
        self._accepting_clients = True

    def update_max_clients(self, x):
        """
        Used to change the max allowed connected clients to the server
        :param x: The number of max allowed connections. Must be 0<
        """
        if x <= 1:
            raise Exception
        self._max_clients = x

    def decrease_max_clients(self):
        """
        Used to change the max allowed connected clients to the server
        when an AI is added to the lobby
        """
        self._max_clients -= 1

    def increase_max_clients(self):
        """
        Used to change the max allowed connected clients to the server
        when an AI is added to the lobby
        """
        self._max_clients += 1

    def connection_exists(self, username):
        """
        Used to check if a connection exist to a specific client
        :param username: The clients username
        :return: True if connection exists, otherwise False
        """
        return username in self._socket_from_player

    def _readServer(self):
        while True:
            try:
                to_read, _, _ = select.select(self._sockets, [], [])
                for active_socket in to_read:
                    if active_socket is self.server:
                        # Accept new clients
                        new_socket, _ = self.server.accept()
                        if len(self._socket_from_player) >= self._max_clients - 1 or not self._accepting_clients:
                            new_socket.close()
                            continue
                        raw_data = new_socket.recv(4096)  # Receieve user name

                        # If disconnected immediately
                        if not raw_data:
                            new_socket.close()
                            continue

                        name = pickle.loads(raw_data).strip()

                        # If already connected
                        if name in self._socket_from_player or name == self._player_name:
                            new_socket.sendall(
                                pickle.dumps(NetworkData(None, CommunicationMessage.EXISTING_USERNAME_ERROR)))
                            new_socket.close()
                            continue

                        # Add socket and player data
                        self._sockets.append(new_socket)
                        self._player_from_socket[new_socket] = name
                        self._socket_from_player[name] = new_socket

                        # Do something with players
                        self._read_queue.put(NetworkData([self._player_name] + list(self._socket_from_player),
                                                         CommunicationMessage.UPDATED_PLAYERS,
                                                         "server"))

                    # If receiving data from client
                    else:
                        name = self._player_from_socket[active_socket]
                        raw_data = active_socket.recv(4096)

                        # If disconnected
                        if not raw_data:
                            self._sockets.remove(active_socket)
                            del self._player_from_socket[active_socket]
                            del self._socket_from_player[name]
                            active_socket.close()

                            # Do something with players
                            self._read_queue.put(NetworkData([self._player_name] + list(self._socket_from_player),
                                                             CommunicationMessage.UPDATED_PLAYERS,
                                                             "server"))
                            continue
                        data = pickle.loads(raw_data)
                        data.sender = name
                        # Do something with data
                        self._read_queue.put(data)
            except:
                return

    def _writeServer(self):
        while True:
            network_data = self._write_queue.get()
            if not network_data:
                return
            data = network_data.data
            player_name = network_data.receiver
            raw_data = pickle.dumps(network_data)
            if player_name != "":
                if player_name == self._player_name:
                    if isinstance(data,Board):
                        board = data
                        board.draw_board()
                        message = json.loads(network_data.message)
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
                                    piece= board.get_board_pos(fr).piece
                                    board.move_piece(board.turn,piece,t)
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
                else:
                    self._socket_from_player[player_name].sendall(raw_data)
            else:
                for socket in self._player_from_socket:
                    socket.sendall(raw_data)

    def end(self):
        self.server.close()
        self.write(None)
        for s in self._player_from_socket:
            s.close()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('1.1.1.1', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
