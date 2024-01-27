import abc
from os import system
import os
from enum import Enum

MIN_LENGTH_USERNAME = 3
MAX_LENGTH_USERNAME = 10
AI_MAX_DIFFICULTY = 3
AI_DIFFS = ["Easy", "Medium", "Hard"]


class bcolors:
    HEADER = '\033[95m'
    ERROR = '\033[91m\033[1m'
    DIM = '\33[90m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BG = '\33[100m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class State(Enum):
    MAIN_MENU = 1
    CREATE_SERVER = 2
    JOIN_SERVER = 3
    START_SERVER = 4
    TOURNAMENT_ENDED = 5
    IN_GAME_LOBBY = 6
    QUIT = 7
    ONE_V_ONE = 8
    TOURNAMENT = 9
    PLAY_LOCAL = 10


def _clear():
    """
    Used to clear the interface from text
    :return: None
    """
    system('cls' if os.name == "nt" else "clear")


def _collect_input(message):
    print(message)
    return input(f'{bcolors.OKBLUE}\nEnter a number: {bcolors.ENDC}')


class TextUI:
    def __init__(self, main, server_size):
        self._main = main
        self._server_size = server_size

    def in_game_lobby(self, tournament):
        """
        Used to print the in-game lobby while playing a tournament
        :param tournament: The tournament that is being played
        :return: None
        """
        _clear()
        players = tournament.get_players()

        print(f'{bcolors.BOLD}{bcolors.OKGREEN}GAME LOBBY\n{bcolors.ENDC}')
        pos = 'Pos'
        player = 'Player'
        wins = 'W/T/L'
        score = 'Score'

        print(
            f'{bcolors.BOLD}LEADERBOARD:\n\n{pos:<10} {player:<10} {score:<10} {wins:<10}{bcolors.ENDC}')
        for i, player in enumerate(players):
            print(
                f'{i + 1 :<10} {player.username:<10} {player.get_score():<10} {player.get_win_tie_loss_ratio():<10}')

        upcoming_matches = tournament.get_not_played_matches()
        print(f'\n{bcolors.BOLD}UPCOMING MATCHES:{bcolors.ENDC}')
        white = 'WHITE'
        black = 'BLACK'
        print(f'{white:^10} vs {black:^10}\n')
        for match in upcoming_matches:
            p1 = match[0]
            p2 = match[1]
            print(f'{p1:<10} vs {p2:>10}')

        played_matches = tournament.get_played_matches()
        print(f'\n{bcolors.BOLD}PLAYED MATCHES:{bcolors.ENDC}')
        white = 'WHITE'
        black = 'BLACK'
        print(f'{white:^10} vs {black:^10}\n')
        for match_tpl in played_matches:
            p1, p2 = match_tpl[0]
            winner = match_tpl[1]
            if winner is None:
                winner = 'Tie'
            else:
                winner = f'{match_tpl[0][winner].username} won!'

            print(f'{p1.username:<10} vs {p2.username:>10} Result: {winner}')

        print('\nWaiting for your game to start...\n')

    def post_game_lobby(self, tournament):
        _clear()
        players = tournament.get_players()
        print(f'{bcolors.OKGREEN}{bcolors.BOLD}RESULTS{bcolors.ENDC}\n')
        pos = 'Pos'
        player = 'Player'
        wins = 'W/T/L'
        score = 'Score'

        print(
            f'{bcolors.BOLD}{pos:<10} {player:<10} {score:<10} {wins:<10}{bcolors.ENDC}')
        for i, player in enumerate(players):
            print(
                f'{i + 1 :<10} {player.username:<10} {player.get_score():<10} {player.get_win_tie_loss_ratio():<10}')

        played_matches = tournament.get_played_matches()
        print(f'\n{bcolors.BOLD}PLAYED MATCHES:{bcolors.ENDC}')
        white = 'WHITE'
        black = 'BLACK'
        print(f'{white:^10} vs {black:^10}\n')
        for match_tpl in played_matches:
            p1, p2 = match_tpl[0]
            winner = match_tpl[1]
            if winner is None:
                winner = 'Tie'
            else:
                winner = f'{match_tpl[0][winner].username} won!'
            print(f'{p1.username:<10} vs {p2.username:>10} Result: {winner}')

        c = _collect_input('\n[1] BACK TO MAIN MENU\n[2] QUIT')
        if c == '1':
            return State.MAIN_MENU
        elif c == '2':
            return State.QUIT
        else:
            self.post_game_lobby(tournament)

    def main_menu(self, username):
        """
        Used to print the main menu.
        Takes input and callbacks accordingly to the input.
        :param username: The current players username
        :return: None
        """
        _clear()
        print(f'{bcolors.HEADER}Hi {username}!\nPlease choose one of the following options below:{bcolors.ENDC}\n')
        print(f'{bcolors.OKGREEN}{bcolors.BOLD}MAIN MENU{bcolors.ENDC}')
        print('[1] JOIN GAME\n[2] START GAME \n[3] QUIT\n')
        c = input(f'{bcolors.OKBLUE}Enter a number: {bcolors.ENDC}')
        while True:
            if c == '1':
                return State.JOIN_SERVER
            elif c == '2':
                return State.CREATE_SERVER
            elif c == '3':
                return State.QUIT
            else:
                print(f"{bcolors.WARNING}Invalid input{bcolors.ENDC}")
                c = input()

    def get_ip(self):
        """
        Used to print the join server menu.
        Takes IP as input and callbacks to join the server
        :return: None
        """
        _clear()
        return input(f'{bcolors.BOLD}{bcolors.OKGREEN}JOIN GAME{bcolors.ENDC}\n{bcolors.OKBLUE}Enter IP address (or 0 to return to main menu): {bcolors.ENDC}')

    def _get_ai_difficulty(self):
        _clear()
        print(f'{bcolors.BOLD}{bcolors.OKGREEN}ADD AI{bcolors.ENDC}')
        print("\n[1] EASY\n[2] MEDIUM\n[3] HARD\n")
        while True:
            try:
                difficulty = int(
                    input(f'{bcolors.OKBLUE}Pick a difficulty: {bcolors.ENDC}'))
                if 0 < difficulty <= AI_MAX_DIFFICULTY:
                    return difficulty
                else:
                    print(f'{bcolors.WARNING}Invalid input{bcolors.ENDC}')
                    continue
            except ValueError:
                print(f'{bcolors.WARNING}Invalid input{bcolors.ENDC}')
                continue

    def game_settings(self):
        """
        Used to collect if to play a 1v1 of tournament game
        :return:
        """
        _clear()
        c = _collect_input("Choose a option:\n[1] 1v1 Online or vs AI\n[2] Tournament\n[3] 1v1 Local PvP\n")
        if c == '1':
            return State.ONE_V_ONE
        elif c == '2':
            return State.TOURNAMENT
        elif c == '3':
                return State.PLAY_LOCAL
        else:
            self.game_settings()

    def pre_game_lobby(self, players, ai=None, ip=None, host=False, server_size=8):
        """
        Used to print the pre game lobby
        :param ai: list of all AI players in the lobby
        :param players: List of all players in the lobby
        :param ip: The IP to the current lobby
        :param host: True if player is host, otherwise false
        If host, a menu is shown and input is taken.
        :param server_size: Number of slots the current server have
        :return: None
        """
        if ai is None:
            ai = []
        _clear()
        if host:
            print(f'{bcolors.OKBLUE}Server IP: {ip}{bcolors.ENDC}')
        print(f'{bcolors.BOLD}{bcolors.OKGREEN}PRE-GAME LOBBY{bcolors.ENDC}')
        print(f'{bcolors.BOLD}Players:{bcolors.ENDC}')

        playerLen = len(players)
        aiLen = len(ai)
        for player in players:
            print('  ' + player)
        for i, ai in enumerate(ai):
            print(f'  AI-{str(i + 1)} ({AI_DIFFS[ai-1]})')
        if host:
            print(f"  {bcolors.DIM}Open\n{bcolors.ENDC}" *
                  (server_size - playerLen - aiLen))

        if host:
            print(
                f'{bcolors.DIM if playerLen + aiLen < 2 else ""}[1] START SERVER\n{bcolors.ENDC}{bcolors.DIM if playerLen + aiLen >= self._server_size else ""}[2] ADD AI\n{bcolors.ENDC}{bcolors.DIM if aiLen==0 else ""}[3] REMOVE AI\n{bcolors.ENDC}[4] QUIT TO MAIN MENU\n\n{bcolors.OKBLUE}Enter a number: {bcolors.ENDC}')
        else:
            print('\nWaiting for host to start game...')

    def get_ai_to_remove(self, ai):
        aiLen = len(ai)
        _clear()
        print(f'{bcolors.BOLD}{bcolors.OKGREEN}REMOVE AI{bcolors.ENDC}')
        print("Which AI do you want to remove?")
        for i, ai in enumerate(ai):
            print(f'[{i+1}]  AI-{str(i + 1)} ({AI_DIFFS[ai-1]})')

        while True:
            try:
                answer = input(
                    f'\n{bcolors.OKBLUE}Enter a number: {bcolors.ENDC}')
                answer = int(answer)
                if 0 < answer <= aiLen:
                    return answer
                else:
                    print(f"{bcolors.WARNING}Invalid input{bcolors.ENDC}")
                    continue
            except ValueError:
                print(f"{bcolors.WARNING}Invalid input{bcolors.ENDC}")
                continue

    def collect_username(self, message=None):
        """
        Asks the user for a inputted username. Max MAX_LENGTH_USERNAME characters, min MIN_LENGTH_USERNAME characters
        :return: The inputted username
        """
        if not (message is None):
            print(message)
        username = input(
            f'{bcolors.OKBLUE}Please enter your username: {bcolors.ENDC}')
        while len(username) > MAX_LENGTH_USERNAME or len(username) < MIN_LENGTH_USERNAME:
            username = input(f'{bcolors.WARNING}Username must be between {MIN_LENGTH_USERNAME} and {MAX_LENGTH_USERNAME} characters{bcolors.ENDC}'
                             f'\n{bcolors.OKBLUE}Please enter you username: {bcolors.ENDC}')
        return username

    def too_many_ai(self):
        """
        If host tries to add an ai player when the lobby is full
        """
        print(
            f"{bcolors.WARNING}Cannot add AI player when lobby is full{bcolors.ENDC}")

    def no_ai_to_remove(self):
        """
        If host tries to remove an AI player when there are none
        """
        print(
            f"{bcolors.WARNING}No AI players to remove{bcolors.ENDC}")

    def failed_connect_server(self):
        _clear()
        print(
            f"{bcolors.ERROR}Could not connect to server{bcolors.ENDC}\nReturning to main menu...")

    def failed_create_server(self):
        _clear()
        print(
            f"{bcolors.ERROR}Could not start server{bcolors.ENDC}\nReturning to main menu...")

    def server_disconnected(self):
        _clear()
        print(f'{bcolors.ERROR}Server disconnected!\n{bcolors.ENDC}')
        c = _collect_input(
            'Please choose one of the following options below:\n[1] MAIN MENU\n[2] QUIT')
        if c == '1':
            return State.MAIN_MENU
        elif c == '2':
            return State.QUIT
        else:
            self.server_disconnected()
