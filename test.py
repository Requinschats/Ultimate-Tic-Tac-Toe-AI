from Game.Game import Game
import Game.outputs as o
import Game.mocks as m

board_parameters = m.input_mock_game_settings()
game = Game(board_parameters=board_parameters, recommend=True)


def test_diagonal_win():
    return game.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN,
                     board_parameters=board_parameters,
                     mock_inputs=[[1, 1], [1, 2], [2, 2], [1, 3], [3, 3]])


def test_row_win():
    return game.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN,
                     board_parameters=board_parameters,
                     mock_inputs=[[1, 3], [1, 2], [2, 3], [1, 3], [3, 3]])


def test_column_win():
    return game.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN,
                     board_parameters=board_parameters,
                     mock_inputs=[[1, 0], [0, 2], [1, 1], [0, 3], [1, 2]])


def test_minimax_maximum_depth_reached():
    return game.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI,
                     board_parameters=m.input_mock_game_settings_short_depth())


def test_minimax_maximum_computing_time_reached():
    return game.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI,
                     board_parameters=m.input_mock_game_settings_short_computing_time())


# game rules
test_diagonal_win()
test_row_win()
test_column_win()

# heuristic constraints
test_minimax_maximum_depth_reached()
# test_minimax_maximum_computing_time_reached()
