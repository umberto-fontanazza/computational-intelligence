from src.state import State
from src.state import Action

def test_state_actions():
    s = State(( ('_', 'O', 'X'),
                ('X', '_', '_'),
                ('_', 'X', 'O')), 'O')
    assert s.actions == ((0, 0), (1, 1), (1, 2), (2, 0))

def test_apply_action():
    s = State(( ('_', 'O', 'X'),
                ('O', '_', 'X'),
                ('_', 'X', 'O')), 'X')
    assert s.apply((0, 0)) == State((   ('X', 'O', 'X'),
                                        ('O', '_', 'X'),
                                        ('_', 'X', 'O')), 'O')

def test_no_action():
    s = State(( ('O', 'X', 'X'),
                ('X', 'O', 'O'),
                ('X', 'X', 'O')), 'O')
    assert len(s.actions) == 0

def test_game_over():
    s = State((('X', 'O', '_'), ('_', 'X', 'O'), ('O', '_', 'X')), 'O')
    assert s.game_over

def test_winner_X_wins():
    s = State((('X', 'O', '_'), ('_', 'X', 'O'), ('O', '_', 'X')), 'O')
    assert s.winner == 'X'