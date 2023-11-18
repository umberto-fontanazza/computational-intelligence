from src.strategy import Strategy
from src.game import Game

def main():
    player = Strategy.expert_system()
    opponent = Strategy.gabriele()
    g = Game(4, player, opponent, False)
    g.play(logging=True)
    print(f'{'player' if g.player_wins() else 'opponent'} wins')

if __name__ == '__main__':
    main()