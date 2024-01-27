from Singleton import Singleton
from Board import Board
from Player import Player

class Game(metaclass=Singleton):
    """
    Defines the Game class
    """

    def __init__(self):
        self.board = None
        self.state = ""
        self.settings = None #until we have a Settings class
        self.input = "menu"
        self.player_1 = None
        self.player_2 = None
        self.all_piecies = None


    def start_game_loop(self):
        """
        Start the game loop
        """

        while self.input != "q":

            if self.input == None:
                self.input = input("Give your input: ")
            
            elif self.input == "start":
                self.start_a_game()

            elif self.input == "menu":
                self.print_menu()

            elif self.input =="s":
                print("setting is not implemented. \n")
                self.input = None

            elif self.input =="reset":
                if self.board == None:
                    print("There is no board created. \n")
                    self.input = None
                else:
                    self.board.reset_board()
                    self.board.draw_board()
                    self.input = None

            else:
                print(self.input + " - is not a proper input. See in the menu what inputs you can give.\n")
                self.input = None


    def print_menu(self):
        """
        Print all items in the menu
        """
        print( "==================================================================")
        print( "                                                                  ")
        print( "    ██╗   ██╗██╗   ██╗     ██████╗  █████╗ ███╗   ███╗███████╗    ")
        print( "    ██║   ██║██║   ██║    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ")
        print( "    ██║   ██║██║   ██║    ██║  ███╗███████║██╔████╔██║█████╗      ")
        print( "    ██║   ██║██║   ██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ")
        print( "    ╚██████╔╝╚██████╔╝    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ")
        print( "     ╚═════╝  ╚═════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ")
        print( "                                                                  ")
        print( "==================================================================")
        print( "==================================================================")
        print()
        print("                     [start] start a game.")
        print("                     [reset] reset the board.")
        print("                     [menu] go to menu.")
        print("                     [q] quit the game.")
        print("                     [s] see the settings.")
        print()
        print( "==================================================================")
        self.input = None


    def start_a_game(self):
        """
        Start playing the game
        """

        player_1 = input("\tEnter the name of Player 1: ")
        player_2 = input("\tEnter the name of Player 2: ")
        while player_1 == player_2:
            print("\tError: Your name cannot be the same as Player 1!" + "\n")
            player_2 = input("\tEnter the name of Player 2: ")
        self.player_1 = Player(player_1, "#")
        self.player_2 = Player(player_2, "*")
        self.board = Board(self.player_1, self.player_2)
        print("\n\t[ " + self.player_1.name + " & " + self.player_2.name + " ] are starting a game. \n")
        self.board.init_board_pos()
        self.board.draw_board()
        self.all_piecies = len(self.player_1.pieces) + len(self.player_2.pieces)
        self.state = "play"

        while self.state == "play":
    
            # Player place a piece on the board, until all pieces are on the board
            if self.all_piecies > 0:
                
                counter = 0   
                if self.board.turn.name == self.player_1.name:
                    for piece in self.player_1.pieces:
                        if (piece.on_board == False and piece.is_alive == True):
                            counter = counter + 1

                if self.board.turn.name == self.player_2.name:
                    for piece in self.player_2.pieces:
                        if piece.on_board == False and piece.is_alive == True:
                            counter = counter + 1

                print("\tTurn: " + self.board.turn.name)
                print("\tPieces left: " + self.board.turn.get_nr_unplaced_pieces() * (" " + self.board.turn.sign))

                success = False
                secured = False
                while not success:
                    try:
                        position = input("\tSelect place to add a piece: ")
                        self.board.add_piece(self.board.turn.pieces[counter-1], position)
                        self.board.update_secured_pieces()
                        secured = self.board.check_if_secured(self.board.get_board_pos(position).piece)
                        print("\tTotal moves: " + str(self.board.turn_counter) + "\n")
                        self.board.draw_board()
                        success = True
                    except Warning as e:
                        print("\tError: " + str(e) + "\n")
                            
                self.all_piecies = self.all_piecies - 1

                if secured:
                    self._try_remove_piece()

                self.board.next_turn()

            # Player can move pieces when all pieces are on the board
            if self.all_piecies == 0:

                print("\tTurn: " + self.board.turn.name)
                print("\tYour symbol is [ " + self.board.turn.sign + " ]")
                success = False
                secured = False
                while not success: 
                    try: 
                        From = input("\tSelect a piece to move: ")
                        To = input("\tWhere would you like to put it: ")
                        self.board.move_piece(self.board.turn, self.board.get_board_pos(From).piece, To)
                        self.board.update_secured_pieces()
                        secured = self.board.check_if_secured(self.board.get_board_pos(To).piece)
                        print("\tTotal moves: " + str(self.board.turn_counter) + "\n")
                        self.board.draw_board()
                        success = True
                    except Warning as e:
                        print("\tError: " + str(e) + "\n")

                if secured:
                    self._try_remove_piece()

                if self.board.current_player_won():
                    print("\t" + str(self.board.turn.name) + " won the match!")
                    self.board.reset_board()
                    self.state = ""
                    self.input = "menu"
                elif self.board.turn_counter == 300:
                    print("\tThe game ended in a draw!")
                    self.board.reset_board()
                    self.state = ""
                    self.input = "menu"

                self.board.next_turn()


    def _try_remove_piece(self):
        """
        Try to remove a piece
        """
        print("\n\tYou have a secure line now, and you can remove an unsecure piece from your apponent.")
        success = False
        while not success:
            try:
                position = input("\tChoose a positon on the board, where you want to remove the piece --: ")
                self.board.remove_piece(position)
                self.board.update_secured_pieces()
                self.board.draw_board()
                success = True
            except Warning as e:
                print("\tError: " + str(e) + "\n")


#game = Game()
#game.start_game_loop()
