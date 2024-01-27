from enum import Enum


class Classification(Enum):
    UNSPECIFIED = 0
    WHITE = 1
    BLACK = 2


class Player:
    """
    Class used to store statistics of a player
    """
    def __init__(self, username=''):
        self.username = username
        self._classification = Classification.UNSPECIFIED
        self._black_wins = 0
        self._white_wins = 0
        self._losses = 0
        self._ties = 0
        self._score = 0

    def player_won_black(self):
        """
        Used when player won a match as black, increasing win statistic and score
        :return: None
        """
        self._black_wins += 1
        self._score += 1

    def player_won_white(self):
        """
        Used when player won a match as white, increasing win statistic and score
        :return: None
        """
        self._white_wins += 1
        self._score += 1

    def player_lost(self):
        """
        Used when player lost a match, increasing lost statistic
        :return:
        """
        self._losses += 1

    def player_tied(self):
        """
        Used when player played tie in a match, increasing tie statistics
        :return:
        """
        self._ties += 1
        self._score += 0.5

    def get_wins(self):
        """
        Get the players wins
        :return: How many wins the player have
        """
        return self._white_wins + self._black_wins

    def get_wins_white(self):
        """
        Used to get the players win while playing as white
        :return: How many times the player have won as white
        """
        return self._white_wins

    def get_wins_black(self):
        """
        Used to get the players win while playing as black
        :return: How many times the player have won as black
        """
        return self._black_wins

    def get_losses(self):
        """
        Get the players losses
        :return: How many losses the player have
        """
        return self._losses

    def get_ties(self):
        """
        Get the players tie
        :return: How many times the player played a tie
        """
        return self._ties

    def get_score(self):
        """
        Get the players current score
        :return: The players score
        """
        return self._score

    def get_win_tie_loss_ratio(self):
        """
        Used to get the win/tie/loss ratio as a string w/t/l
        :return: wins, ties and losses as a string 'w/t/l'
        """
        return str(self._white_wins + self._black_wins) + '/' + self._ties.__str__() + '/' + self._losses.__str__()

    def set_classification(self, classification):
        """
        Used to set the players classification
        :param classification: The new classification of the player
        :return: None
        """
        self._classification = classification

    def get_classification(self):
        """
        Used to get the players classification
        :return: The players classificaiton
        """
        return self._classification


def _set_AI_username(username_index, difficulty):
    return 'AI-' + str(username_index) + ' (' + str(difficulty) + ')'


class AIPlayer(Player):
    """
    Class to represent a AI player
    """
    def __init__(self, username_index, difficulty):
        """
        :param username_index: Index to create a username from
        :param difficulty: The AI-players difficulty
        """
        super().__init__(_set_AI_username(username_index, difficulty))
        self._difficulty = difficulty

    def get_difficulty(self):
        """
        Used to get the AI-players difficulty
        :return: The AI-players difficulty
        """
        return self._difficulty
