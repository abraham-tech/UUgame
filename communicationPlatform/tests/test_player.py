import unittest
from game.player import Player


class TestPlayerMethods(unittest.TestCase):

    def test_player_won(self):
        player = Player("username")
        player.player_won_white()
        player.player_won_black()
        player.player_won_black()
        self.assertEqual(player.get_wins(), 3)
        self.assertEqual(player.get_score(), 3)

    def test_player_lost(self):
        player = Player("username")
        player.player_lost()
        player.player_lost()
        player.player_lost()
        self.assertEqual(player.get_losses(), 3)
        self.assertEqual(player.get_score(), 0)

    def test_player_tied(self):
        player = Player("username")
        player.player_tied()
        player.player_tied()
        player.player_tied()
        self.assertEqual(player.get_ties(), 3)
        self.assertEqual(player.get_score(), 1.5)

    def test_player_scoring(self):
        player = Player("username")
        player.player_won_white()
        player.player_lost()
        player.player_tied()
        self.assertEqual(player.get_score(), 1.5)
        self.assertEqual(player.get_wins(), 1)
        self.assertEqual(player.get_losses(), 1)
        self.assertEqual(player.get_ties(), 1)


if __name__ == '__main__':
    unittest.main()