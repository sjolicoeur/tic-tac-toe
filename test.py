import unittest
from game import  Game
from players import AIPlayer


class TestWinningStateDetection(unittest.TestCase):

    def test_top_row_is_winning(self):
        game_board = Game()
        game_board.board = [
            "X", "X", "X",
            "O", "O", None,
            None,None,None
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(is_win)
        assert game_board.winner_symbol == "X"


    def test_top_left_diagonal_row_is_winning(self):
        game_board = Game()
        game_board.board = [
            "O", "X", "X",
            "O", "O", "x",
            None,"x","O"
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(is_win)
        assert game_board.winner_symbol == "O"

    def test_right_column_is_winning(self):
        game_board = Game()
        game_board.board = [
            "O", "O", "X",
            "O", "O", "X",
            None,"x","X"
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(is_win)
        assert game_board.winner_symbol == "X"

    def test_no_winning_state_1(self):
        game_board = Game()
        game_board.board = [
            "O", "O", "X",
            "O", None, "X",
            None,"x",None
        ]

        is_win = game_board.is_winning_board
        self.assertFalse(is_win)
        assert game_board.winner_symbol == None

    def test_no_winning_state_2(self):
        game_board = Game()
        game_board.board = [
            "O", "O", "X",
            "O", "O", "X",
            None,"x",None
        ]

        is_win = game_board.is_winning_board
        self.assertFalse(is_win)
        assert game_board.winner_symbol == None


class TestEndGameStateDetection(unittest.TestCase):
    def test_no_more_moves_game_ended_draw(self):
        game_board = Game()
        game_board.board = [
            "X", "O", "X",
            "O", "X", "X",
            "O", "X", "O"
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(game_board.is_game_ended)
        self.assertFalse(is_win)
        assert game_board.winner_symbol == None

    def test_no_more_moves_game_ended_win(self):
        game_board = Game()
        game_board.board = [
            "X", "O", "O",
            "O", "X", "X",
            "O", "X", "X"
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(game_board.is_game_ended)
        self.assertTrue(is_win)
        assert game_board.winner_symbol == "X"

    def test_quick_winning_state_game_ended(self):
        game_board = Game()
        game_board.board = [
            "X", "O", None,
            "O", "X", None,
            None,None,"X"
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(game_board.is_game_ended)
        self.assertTrue(is_win)
        assert game_board.winner_symbol == "X"

    def test_long_game_winning_game_ended(self):
        game_board = Game()
        game_board.board = [
            "X", "O", None,
            "O", "X","X",
            "O", "O","X"
        ]

        is_win = game_board.is_winning_board
        self.assertTrue(game_board.is_game_ended)
        self.assertTrue(is_win)
        assert game_board.winner_symbol == "X"

    def test_short_game_not_ended(self):
        game_board = Game()
        game_board.board = [
            "X", "O", None,
            None, None,None,
            "O", None,"X"
        ]

        is_win = game_board.is_winning_board
        self.assertFalse(game_board.is_game_ended)
        self.assertFalse(is_win)
        assert game_board.winner_symbol == None

    def test_long_game_not_ended(self):
        game_board = Game()
        game_board.board = [
            "X", "O", "X",
            None, None,"O",
            "O", "X","X"
        ]

        is_win = game_board.is_winning_board
        self.assertFalse(game_board.is_game_ended)
        self.assertFalse(is_win)
        assert game_board.winner_symbol == None




class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.board_and_results = [
            # 0
            {
                "board_to_score": [
                    "x", "o", "x",
                    None, "o", "o",
                    "x", None, "x"
                ],
                "expected_score": [
                    None, None, None,
                    15, None, None,
                    None, 15,  None,
                ],
                "expected_moves": [3,7],
                "player_args": ("o", "x")
            },
            # 1 
            {
                "board_to_score": [
                    "x", "o", "x",
                    None, "o", "o",
                    None,"x", "x"
                ],
                "expected_score": [
                    None, None, None,
                    8, None, None,
                    12, None,  None,
                ],
                "expected_moves": [6],
                "player_args": ("x", "o")

            },
            # 2
            {
                "board_to_score": [
                    "x", "o", "x",
                    None, "o", "o",
                    None, None, "x"
                ],
                "expected_score": [
                    None, None, None,
                    8, None, None,
                    5, 8,  None,
                ],
                "expected_moves": [3,7],
                "player_args": ("x", "o")

            },
            # 3 DUPE?
            {
                "board_to_score": [
                    "x", "o", "x",
                    None, "o", None,
                    None, None, "x"
                ],
                "expected_score": [
                    None, None, None,
                    4, None, 8,
                    5, 11,  None,
                ],
                "expected_moves": [7],
                "player_args": ("o", "x")

            },
            # 4
            {
                "board_to_score": [
                    None, None, None,
                    None, "x", None,
                    None, None, "o"
                ],
                "expected_score": [
                    3, 6, 5,
                    6, None, 7,
                    5, 7,  None,
                ],
                "expected_moves": [5,7],
                "player_args": ("o", "x")

            },
            # 5 
            {
                "board_to_score": [
                    None, "x", None,
                    None, "o", None,
                    None, None, None
                ],
                "expected_score": [
                    5, None, 5,
                    6, None, 6,
                    4, 5,  4,
                ],
                "expected_moves": [3,5],
                "player_args": ("o", "x")

            },
            # 6
            {
                "board_to_score": [
                    None, None, None,
                    None, None, None,
                    None, None, None
                ],
                "expected_score": [
                    3, 2, 3,
                    2, 7, 2,
                    3, 2, 3,
                ],
                "expected_moves": [4],
                "player_args": ("o", "x")

            },
            # 7
            {
                "board_to_score": [
                    "x", "o", "o",
                    "o", "x", "x",
                    "x", "x", "o"
                ],
                "expected_score": [
                    None, None, None,
                    None, None, None,
                    None, None, None,
                ],
                "expected_moves": [],
                "player_args": ("o", "x")

            },
            # 8
            {
                "board_to_score": [
                    "x", None, "x",
                    "o", "o", None,
                    None, None, "x"
                ],
                "expected_score": [
                    None, 8, None,
                    None, None, 15,
                    4, 4, None,
                ],
                "expected_moves": [5],
                "player_args": ("o", "x")

            },
            # 9 
            {
                "board_to_score": [
                    "x", None, "x",
                    None, "o", None,
                    None, None, None
                ],
                "expected_score": [
                    None, 11, None,
                    7, None, 7,
                    4, 6, 4,
                ],
                "expected_moves": [1],
                "player_args": ("o", "x")

            },
            # 10
            {
                "board_to_score": [
                    "o", "x", None,
                    None, "x", None,
                    None, None, None
                ],
                "expected_score": [
                    None, None, 4,
                    7, None, 6,
                    5, 10, 3,
                ],
                "expected_moves": [7],
                "player_args": ("o", "x")

            },
            # 11
            {
                "board_to_score": [
                    "x", None, None,
                    None, "o", None,
                    None, None, "x"
                ],
                "expected_score": [
                    None, 7, 6,
                    7, None, 7,
                    6, 7, None,
                ],
                "expected_moves": [1,3,5,7],
                "player_args": ("o", "x")

            },
            # 12 sure win for "o"
            {
                "board_to_score": [
                    "x", "o", "x",
                    "X", "o", "o",
                    None, None, "x"
                ],
                "expected_score": [
                    None, None, None,
                    None, None, None,
                    4, 11,  None,
                ],
                "expected_moves": [7],
                "player_args": ("o", "x")

            },
            # 13 I was able to win this scenrio
            {
                "board_to_score": [
                    None, None, "x",
                    None, "o", "x",
                    None, None, None
                ],
                "expected_score": [
                    5, 7, None,
                    5, None, None,
                    3, 6,  9,
                ],
                "expected_moves": [8],
                "player_args": ("o", "x")

            },
            # 14 I was able to win this scenrio
            {
                "board_to_score": [
                    None, "o", None,
                    None, "x", "x",
                    None, "o", "o"
                ],
                "expected_score": [
                    4, None, 5,
                    10, None, None,
                    9, None,  None,
                ],
                "expected_moves": [3],
                "player_args": ("x", "o")

            },
        ]

    def test_potentialboard_states(self):
        """
        Make sure AI behaves as expected for some scenario
        """
        for i, boards in enumerate(self.board_and_results):
            print "Scoring board: ", i
            board_to_score = boards['board_to_score']
            expected_score = boards['expected_score']
            expected_moves = boards['expected_moves']
            player_args = boards['player_args']
            ai_player = AIPlayer( *player_args)
            board = ai_player.score_current_board(board_to_score)
            self.assertEqual( 
                board,
                expected_score
            )

            self.assertEqual(
                ai_player.get_potential_moves(board_to_score),
                expected_moves
            )

if __name__ == '__main__':
    unittest.main()