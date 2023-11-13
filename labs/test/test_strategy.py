from src.strategy import Strategy
from src.game import Game

def test_gabriele_vs_expert_system():
    player = Strategy.gabriele()
    opponent = Strategy.expert_system()
    testgame = Game(4, player, opponent, True)
    assert testgame.player_wins() == True

def test_exepert_system_vs_gabriele():
    player = Strategy.expert_system()
    opponent = Strategy.gabriele()
    testgame = Game(4, player, opponent, True)
    assert testgame.player_wins() == True