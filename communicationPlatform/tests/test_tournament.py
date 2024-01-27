import unittest
from game.game_result import GameResult
from game.tournament import * 


class TestTournamentLogic(unittest.TestCase):

    def test_get_players(self):
        tournament = setup_tournament_even_amount()
        self.assertEqual(len(tournament.get_players()), 8)

    def test_get_players_empty_tournament(self):
        tournament = setup_empty_tournament()
        self.assertEqual(len(tournament.get_players()), 0)

    def test_get_played_matches(self):
        tournament = setup_tournament_even_amount()
        self.assertEqual(len(tournament.get_played_matches()), 0)

    def test_get_not_played_matches(self):
        tournament = setup_tournament_even_amount()
        n_players = len(tournament.get_players())
        self.assertEqual(len(tournament.get_not_played_matches()), n_players*(n_players-1)/2)

    def test_get_next_match(self):
        tournament = setup_tournament_even_amount()
        n_players = len(tournament.get_players())
        m1 = tournament.get_next_match()
        self.assertEqual(len(tournament.get_not_played_matches()), n_players*(n_players-1)/2-1)
        m2 = tournament.get_next_match()
        self.assertEqual(len(tournament.get_not_played_matches()), n_players*(n_players-1)/2-2)
        self.assertNotEqual(m1, m2)

    def test_get_next_match_empty_tournament(self):
        t = setup_empty_tournament()
        t.get_next_match()

    def test_one_match_ended(self):
        tournament = setup_tournament_even_amount()
        p1, p2 = tournament.get_next_match()

        tournament.match_ended(GameResult(None, p1))
        played_matches = tournament.get_played_matches()
        self.assertEqual(len(played_matches), 1)
        p1, p2 = played_matches[0][0]
        self.assertEqual(p1.get_wins(), 1)
        self.assertEqual(p1.get_losses(), 0)
        self.assertEqual(p2.get_wins(), 0)
        self.assertEqual(p2.get_losses(), 1)

    def test_match_ended_tie(self):
        tournament = setup_tournament_even_amount()
        tournament.get_next_match()

        tournament.match_ended(GameResult(None, None))
        played_matches = tournament.get_played_matches()
        self.assertEqual(len(played_matches), 1)
        p1, p2 = played_matches[0][0]
        self.assertEqual(p1.get_wins(), 0)
        self.assertEqual(p1.get_losses(), 0)
        self.assertEqual(p1.get_ties(), 1)
        self.assertEqual(p2.get_wins(), 0)
        self.assertEqual(p2.get_losses(), 0)
        self.assertEqual(p2.get_ties(), 1)

    def test_all_matches_ended(self):
        tournament = setup_tournament_even_amount()
        n_players = len(tournament.get_players())

        while tournament.matches_left():
            tournament.get_next_match()
            tournament.match_ended(GameResult(None, None))

        self.assertEqual(len(tournament.get_not_played_matches()), 0)
        self.assertEqual(len(tournament.get_played_matches()), n_players*(n_players-1)/2)

    def test_match_algorithm_even_players(self):
        tournament = setup_tournament_even_amount()
        matches = tournament.get_not_played_matches()
        p0_white = 0
        p0_black = 0
        for w_p, b_p in matches:
            if w_p == "Player0":
                p0_white += 1
            elif b_p == 'Player0':
                p0_black += 1

        self.assertEqual((p0_white+p0_black) % 2, 1)

    def test_match_algorithm_uneven_players(self):
        tournament = setup_tournament_uneven_amount()
        matches = tournament.get_not_played_matches()
        p0_white = 0
        p0_black = 0
        for w_p, b_p in matches:
            if w_p == "Player0":
                p0_white += 1
            elif b_p == 'Player0':
                p0_black += 1

        self.assertEqual((p0_white+p0_black) % 2, 0)


# Utils for setting up the tests
def setup_tournament_even_amount():
    players = []
    for i in range(8):
        players += ['Player'+i.__str__()]
    return Tournament(players)


def setup_tournament_uneven_amount():
    players = []
    for i in range(7):
        players += ['Player'+i.__str__()]
    return Tournament(players)


def setup_empty_tournament():
    return Tournament([])


class TestMain():
    def callback_match_ended(self):
        pass

    def callback_start_tournament(self):
        pass

    def callback_tournament_ended(self):
        pass

    def callback_update_ui(self):
        pass
