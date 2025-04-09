import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display , Image, HTML

class SudokuGeneticSolver:
    def __init__(self, grid, population_size=1000, generations=3000, mutation_rate=0.3):
        self.grid = np.array(grid)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = int(population_size * 0.1)  # Legjobb 10% megőrzése

    def solve(self):
        population = self.initialize_population()

        for generation in range(self.generations):
            fitness_scores = [self.fitness(individual) for individual in population]

            if 0 in fitness_scores:
                solution_index = fitness_scores.index(0)
                return population[solution_index]

            new_population = self.create_new_generation(population, fitness_scores)
            population = new_population

        return None

    def solve_with_visualization(self):
        population = self.initialize_population()
        solutions = []  # Most már minden generációt tárolunk
        fitness_history = []

        for generation in range(self.generations):
            fitness_scores = [self.fitness(individual) for individual in population]
            fitness_history.append(min(fitness_scores))

            # Minden generációnál kiírjuk az állapotot
            print(f"Generation {generation}: Best fitness = {min(fitness_scores)}")

            # Ha megtaláltuk a megoldást
            if 0 in fitness_scores:
                solution_index = fitness_scores.index(0)
                solutions.append(population[solution_index])
                self.visualize_solution(solutions)
                self.plot_fitness_history(fitness_history)
                return population[solution_index], generation + 1

            # Új generáció létrehozása
            new_population = self.create_new_generation(population, fitness_scores)
            population = new_population

            # Minden generációt hozzáadunk az animációhoz
            best_index = fitness_scores.index(min(fitness_scores))
            solutions.append(population[best_index])

        # Ha nem találtunk megoldást, az összes állapotot vizualizáljuk
        self.visualize_solution(solutions)
        self.plot_fitness_history(fitness_history)
        return None, None

    def visualize_solution(self, solutions):
        fig, ax = plt.subplots(figsize=(8, 8))

        def is_valid_solution(state):
            for row in state:
                if len(set(row)) != 9:
                    return False
            for col in state.T:
                if len(set(col)) != 9:
                    return False
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    block = state[i:i+3, j:j+3].flatten()
                    if len(set(block)) != 9:
                        return False
            return True

        def update(frame):
            ax.clear()
            state = solutions[frame]
            
            # Rajzoljuk meg a cellák hátterét
            for i in range(9):
                for j in range(9):
                    ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, 
                                            facecolor='white' if self.grid[i, j] != 0 else '#f0f0f0',
                                            edgecolor='black',
                                            linewidth=0.5))
                    if state[i, j] != 0:
                        ax.text(j, i, str(state[i, j]), 
                               ha='center', va='center', 
                               fontsize=16,
                               color='black')
            
            # Rácsvonalak rajzolása
            for n in range(10):
                lw = 2 if n % 3 == 0 else 0.5
                ax.axhline(y=n-0.5, color='black', linewidth=lw)
                ax.axvline(x=n-0.5, color='black', linewidth=lw)
                
            ax.set_xlim(-0.5, 8.5)
            ax.set_ylim(8.5, -0.5)
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Ellenőrizzük az aktuális állapotot és frissítsük a címet
            valid = is_valid_solution(state)
            ax.set_title(f"Generation: {frame} - {'Valid' if valid else 'Invalid'}", 
                        pad=20)

        ani = animation.FuncAnimation(fig, update, frames=len(solutions), interval=500)

        try:
            display(HTML(ani.to_jshtml()))
        except NameError:
            pass

        # GIF mentése
        ani.save("sudoku_solution.gif", writer="pillow", fps=2)
        print(f"GIF saved as 'sudoku_solution.gif' with {len(solutions)} frames")
        plt.show()

    def plot_fitness_history(self, fitness_history):
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_history, label="Best Fitness")
        plt.title("Fitness Value Over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Fitness Value")
        plt.legend()
        plt.grid()
        plt.savefig("fitness_history.png")  # Save the plot as an image
        print("Fitness history plot saved as 'fitness_history.png'")
        plt.show()

    def compare_grids(self, solution):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Kezdő rács
        ax1.set_title("Initial Grid")
        for i in range(9):
            for j in range(9):
                ax1.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, 
                                        facecolor='white',
                                        edgecolor='black',
                                        linewidth=0.5))
                if self.grid[i, j] != 0:
                    ax1.text(j, i, str(self.grid[i, j]), 
                           ha='center', va='center', 
                           fontsize=16,
                           color='black')
        
        # Megoldott rács
        ax2.set_title("Solution Grid")
        for i in range(9):
            for j in range(9):
                ax2.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, 
                                        facecolor='#f0f0f0' if self.grid[i, j] == 0 else 'white',
                                        edgecolor='black',
                                        linewidth=0.5))
                ax2.text(j, i, str(solution[i, j]), 
                       ha='center', va='center', 
                       fontsize=16,
                       color='blue' if self.grid[i, j] == 0 else 'black')
        
        # Rácsvonalak mindkét táblához
        for ax in [ax1, ax2]:
            for n in range(10):
                lw = 2 if n % 3 == 0 else 0.5
                ax.axhline(y=n-0.5, color='black', linewidth=lw)
                ax.axvline(x=n-0.5, color='black', linewidth=lw)
            ax.set_xlim(-0.5, 8.5)
            ax.set_ylim(8.5, -0.5)
            ax.set_xticks([])
            ax.set_yticks([])
        
        plt.savefig("sudoku_comparison.png", bbox_inches='tight', dpi=150)
        print("Comparison image saved as 'sudoku_comparison.png'")
        plt.show()

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = self.fill_grid_randomly(self.grid.copy())
            population.append(individual)
        return population

    def fill_grid_randomly(self, grid):
        for row in range(9):
            missing_numbers = [num for num in range(1, 10) if num not in grid[row]]
            random.shuffle(missing_numbers)
            for col in range(9):
                if grid[row][col] == 0:
                    grid[row][col] = missing_numbers.pop()
        return grid

    def fitness(self, individual):
        fitness = 0
        for row in individual:
            fitness += 9 - len(set(row))
        for col in individual.T:
            fitness += 9 - len(set(col))
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = individual[i:i+3, j:j+3].flatten()
                fitness += 9 - len(set(block))
        return fitness

    def create_new_generation(self, population, fitness_scores):
        new_population = []
        
        # Elitizmus - legjobb egyedek megőrzése
        elite_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i])[:self.elite_size]
        elites = [population[i] for i in elite_indices]
        new_population.extend(elites)
        
        # Populáció feltöltése új egyedekkel
        selected = self.select_population(population, fitness_scores)
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = self.crossover(parent1, parent2)
            if random.random() < self.mutation_rate:
                child = self.mutate(child)
            new_population.append(child)
        
        return new_population

    def select_population(self, population, fitness_scores):
        # Tournament selection implementálása
        tournament_size = 5
        selected = []
        for _ in range(self.population_size // 2):
            tournament = random.sample(list(enumerate(fitness_scores)), tournament_size)
            winner_idx = min(tournament, key=lambda x: x[1])[0]
            selected.append(population[winner_idx])
        return selected

    def crossover(self, parent1, parent2):
        child = parent1.copy()
        for row in range(9):
            if random.random() > 0.5:
                child[row] = parent2[row]
        return child

    def mutate(self, individual):
        mutated = individual.copy()
        for row in range(9):
            if random.random() < self.mutation_rate:
                empty_positions = [i for i in range(9) if self.grid[row][i] == 0]
                if len(empty_positions) > 1:
                    # Több pozíció cseréje egy sorban
                    num_swaps = random.randint(1, min(3, len(empty_positions) // 2))
                    for _ in range(num_swaps):
                        pos1, pos2 = random.sample(empty_positions, 2)
                        mutated[row][pos1], mutated[row][pos2] = mutated[row][pos2], mutated[row][pos1]
        return mutated


if __name__ == "__main__":
    grid = [
        [9, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 5, 0, 0, 9],
        [0, 0, 0, 3, 9, 0, 0, 7, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 1, 0, 0, 6],
        [7, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 3, 0, 2],
        [0, 0, 0, 0, 0, 0, 1, 0, 7],
        [0, 7, 0, 0, 0, 9, 0, 0, 0]
    ]

    solver = SudokuGeneticSolver(grid)
    solution, generation = solver.solve_with_visualization()

    if solution is not None:
        print("Sudoku solved!")
        print(np.array(solution))
        print(f"Solved in {generation} generations.")
        solver.compare_grids(solution)  # Új összehasonlító kép generálása
    else:
        print("No solution found.")