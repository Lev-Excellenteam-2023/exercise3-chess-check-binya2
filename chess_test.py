from unittest.mock import Mock
import Piece
from enums import Player
import ai_engine
import chess_engine


# unit tests
def test_that_there_are_no_parts_to_eat_around():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Player.EMPTY
    mock_game_state.is_valid_piece = lambda row, col: False

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 0

def test_that_does_not_eat_itself():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0

def test_how_many_parts_to_eat_around():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 8

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in valid_moves

def test_that_verifies_the_locations_the_tool_can_go_to():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Player.EMPTY

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 8

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in valid_moves


def test_to_get_empty_positions_from_the_opponents_tools():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)

    assert len(valid_moves) == 0

def test_to_get_empty_locations_from_self_tools():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0

# integration tests
def Test_to_get_empty_or_full_locations_together():
    mock_game_state = Mock()
    mock_game_state.get_valid_piece_takes = [(2, 3), (2, 5), (3, 2), (3, 6) ]
    mock_game_state.get_valid_peaceful_moves = [(5, 2), (5, 6), (6, 3), (6, 5)]

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    all_moves = Piece.Knight.get_valid_piece_moves(mock_self_knight, mock_game_state)

    assert len(all_moves)  == 8
    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in all_moves

def test_several_AI_system_calculations():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)

    mock_self_ai = Mock()
    mock_self_ai.get_piece_value = lambda evaluated_piece, player: 50

    evaluation_score = ai_engine.chess_ai.evaluate_board(mock_self_ai, mock_game_state, Player.PLAYER_1)

    expected_evaluation_score = 50 * 8 * 8
    assert expected_evaluation_score == evaluation_score