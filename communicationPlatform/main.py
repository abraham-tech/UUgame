from game.tournament import Tournament
from game.game_result import GameResult
from game.player import AIPlayer, Classification
from ui.text_ui import TextUI, State, bcolors, AI_DIFFS
from communication.server import Server, CommunicationMessage, NetworkData
from communication.client import Client
import random
import time
import sys
import atexit
from GameT import GameT
import sys
from Board import Board
from AIPlayer import AIPlayer as AIPlayerEnginge
from Game import Game

SERVER_SIZE = 8
ONE_V_ONE = 2

def ai_to_list(ai):
    result = []
    for i, ai in enumerate(ai):
        result.append(f'AI-{str(i + 1)} ({AI_DIFFS[ai-1]})')
    return result


class Main:
    """
    Main-class that runs the program
    """

    def __init__(self):
        self._ui = TextUI(self, 8)
        self.tournament = None
        self.username = ''
        self.players = []
        self.ip = "192.168.0.1"
        self.state = State.MAIN_MENU
        self.host = False
        self.comm = None
        self.ai = []

    def start(self):
        """
        Used to start the program
        """
        self.username = self._ui.collect_username()
        while True:
            if self.state == State.MAIN_MENU:
                self.state = self._ui.main_menu(self.username)
            elif self.state == State.CREATE_SERVER:
                self.state = self.create_server()
            elif self.state == State.JOIN_SERVER:
                self.ip = self._ui.get_ip()
                if self.ip == '0':
                    self.state = State.MAIN_MENU
                    continue

                self.join_server()

            elif self.state == State.START_SERVER:
                self.start_server()
            elif self.state == State.TOURNAMENT_ENDED:
                self.state = self._ui.post_game_lobby(self.tournament)
            elif self.state == State.IN_GAME_LOBBY:
                self.in_tournament()
            elif self.state == State.QUIT:
                if not (self.comm is None):
                    self.comm.end()
                sys.exit()
            else:
                print(f"{bcolors.ERROR}Invalid state{bcolors.ENDC}")
                sys.exit()

    def start_tournament(self):
        """
        Used to start a tournament and play all matches
        """
        self.comm.write(NetworkData(self.tournament,
                                    CommunicationMessage.UPDATED_TOURNAMENT))
        while self.tournament.matches_left():
            self._ui.in_game_lobby(self.tournament)
            match = self.tournament.get_next_match()
            self.comm.write(NetworkData(self.tournament,
                                        CommunicationMessage.UPDATED_TOURNAMENT))
            self.start_match(match)
        self.tournament_ended()

    def start_match(self, match):
        """
        Start one match
        :param match: The match that are to be started
        """
        white_player, black_player = match
        if isinstance(white_player, AIPlayer) and isinstance(black_player, AIPlayer):
            # Start AI vs AI
            self._start_ai_vs_ai(match)
        elif isinstance(white_player, AIPlayer) and black_player.username == self.username:
            # Start AI vs host
            self._start_ai_vs_host(match)
        elif white_player.username == self.username and isinstance(black_player, AIPlayer):
            # Start host vs AI
            self._start_host_vs_ai(match)
        elif white_player.username == self.username:
            # Start host vs player
            self._start_host_vs_player(match)
        elif black_player.username == self.username:
            # Start player vs host
            self._start_player_vs_host(match)
        elif isinstance(white_player, AIPlayer):
            # Start AI vs player
            self._start_ai_vs_player(match)
        elif isinstance(black_player, AIPlayer):
            # Start player vs AI
            self._start_player_vs_ai(match)
        else:
            # Start player vs player
            self._start_player_vs_player(match)



    def _match_ended(self, winner):
        game_result = GameResult(None, winner)
        self.tournament.match_ended(game_result)
        self.comm.write(NetworkData(self.tournament, CommunicationMessage.UPDATED_TOURNAMENT))

    def _start_ai_vs_ai(self, match):
        """
        Used to start an AI vs AI match
        :param match: The match that are to be started containing (AIPlayer, AIPlayer)
        """
        white_ai, black_ai = match
        g = GameT(player_1=white_ai, player_2=black_ai, comm=self.comm)
        winner = g.ai_ai_loop()
        self._match_ended(winner)

    def _start_ai_vs_host(self, match):
        """
        Used to start an AI vs host match
        :param match: The match that are to be started containing (AIPlayer, Player) where Player is host
        """
        white_ai, black_host = match
        print('Starting AI vs host')
        g = GameT(match_type="ah", player_1=white_ai, player_2=black_host, comm=self.comm)
        winner = g.ai_player_loop()
        self._match_ended(winner)

    def _start_host_vs_ai(self, match):
        """
        Used to start an host vs AI match
        :param match: The match that are to be started containing (Player, AIPlayer) where player is host
        """
        white_host, black_ai = match
        print('Starting host vs AI')
        g = GameT(match_type="ha", player_1=white_host, player_2=black_ai, comm=self.comm)
        winner = g.ai_player_loop()
        self._match_ended(winner)

    def _start_host_vs_player(self, match):
        """
        Used to start an host vs player match
        :param match: The match that are to be started containing (Player1, Player2) where Player1 is host
        and Player2 is a client
        """
        white_host, black_player = match
        if not self.comm.connection_exists(black_player.username):
            # Client disconnected, host won on walk over.
            self._walk_over_victory(white_host)
            return

        print('Starting host vs player')
        g = GameT(match_type="hp", player_1=white_host, player_2=black_player, comm=self.comm)
        winner = g.player_loop()
        self._match_ended(winner)

    def _start_player_vs_host(self, match):
        """
        Used to start an player vs host match
        :param match: The match that are to be started containing (Player1, Player2) where Player2 is host
        and Player1 is a client
        """
        white_player, black_host = match
        if not self.comm.connection_exists(white_player.username):
            # Client disconnected, host won on walk over.
            self._walk_over_victory(black_host)
            return

        print('Starting player vs host')
        self.comm.write(NetworkData(
            match, CommunicationMessage.START_GAME, white_player.username))

        g = GameT(match_type="ph", player_1=white_player, player_2=black_host, comm=self.comm)
        winner = g.player_loop()
        self._match_ended(winner)

    def _start_player_vs_player(self, match):
        """
        Used to start a player vs player match
        :param match: The match that are to be started containing (Player1, Player2) where both are clients
        """
        print('Starting player vs player')
        white_player, black_player = match
        w_connected = self.comm.connection_exists(white_player.username)
        b_connected = self.comm.connection_exists(black_player.username)
        if not w_connected and not b_connected:
            # Both players disconnected, match set to tie
            self._walk_over_victory(None)
            return
        elif not w_connected:
            # White player disconnected, black player won on walk over
            self._walk_over_victory(black_player)
            return
        elif not b_connected:
            # Black player disconnected, white player won on walk over
            self._walk_over_victory(white_player)
            return

        self.comm.write(NetworkData(
            match, CommunicationMessage.START_GAME, white_player.username))
        self.comm.write(NetworkData(
            match, CommunicationMessage.START_GAME, black_player.username))

        time.sleep(5) # Is this needed?
        g = GameT(match_type="pp", player_1=white_player, player_2=black_player, comm=self.comm)
        winner= g.player_loop()
        self._match_ended(winner)

    def _start_ai_vs_player(self, match):
        """
        Used to start an AI vs player match
        :param match: The match that are to be started containing (AIPlayer, Player)
        """
        white_ai, black_player = match
        if not self.comm.connection_exists(black_player.username):
            # Black player disconnected, AI won on walk over
            self._walk_over_victory(white_ai)
            return

        g = GameT(match_type="ap", player_1=white_ai, player_2=black_player, comm=self.comm)
        winner = g.ai_player_loop()
        self._match_ended(winner)

    def _start_player_vs_ai(self, match):
        """
        Used to start an player vs AI match
        :param match: The match that are to be started containing (Player, AIPlayer)
        """
        white_player, black_ai = match
        if not self.comm.connection_exists(white_player.username):
            # White player disconnected, AI won on walk over
            self._walk_over_victory(black_ai)
            return

        g = GameT(match_type="pa", player_1=white_player, player_2=black_ai, comm=self.comm)
        winner = g.ai_player_loop()
        self._match_ended(winner)

        self.comm.write(NetworkData(
            match, CommunicationMessage.START_GAME, white_player.username))
        network_data = self.comm.read()
        if network_data.message == CommunicationMessage.GAME_RESULT:
            self.tournament.match_ended(network_data.data)
            self.comm.write(NetworkData(self.tournament,
                                        CommunicationMessage.UPDATED_TOURNAMENT))

    def _start_local_match(self, match):
        """
        Used to start a local played match, i.e. starting the game for the player
        :param match: The match that are to be started
        """
        white_player, black_player = match
        # TODO start player vs player
        # TODO remove demo code
        if white_player.username == self.username:
            print('Starting local match')
            time.sleep(1)
            random_result = GameResult(
                None, random.choice((white_player, black_player)))
            self.comm.write(NetworkData(
                random_result, CommunicationMessage.GAME_RESULT))
        else:
            network_data = self.comm.read()
            if network_data.message == CommunicationMessage.UPDATED_TOURNAMENT:
                self.tournament = network_data.data

    def _walk_over_victory(self, player):
        """
        Used to notify that the last match in the tournament was won due to a walk over (disconnected player)
        :param player: The player that won the match, or None if both players disconnected
        """
        self.tournament.match_ended(GameResult(None, player))
        self.comm.write(NetworkData(self.tournament,
                                    CommunicationMessage.UPDATED_TOURNAMENT))

    def in_tournament(self):
        """
        Used to put a client player in wait before their matches will begin.
        Listening from communication from the server
        """
        while True:
            self._ui.in_game_lobby(self.tournament)
            network_data = self.comm.read()
            if network_data.message == CommunicationMessage.UPDATED_TOURNAMENT:
                self.tournament = network_data.data
            elif network_data.message == CommunicationMessage.START_GAME:
                self._start_local_match(network_data.data)
            elif network_data.message == CommunicationMessage.TOURNAMENT_ENDED:
                self.tournament = network_data.data
                self.state = State.TOURNAMENT_ENDED
                self.comm.end()
                self.comm = None
                break
            elif network_data.message == CommunicationMessage.SERVER_DISCONNECTED:
                self.comm.end()
                self.comm = None
                self.state = self._ui.server_disconnected()
            return

    def tournament_ended(self):
        """
        Ends the current tournament and sends the result to all connected players
        :return:
        """
        self.state = State.TOURNAMENT_ENDED
        self.comm.write(NetworkData(self.tournament,
                                    CommunicationMessage.TOURNAMENT_ENDED))
        self.ai = []
        self.players = []

    def _failed_connection(self):
        self._ui.failed_connect_server()
        time.sleep(2)
        self.state = State.MAIN_MENU

    def join_server(self):
        """
        Used when joining a another server. Tries to connect to a server, if fails. Returns to main menu
        :return: None
        """
        try:
            self.comm = Client(self.username, self.ip)
            network_data = self.comm.read()
            if network_data.message == CommunicationMessage.EXISTING_USERNAME_ERROR:
                self.username = self._ui.collect_username(
                    f'{bcolors.WARNING}Username is occupied. Change it and try again.{bcolors.ENDC}')
                return
            elif network_data.message == CommunicationMessage.UPDATED_PLAYERS:
                self.players = network_data.data
            elif network_data.message == CommunicationMessage.SERVER_DISCONNECTED:
                self._failed_connection()
                return
        except:
            self._failed_connection()
            return

        self.host = False
        self._ui.pre_game_lobby(self.players)
        while True:
            network_data = self.comm.read()
            message = network_data.message
            data = network_data.data
            if not message:
                continue
            elif message == CommunicationMessage.UPDATED_PLAYERS:
                self.players = data
                self._ui.pre_game_lobby(self.players)
            elif message == CommunicationMessage.UPDATED_TOURNAMENT:
                self.tournament = data
                self.state = State.IN_GAME_LOBBY
                break
            elif message == CommunicationMessage.SERVER_DISCONNECTED:
                self.comm.end()
                self.comm = None
                self.state = self._ui.server_disconnected()
                return

    def start_server(self):
        """
        Used to start a game server. Stops clients to be able to connect and starts the tournament/match
        :return: None
        """
        self.comm.stop_accept()
        self.tournament = Tournament(self.players, self.ai)
        self.comm.write(NetworkData(self.tournament,
                                    CommunicationMessage.UPDATED_TOURNAMENT))
        self.start_tournament()

    def add_AI(self, difficulty, server_size):
        """
        Used to add a AI to the current game server. If no room on server, no AI is added
        :param difficulty: The difficulty of the AI
        :param server_size: The number of player slots on the current game server
        :return: None
        """
        if len(self.ai) + len(self.players) < server_size:
            self.ai.append(difficulty)
            self.comm.write(NetworkData(
                self.players + ai_to_list(self.ai), CommunicationMessage.UPDATED_PLAYERS))
            self.comm.decrease_max_clients()

    def remove_AI(self, index):
        """
        Used to remove a AI from the current server.
        :param index: Index of the current AI
        :return: None
        """
        del self.ai[index]
        self.comm.increase_max_clients()
        self.comm.write(NetworkData(
            self.players + ai_to_list(self.ai), CommunicationMessage.UPDATED_PLAYERS))

    def quit_comm(self):
        """
        Used to quit the communication component and restoring game server to default values
        :return: Main Menu state
        """
        if self.comm:
            self.comm.end()
        self.comm = None
        self.ai = []
        self.players = []
        self.host = False
        return State.MAIN_MENU

    def create_server(self):
        """
        Used to create a game server
        :return: START_SERVER if server is about to be started or MAIN_MENU if to return to the main menu
        """
        game_setting = self._ui.game_settings()
        if game_setting == State.PLAY_LOCAL:
            g = Game()
            g.start_game_loop()
            return State.MAIN_MENU
        else:
            server_size = SERVER_SIZE if game_setting == State.TOURNAMENT else ONE_V_ONE
            try:
                self.comm = Server(
                self.username) if self.comm is None else self.comm
            except:
                self._ui.failed_create_server()
                time.sleep(2)
                return State.MAIN_MENU
            self.comm.update_max_clients(server_size)
            self.comm.start_accept()
            self.players = [self.username]
            self.ip = self.comm.get_ip()
            self.host = True
            self._ui.pre_game_lobby(self.players, self.ai, self.ip, self.host, server_size)
            self.comm.async_input()
            while True:
                network_data = self.comm.read()
                message = network_data.message
                data = network_data.data
                if not message:
                    continue

                if message == CommunicationMessage.UPDATED_PLAYERS:
                    self.players = data
                    self.comm.write(NetworkData(
                    self.players + ai_to_list(self.ai), CommunicationMessage.UPDATED_PLAYERS))
                    self._ui.pre_game_lobby(
                    self.players, self.ai, self.ip, self.host, server_size)
                elif message == CommunicationMessage.USER_INPUT:
                    if data:
                        command = data[-1]
                    else:
                        command = None
                    if command == '1':
                        if 1 < len(self.players) + len(self.ai) <= server_size:
                            return State.START_SERVER
                        else:
                            print(
                            f'{bcolors.WARNING}At least 2 players required{bcolors.ENDC}')
                            self.comm.async_input()
                    elif command == "2":
                        if len(self.ai) + len(self.players) < server_size:
                            self.add_AI(self._ui._get_ai_difficulty(), server_size)
                            self._ui.pre_game_lobby(
                            self.players, self.ai, self.ip, self.host, server_size)
                        else:
                            self._ui.too_many_ai()
                        self.comm.async_input()
                        continue
                    elif command == "3":
                        if len(self.ai):
                            self.remove_AI(self._ui.get_ai_to_remove(self.ai)-1)
                            self._ui.pre_game_lobby(
                            self.players, self.ai, self.ip, self.host, server_size)
                        else:
                            self._ui.no_ai_to_remove()
                        self.comm.async_input()
                        continue
                    elif command == "4":
                        return self.quit_comm()
                    else:
                        print(f"{bcolors.WARNING}\nIncorrect input{bcolors.ENDC}")
                        self.comm.async_input()

    def _randomize_game_result_demo(self, w_p, b_p):
        time.sleep(1)
        finished_game = None
        # Derive game result from finished game
        game_result = GameResult(finished_game, random.choice(
            (random.choice((w_p, b_p)), None)))
        # Send game result to tournament
        self.tournament.match_ended(game_result)
        # Send tournament to server/other players
        self.comm.write(NetworkData(self.tournament,
                                    CommunicationMessage.UPDATED_TOURNAMENT))


if __name__ == '__main__':
    m = Main()
    atexit.register(m.quit_comm)
    try:
        m.start()
    except KeyboardInterrupt:
        sys.exit()
