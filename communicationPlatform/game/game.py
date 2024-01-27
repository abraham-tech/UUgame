
class Game:

    def __init__(self, white_player_username, black_player_username):
        self.black_player_username = black_player_username
        self.white_player_username = white_player_username

    def is_players_move(self, player_username):
        """
        Used to check if it's a specific players turn to make a move
        :param player_username: The players username
        :return: True if it's players turn to make a move, otherwise false
        """
        pass

    def print_game_state(self):
        """
        Used to print the current game state and board to the user
        :return:
        """
        pass

    def collect_move(self):
        """
        Used to collect a move from a player. Prints game state, takes input, verifies input, and returns move if valid
        :return: The collected move
        """
        pass

    def make_move(self, move):
        """
        Used to make a move in the game state
        :param move The move that are to be made in the current game
        :return: True if successful, otherwise False
        """
        pass

    def game_ended(self):
        """
        Used to check if a game has ended
        :return: True if game ended, otherwise False
        """
        pass

    def get_winner(self):
        """
        Used to get the currents game winner.
        Can only be used on a game that has ended.
        :return: Username of the player that won or None if the game was a tie
        """
        pass

    def import_game_state(self, game_state):
        """
        Used to update the current game state to the imported game state
        :param game_state: The new game state containing as GameState
        :return: None
        """
        pass

    def export_game_state(self):
        """
        Used to derive all data from the current game state to a data object only containing the data
        :return: The current game state as a GameState object
        """
        pass

class GameState:
    def __init__(self, board, white_player, black_player):
        self.board = board
        self.white_player = white_player
        self.black_player = black_player
