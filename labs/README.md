The goal of the lab is to develop an evolutionary strategy able to identify the best strategy among a range of possible strategies to play Nim.
In this case the strategy is intended as a criterion for making a move. The state of the problem therefore is not the state of the Nim game, instead it is an array of probabilities associated with the various strategies and the initial state is a uniform distribution of probability to use each of the strategies.

The fitness function therefore arranges a certain amount of matches and evaluates win and losses using for each mach a strategy extracted from the pool of strategies with the probability of extraction given by the state.


## How expert systems calculates ply to leave nim sum == 0

If and only if the current nim configuration is unstable (nim_sum != 0) it can become stable.
Since the nim_sum is the xor of all the rows and only one row can change in a turn we need to change the bits of such row so that the nim sum become zero.

Let me give some names

R: the row before the subtraction
R': the row after the subtraction
P: the number of matchsticks removed
N: current nim sum

To make the configuration stable the bits in the row that must change after the subtraction are those and only those of the nim sum. XOR operator detects bitwise change.

This means R XOR R' = N --> R' = N XOR R
R' is obtained with a subtraction from the row: R - P = R' --> P = R - R'

We put toghether the 2 equations above and get:
P = R - (N XOR R)

We just need to check the constraint 0 < P <= R and we found the best move