
class GameResult:

    def __init__(self, finished_game, _winner=None):
        """
        Used to represent a game result.
        :param finished_game: A finished game to derive game result from
        :param _winner: USED FOR TESTING AND DEMO, Player object of the winner. None implies that the game was a tie
        """
        # TODO derive game result from finished game state, set winner to winner, or None if a tie
        self.winner = _winner
