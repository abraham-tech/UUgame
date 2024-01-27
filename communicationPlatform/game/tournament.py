from game.player import Player, AIPlayer, Classification
import random
import math

_PLAYERS_PER_GAME = 2
_FAVOURABLE_COLOR = Classification.WHITE


class Tournament:
    def __init__(self, players, AIs=None):
        """
        Class representing a round robin tournament
        :param main: main to make callbacks to
        :param players: List of usernames of all players playing the tournament
        :param AIs: List of all AI:s as a integers, where the integer represent the AI-s difficulty.
        :precondition The length of players and AIs combined must be a minimum of 2.
        """
        self._players = {username: Player(username) for username in players}
        if AIs:
            toAI = lambda t: AIPlayer(t[0]+1, t[1])
            self._players.update({AIp.username: AIp for AIp in list(map(toAI, enumerate(AIs)))})

        self._not_played_matches = _match_schedule(list(self._players.keys()))
        self._played_matches = []
        self._current_match = None
        self._game_results = []

    def matches_left(self):
        return len(self._not_played_matches) > 0

    def get_next_match(self):
        """
        Sets the current match to the next match that are to be played
        :return: None if no matches are left to be played,
        otherwise the next match that are to be played as a tuple (white_player, black_player)
        """
        if not self._not_played_matches:
            return

        p1, p2 = self._not_played_matches.pop(0)
        p1 = self._players[p1]
        p2 = self._players[p2]
        p1.set_classification(Classification.WHITE)
        p2.set_classification(Classification.BLACK)
        self._current_match = (p1, p2)
        return self._current_match

    def get_not_played_matches(self):
        """
        Used to get the not yet played matches
        :return: List of not yet played matches
        """
        return self._not_played_matches

    def get_played_matches(self):
        """
        Used to get all the played matches
        :return: List of all played matches as [(match, winner_index)], if a match is tie [(match, None)]
        """
        return self._played_matches

    def get_players(self):
        """
            Used to get all the players in the tournament
            :return: List of all players in the tournament sorted by score in reverse
        """
        players = list(self._players.values())
        players.sort(key=_compare_player, reverse=True)
        return players

    def match_ended(self, game_result):
        """
        Used to notify that the current match have ended and updates the score accordingly
        to the game result
        :param game_result: Result of the last played match
        :return: None
        """
        if self._current_match is None:
            return

        white_player, black_player = self._current_match
        winner = None
        if game_result.winner is None:
            white_player.player_tied()
            black_player.player_tied()
        elif game_result.winner.username == white_player.username:
            white_player.player_won_white()
            winner = 0
            black_player.player_lost()
        elif game_result.winner.username == black_player.username:
            black_player.player_won_black()
            winner = 1
            white_player.player_lost()

        self._played_matches = [(self._current_match, winner)] + self._played_matches
        self._game_results += [game_result]


def _compare_player(player):
    if _FAVOURABLE_COLOR == Classification.BLACK:
        return (player.get_score(), player.get_wins_white(), player.get_wins_black())
    else:
        return (player.get_score(), player.get_wins_black(), player.get_wins_white())


def _match_schedule(players):
    """
    This function takes a list of names of players in the tournament as argument
    Returns match-touples where the first element in each touple is playing White
    The algoritms below make sure that all players gets to play white/black equal amounts of times, if possible.
    :param players: List of
    :return:
    """


    match_tuple = []
    number_players = len(players)
    len_table = int(number_players/2)
    random.shuffle(players)
    #2 players
    if(number_players == 2):
        match_tuple.append(tuple([players[0],players[1]]))
    #3 player
    elif(number_players == 3):
        top_table = players[0:2]
        bottom_table = ["x",players[-1]] 
        #Append matches .. top table is white
        for i in range(len(top_table)): 
            if "x" not in [top_table[i],bottom_table[i]]:
                match_tuple.append(tuple([top_table[i],bottom_table[i]]))
        #the two players on top table switch places
        top_table = list(reversed(top_table)) 
        bottom_table = bottom_table
        #top table is black
        for i in range(len(top_table)): 
            if "x" not in [top_table[i],bottom_table[i]]:
                match_tuple.append(tuple([bottom_table[i],top_table[i]]))
        #We swap one diagonal
        top_table_new = [bottom_table[1],top_table[1]]
        bottom_table_new = [bottom_table[0],top_table[0]]
        top_table = top_table_new
        bottom_table =  bottom_table_new
        #top table is white
        for i in range(len(top_table)): 
            if "x" not in [top_table[i],bottom_table[i]]:
                match_tuple.append(tuple([top_table[i],bottom_table[i]])) 
        
    #4 players
    elif (number_players == 4):
        top_table = players[0:int(number_players/2)]
        bottom_table = list(reversed(players[int(number_players/2):number_players]))
        #Append matches .. top table is white
        for i in range(len_table): 
            match_tuple.append(tuple([top_table[i],bottom_table[i]]))
        #the two players on top table switch places
        top_table = list(reversed(top_table)) 
        bottom_table = bottom_table
        #bot table is white
        for i in range(len_table): 
            match_tuple.append(tuple([bottom_table[i],top_table[i]]))
        #We swap one diagonal
        top_table_new = [bottom_table[1],top_table[1]]
        bottom_table_new = [bottom_table[0],top_table[0]]
        top_table = top_table_new
        bottom_table =  bottom_table_new
        #top table is white
        for i in range(len_table): 
            match_tuple.append(tuple([top_table[i],bottom_table[i]]))

    # > 4 players    
    else:
        #even numbers
        if ((number_players)%2==0):
            top_table = players[0:math.ceil(number_players/2)]
            bottom_table = list(reversed(players[int(number_players/2):number_players]))
            for k in range(number_players-1):
                for i in range(len_table):
                    #top table is white
                    if (k%2 ==0):
                        match_tuple.append(tuple([top_table[i],bottom_table[i]]))
                    #bot table is white
                    else:
                        match_tuple.append(tuple([bottom_table[i],top_table[i]]))
                bottom_table_new = bottom_table[1:len_table] + [top_table[-1]]# Every player takes a step to the left exept p1
                top_table_new = [top_table[0]]+[bottom_table[0]]+top_table[1:len_table-1] #same as above
                top_table = top_table_new
                bottom_table = bottom_table_new
        #odd numbers
        if(number_players%2 > 0):
            top_table = players[0:math.ceil(number_players/2)]
            bottom_table = ["x"]+ list(reversed(players[math.ceil(number_players/2):number_players]))
            for k in range(number_players):
                for i in range(len(top_table)):
                    if (k%2 ==0):
                        if "x" not in [top_table[i],bottom_table[i]]:
                            match_tuple.append(tuple([top_table[i],bottom_table[i]]))
                    else:
                        if "x" not in [top_table[i],bottom_table[i]]:
                            match_tuple.append(tuple([bottom_table[i],top_table[i]]))     
                bottom_table_new = bottom_table[1:len(top_table)] + [top_table[-1]]# Every player takes a step to the left exept p1
                top_table_new = [top_table[0]]+[bottom_table[0]]+top_table[1:len(top_table)-1] #same as above
                top_table = top_table_new
                bottom_table = bottom_table_new
    return(match_tuple)