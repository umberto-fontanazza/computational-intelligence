from state import State
from queue import PriorityQueue
from problem_data import SETS

def main():
    frontier = PriorityQueue()
    current_state = State.initial(SETS)
    frontier.put((current_state.estimated_total_cost(), current_state))

    while not current_state.is_solution():
        for covering_set in current_state.not_taken:
            adjacent_state : State = current_state.take_covering_set(covering_set)
            frontier.put((adjacent_state.estimated_total_cost(), adjacent_state))
        current_state = frontier.get()

    print('Solution found')
    print(current_state)

if __name__ == '__main__':
    main()