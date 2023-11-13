from src.strategy import Strategy
from src.game import Game

def main():
    player = Strategy.expert_system()
    opponent = Strategy.gabriele()
    g = Game(4, player, opponent, True)
    g.play(logging=True)

if __name__ == '__main__':
    main()