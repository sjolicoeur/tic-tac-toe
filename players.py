from operator import itemgetter 
from collections import Counter
import random

class NoMoveSet(Exception):
    pass


class Player(object):
    """
    Default type of player, is human.
    Needs input
    """

    next_move = None
    
    def __init__(self, symbol, opponent_symbol, player_type="human"):
        self.symbol = symbol
        self.opponent_symbol = opponent_symbol
        self.type = player_type

    def make_move(self, board):
        if self.next_move is not None:
            position = self.next_move
            self.next_move = None
            return position
        raise NoMoveSet("Player has Not made a decision")

    def set_move(self, position):
        self.next_move = position


class AIPlayer(Player):
    """
    Automated player, that is quite frustrating to play against.
    No real strategy. It evaluates potential fields makes a choice to maximize points
    or random betwen equally scored cells
    - center is always of high value
    - the board may be given other biases
    - assume board is made out of 9 cells
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

    def __init__(self, symbol, opponent_symbol, player_type="AI"):
        super(AIPlayer, self).__init__(symbol, opponent_symbol, player_type=player_type)

    def get_potential_moves(self, board):
        """
        Get a list of possible moves for a given board state
        """
        scored_board = self.score_current_board(board)
        max_score = max(scored_board)
        valid_moves = []
        for i, value in enumerate(scored_board):
            if max_score and value == max_score:
                valid_moves.append(i)
        return valid_moves

    def make_move(self, board):
        """
        Strategy to choose from valid moves
        this is what will be played on the board
        """
        valid_moves = self.get_potential_moves( board)
        if not valid_moves:
            return valid_moves
        elif len(valid_moves) == 1:
            return valid_moves.pop()
        else:
            index = random.randrange(len(valid_moves))
            return valid_moves[index]

    def calculate_state_score_weight(self, state):
        """
        Given a row score it base on what it contains
        # 0: if the row is full
        # 2: if it contains a single symbol
        # 4: if it contains two of the same symbols
        # 5: if it contains two of the same symbols that are the player's
        """
        row_tally = Counter(state)
        bonus = 0
        weight = 0
        # filter out the Nones so we don't count them
        row_tally = dict([
            (symbol, count) for symbol,count in row_tally.items() \
                if symbol is not None
        ])

        checksum = sum(row_tally.values())
        if checksum == 3: # if the row is full
            return 0
        if checksum == 2 and len(row_tally.values()) == 1: # the row is almost full with one symbol
            bonus = 5
            if self.symbol in row_tally: # it's the AI's symbol so ad bonus for that
                bonus += 3
        if checksum == 1: # if there is a single sybol in this row score itas one
            bonus = 1
        weight = 1 + bonus
        return weight

    def score_current_board(self, board):
        scored_board = [0 for i in range(9)]
        # add bias
        # score the center cell at 3 to start with
        scored_board[4] = 3 
        # add bias for second and third moves
        # we want to score the cross higher surrounding the center
        # higher
        if board.count(None) in [6,7]:
            scored_board[1] = 3
            scored_board[3] = 3
            scored_board[5] = 3
            scored_board[7] = 3

        for state in self.winning_states:
            # align indexes to 0
            zeroed_index = map(lambda x: x-1, state)
            # get row
            board_values = itemgetter(*zeroed_index)(board)
            # calculate the score for that row
            score = self.calculate_state_score_weight(board_values)
            # apply score to each cell
            for i in zeroed_index:
                if board[i] is None:
                    scored_board[i] += score  
                else:
                    scored_board[i] = None
        return scored_board



