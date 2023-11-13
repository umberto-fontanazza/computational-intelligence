from src.state import State

def main():
    initial_state = State()
    steps = 100

    current_state, current_fitness = initial_state, initial_state.fitness()
    print(current_state)
    for _ in range(steps):
        # 1 + 3 evolution strategy
        parent = current_state
        μ, λ = 1, 3
        for i in range(λ):
            child = parent.mutate()
            child_fit = child.fitness()
            if(child_fit > current_fitness):
                current_state = child
                current_fitness = child_fit
        print(f'Fit: {current_fitness}')
    print(current_state)

if __name__ == '__main__':
    main()