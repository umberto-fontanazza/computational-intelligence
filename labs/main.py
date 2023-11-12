from state import State


def main():
    initial_state = State()
    steps = 100

    current_state, current_fitness = initial_state, initial_state.fitness()
    for _ in range(steps):
        # 1 + 3 evolution strategy
        parent = current_state
        for i in range(3):
            child = parent.mutate()
            child_fit = child.fitness()
            if(child_fit > current_fitness):
                current_state = child
                current_fitness = child_fit

if __name__ == '__main__':
    main()