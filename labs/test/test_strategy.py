from src.strategy import Strategy
from src.game import Game
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