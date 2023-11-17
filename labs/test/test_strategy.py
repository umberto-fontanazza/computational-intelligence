from src.strategy import Strategy
from src.game import Game
from src.nim import Nim
from src.nim import Move
from itertools import product

def test_gabriele_vs_expert_system():
    player = Strategy.expert_system()
    opponent = Strategy.gabriele()
    testgame = Game(4, player, opponent, play_first = False)
    assert testgame.player_wins() == True

def test_exepert_system_vs_gabriele():
    player = Strategy.expert_system()
    opponent = Strategy.gabriele()
    test_game = Game(4, player, opponent, play_first = True)
    assert test_game.player_wins() == True

def test_expert_system_vs_gabriele_100():
    '''Make es play versus Gabriele 100 times, 50 for each starting player'''
    games_number = 100
    player = Strategy.expert_system()
    opponent = Strategy.gabriele()
    total_victories, total_played_games = 0, 0
    for player_starts, _ in product([True, False], range(games_number // 2)):
        game = Game(4, player, opponent, play_first = player_starts)
        total_played_games += 1
        if game.player_wins():
            total_victories += 1
    assert total_played_games == games_number
    assert total_victories >= 50

def test_expert_system_several():
    expert_system = Strategy.expert_system()
    best_moves = (
        ([1, 3, 5, 1], Move(2, 2)),
        ([0, 0, 4, 2], Move(2, 2)),
        ([1, 3, 3, 6], Move(3, 5)),
        ([1, 3, 1, 6], Move(3, 3))
    )

    for state, best_move in best_moves:
        nim = Nim.from_rows(state)
        es_move = expert_system.make_move(nim)
        assert es_move == best_move

def test_expert_system_limit_case():
    expert_system = Strategy.expert_system()
    best_moves = [
        (Nim.from_rows([0, 1, 1, 2]), Move(3, 1)),
        (Nim.from_rows([1, 1, 1, 2]), Move(3, 2))
    ]

    for nim, best_move in best_moves:
        es_move = expert_system.make_move(nim)
        assert es_move == best_move