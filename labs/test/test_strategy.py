# TODO: write tests
from src.strategy import Strategy

def test_exeprt_system_vs_gabriele():
    es = Strategy.expert_system()
    gabriele = Strategy.gabriele()
    assert es is not None