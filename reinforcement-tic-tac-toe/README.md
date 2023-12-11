## TODO

- Make model incremental (add method to export q_table and constructor from exported q_table)
- Use epsilon and make it self adaptive. Gamma and alpha should be made self adaptive as well.
- Add an optimal policy to train the agent against
- Improve the testing
- Add benchmarks

A qtable fully represents the learning done by the agent, the table is clearly incremental since the update formula is known. 

Open question:
is it possible to merge two q tables in a meaningful way? [Average of q values weighted by the number of games played? Averaged by the number of upates to that specific q value?]