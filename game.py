from operator import itemgetter 
from collections import Counter
from players import  AIPlayer, Player


class IllegalMove(Exception):
    """
    Exception to be raise when an illegal move is made
    """
    pass


class WrongTurn(IllegalMove):
    """
    Exception to be raise when the wrong player makes a move
    """
    pass


class Game(object):
    """
    Board will look like
     | |
    1|2|3
    _|_|_
     | |
    4|5|6
    _|_|_
     | |
    7|8|9
     | |
    """

    winning_states = [
        [1,2,3],
        [4,5,6],
        [7,8,9],

        [1,4,7],
        [2,5,8],
        [3,6,9],

        [1,5,9],
        [3,5,7],
    ]

    board = []

    players = (
        {
            "symbol": "x",
            "value": 0,
            "is_human": True
        },
        {
            "symbol": "o",
            "value": 1,
            "is_human": False
        }

    )
    winner_symbol = None
    winning_row = []
    # is_game_ended  = True

    def __init__(self, \
                    player_1_symbol="x", player_1_type=Player, \
                    player_2_symbol="o", player_2_type=AIPlayer, \
                    board_state=[None for i in range(9)],
                    step=0):
        # initialize board
        self.board = board_state
        self.step = step
            
        if player_1_symbol == player_2_symbol:
            raise Exception("Players cannot have the same symbols")

        self.players = [
            player_1_type(player_1_symbol, player_2_symbol),
            player_2_type(player_2_symbol, player_1_symbol)
        ]
        print "players:::", [(p.symbol, p.type) for p in self.players]

    def loop_step(self):
        flag = True
        while(True):
            player = self.players[self.step % 2]
            move = player.make_move(self.board)
            if move: # if there is no move break out of the loop
                self.execute_move(player, move)
            else:
                flag = False

    def get_current_player(self):
        return self.players[self.step % 2]

    def execute_move(self, player): # , position):
        # make sure there are moves left and  game has not ended?
        if not self.is_game_ended: # game not ended
            # check that the player can make the move
            if self.players[self.step % 2].symbol == player.symbol:
                # place mark
                position = player.make_move(self.board)
                self.place_mark(player, position)
                self.step += 1
                return self.board
            else:
                raise WrongTurn("Invalid move, it is not the player's turn!")
        # if so who won? is it a tie?
        print " game has ended "
        print " game has been won? ", self.is_winning_board
        if self.is_winning_board:
            print " game has been won by: ", self.winner_symbol
            print " winning row :", self.winning_row


    def place_mark(self, player, position):
        if self.board[position] == None:
            self.board[position] = player.symbol
            return self.board
        raise IllegalMove("Illegal Move cell is already occupied")

    @property 
    def moves_left(self):
        cells = Counter(self.board)
        return cells.get(None,0)

    @property
    def is_game_ended(self):
        # are there any more moves?
        # count the number of empty spaces
        moves_left = Counter(self.board).get(None,0) 
        # is there a winner?
        if moves_left == 0:
            return True
        if self.is_winning_board:
            return True
        # no more moves and no winner == draw
        return False

    @property
    def is_winning_board(self):
        """
        Here we check if a board has entered a winning state
        """
        winner = None
        for state in self.winning_states:
            # because we've made the winning state start from 1
            # if we want to extract those positions we need to have them
            # start from 0
            zeroed_index = map(lambda x: x-1, state)
            board_values = itemgetter(*zeroed_index)(self.board)
            # tally up the number of X and O
            board_tally = Counter(board_values)
            # get only the values from the board_tally
            # and check if we have  3 in a row of a symbol
            # make sure we aren't summing up the None
            is_winning_state = [
                symbol for symbol, count in board_tally.items() \
                    if count == 3 and symbol is not None
                ]
            if is_winning_state:
                # there should be only one symbol as
                # we need 3 in a row to win
                winner = board_tally.keys().pop()
                self.winner_symbol = winner
                self.winning_row = zeroed_index
                return True
        return False

    def serialize_to_dict(self):
        return {
            "board": self.board,
            "players": [{"symbol": p.symbol,"player_type": p.type} for p in self.players]
        }
