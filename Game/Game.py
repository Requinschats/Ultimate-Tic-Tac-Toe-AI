import time

import Game.selectors as s
import Game.outputs as o
import Game.constants as c

import game_traces.outputs as go


class Game:
    MINIMAX, ALPHABETA = 0, 1
    HUMAN, AI = 2, 3
    statistics = {}

    def __init__(self, board_parameters, recommend=True, heuristics=None):
        self.initialize_game(board_parameters)
        self.recommend = recommend
        self.statistics = s.select_initial_statistics()
        self.heuristics = heuristics

    def initialize_game(self, board_parameters):
        self.current_state = s.select_initial_state(board_parameters)
        self.player_turn = s.select_initial_player()

    def is_valid_move(self, px, py, board_parameters):
        return s.select_is_valid_move(self, px, py, board_parameters)

    def check_end(self, board_parameters):
        self.result = s.select_is_end_token(self, board_parameters)
        end_game_output = s.select_end_game_output(self)
        if end_game_output:
            print(end_game_output)
        return self.result

    def input_move(self, board_parameters):
        while True:
            px, py = o.input_coordinates(self)
            if self.is_valid_move(px, py, board_parameters):
                return px, py
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        return s.select_next_player(self)

    def add_evaluation_time(self, start_time):
        self.statistics["evaluation_times"].append(time.time() - start_time)

    def turn_index(self):
        return self.statistics["move_count"]

    def increment_states_count(self):
        if self.turn_index() in self.statistics["states_evaluated"]:
            self.statistics["states_evaluated"][self.turn_index()] += 1
        else:
            self.statistics["states_evaluated"][self.turn_index()] = 0

    def increment_depth_state_count(self, depth):
        if depth in self.statistics["state_count_per_depth"]:
            self.statistics["state_count_per_depth"][depth] += 1
        else:
            self.statistics["state_count_per_depth"][depth] = 1

    def increment_move_count(self):
        self.statistics["move_count"] += 1

    def add_depth_state_evaluation(self, depth):
        self.statistics["average_move_depths"].append(depth)

    def average_move_depths(self):
        self.statistics["average_move_depths"] = s.select_list_average(
            self.statistics["average_move_depths"])

    def update_statistics_after_state_evaluation(self, state_evaluation_start_time, current_depth):
        self.increment_states_count()
        self.add_evaluation_time(start_time=state_evaluation_start_time)
        self.increment_depth_state_count(depth=current_depth)
        self.add_depth_state_evaluation(current_depth)

    def set_current_state(self, x_coordinate, y_coordinate, player_turn):
        self.current_state[y_coordinate][x_coordinate] = player_turn

    def select_next_best_state(self, current_coordinates,
                               best_coordinates, child_minimax_result, best_value, current_depth,
                               is_max):
        x_evaluate, y_evaluate = current_coordinates
        x_best, y_best = best_coordinates

        if (is_max and child_minimax_result > best_value) or (
                not is_max and child_minimax_result < best_value):
            best_value = child_minimax_result
            x_best, y_best = x_evaluate, y_evaluate
        return best_value, x_best, y_best

    def select_maximum_depth(self, maximum_depths):
        return maximum_depths[0] if self.player_turn == c.X_TOKEN else maximum_depths[1]

    def minimax(self, is_max=False, board_parameters=None, current_depth=0, start_time=None):
        board_size, blocks, winning_line_size, maximum_depths, maximum_computing_time = board_parameters
        best_value = c.HEURISTIC_MIN_DEFAULT_VALUE if not is_max else c.HEURISTIC_MAX_DEFAULT_VALUE
        top_x_coordinate, top_y_coordinate = None, None

        for y_coordinate_evaluate in range(board_size):
            for x_coordinate_evaluate in range(board_size):
                if s.select_is_empty_position(
                        self.current_state[y_coordinate_evaluate][x_coordinate_evaluate]):
                    self.set_current_state(x_coordinate_evaluate, y_coordinate_evaluate,
                                           self.player_turn if is_max else s.select_opposite_player(
                                               self.player_turn))

                    maximum_depth = self.select_maximum_depth(maximum_depths)
                    child_value = s.select_mini_max_child_value(self,
                                                                (False if is_max else True,
                                                                 board_parameters,
                                                                 current_depth + 1, start_time),
                                                                (current_depth, maximum_depth))
                    best_value, top_x_coordinate, top_y_coordinate = self.select_next_best_state(
                        (x_coordinate_evaluate, y_coordinate_evaluate),
                        (top_x_coordinate, top_y_coordinate),
                        child_value, best_value, current_depth,
                        is_max)
                    self.current_state[y_coordinate_evaluate][x_coordinate_evaluate] = c.EMPTY_TOKEN
        return best_value, top_x_coordinate, top_y_coordinate

    def alphabeta(self, alpha=c.HEURISTIC_MAX_DEFAULT_VALUE, beta=c.HEURISTIC_MIN_DEFAULT_VALUE,
                  is_max=False, board_parameters=None, current_depth=0, start_time=None):
        board_size, blocks, winning_line_size, maximum_depths, maximum_computing_time = board_parameters
        best_value = c.HEURISTIC_MIN_DEFAULT_VALUE if not is_max else c.HEURISTIC_MAX_DEFAULT_VALUE
        top_x_coordinate, top_y_coordinate = None, None

        for y_coordinate_evaluate in range(board_size):
            for x_coordinate_evaluate in range(board_size):
                current_position = self.current_state[y_coordinate_evaluate][x_coordinate_evaluate]
                is_empty = s.select_is_empty_position(current_position)
                if is_empty:
                    self.set_current_state(x_coordinate_evaluate, y_coordinate_evaluate,
                                           self.player_turn if is_max else s.select_opposite_player(
                                               self.player_turn))
                    maximum_depth = self.select_maximum_depth(maximum_depths)
                    child_result = s.select_alpha_beta_child_value(alpha, beta, self,
                                                                   (False if is_max else True,
                                                                    board_parameters,
                                                                    current_depth + 1, start_time),
                                                                   (current_depth,
                                                                    maximum_depth))
                    best_value, top_x_coordinate, top_y_coordinate = self.select_next_best_state(
                        (x_coordinate_evaluate, y_coordinate_evaluate),
                        (top_x_coordinate, top_y_coordinate),
                        child_result, best_value,
                        current_depth,
                        is_max)
                    self.current_state[y_coordinate_evaluate][x_coordinate_evaluate] = c.EMPTY_TOKEN

                    if is_max:
                        if best_value >= beta: return best_value, top_x_coordinate, top_y_coordinate
                        if best_value > alpha: alpha = best_value
                    else:
                        if best_value <= alpha: return best_value, top_x_coordinate, top_y_coordinate
                        if best_value < beta: beta = best_value
        return best_value, top_x_coordinate, top_y_coordinate

    def finish_turn(self, x, y, file, board_parameters):
        self.current_state[y][x] = self.player_turn
        go.output_turn_statistics(file, self.statistics, (x, y))
        go.output_move_to_game_trace(file, self, board_parameters)
        self.increment_move_count()
        self.switch_player()

    def handle_end_game(self, file, board_parameters):
        game_result = self.check_end(board_parameters=board_parameters)
        if game_result:
            self.average_move_depths()
            go.output_game_trace_end(file, game_result, self.statistics)
            if self.result is not None:
                self.initialize_game(board_parameters)
        return game_result

    def play(self, algo=None, player_x=None, player_o=None, board_parameters=None,
             mock_inputs=None, file=None):
        algo, player_x, player_o = s.select_play_initial_values(self, algo, player_x, player_o)
        x, y = None, None

        go.output_game_trace_initial_values(file, board_parameters, (player_x, player_o, algo),
                                            self)

        while True:
            if not mock_inputs: o.draw_game_board(self, board_parameters)

            game_result = self.handle_end_game(file, board_parameters)
            if game_result: return self.statistics, game_result

            if s.select_is_human_turn(self, player_x, player_o):
                (x, y) = s.select_human_turn_move(self, mock_inputs, board_parameters, (x, y))

            if s.select_is_ai_turn(self, player_x, player_o):
                start_time = time.time()
                (m, x, y) = s.select_heuristic_move(board_parameters, algo, self)
                o.output_ai_turn_recommend(start_time, self, x, y)

            self.finish_turn(x=x, y=y, file=file, board_parameters=board_parameters)
