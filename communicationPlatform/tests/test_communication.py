import unittest
from communication.client import Client
from communication.server import Server, CommunicationMessage, NetworkData, PORT
import time


class TestPlayerMethods(unittest.TestCase):
    def test_connect(self):
        s = Server("Player1")
        c = Client("Player2", "")
        time.sleep(0.1)
        self.assertTrue("Player2" in s._socket_from_player)
        s.end()
        c.end()

    def test_send_receive(self):
        s = Server("Player1")
        c = Client("Player2", "")
        c.write(NetworkData("test", CommunicationMessage.CLIENT_DATA))
        # First receive player list
        self.assertEqual(s.read().message,
                         CommunicationMessage.UPDATED_PLAYERS)
        self.assertEqual(s.read().data, "test")


if __name__ == '__main__':
    unittest.main()
