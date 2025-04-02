import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display , Image, HTML

class SudokuGeneticSolver:
    def __init__(self, grid, population_size=200, generations=2000, mutation_rate=0.5): #100,1000,0.1 default
        self.grid = np.array(grid)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

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
        solutions = []

        for generation in range(self.generations):
            fitness_scores = [self.fitness(individual) for individual in population]

            if 0 in fitness_scores:
                solution_index = fitness_scores.index(0)
                solutions.append(population[solution_index])
                self.visualize_solution(solutions)
                return population[solution_index], generation + 1  # Visszaadjuk a generáció számát

            new_population = self.create_new_generation(population, fitness_scores)
            population = new_population

            # Mentjük a populáció legjobb egyedét a vizualizációhoz
            best_index = fitness_scores.index(min(fitness_scores))
            solutions.append(population[best_index])

        self.visualize_solution(solutions)
        return None, None  # Ha nincs megoldás, None-t adunk vissza

    def visualize_solution(self, solutions):
        fig, ax = plt.subplots()

        def is_valid_solution(state):
            # Ellenőrizzük, hogy az aktuális állapot megfelel-e a Sudoku szabályainak
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
            ax.imshow(np.ones((9, 9)), cmap='gray', alpha=0.3)
            state = solutions[frame]
            for i in range(9):
                for j in range(9):
                    if state[i, j] != 0:
                        ax.text(j, i, str(state[i, j]), ha='center', va='center', fontsize=16)
            ax.set_xticks([])
            ax.set_yticks([])

            # Ellenőrizzük, hogy az aktuális állapot helyes-e
            valid = is_valid_solution(state)
            ax.set_title(f"Generation: {frame + 1} - {'Valid' if valid else 'Invalid'}")

        ani = animation.FuncAnimation(fig, update, frames=len(solutions), interval=500)

        # Megjelenítés Jupyter Notebookban (ha szükséges)
        try:
            display(HTML(ani.to_jshtml()))
        except NameError:
            pass

        # GIF mentés
        ani.save("sudoku_solution.gif", writer="pillow", fps=2)
        print("GIF saved as 'sudoku_solution.gif'")
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
        selected = self.select_population(population, fitness_scores)
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = self.crossover(parent1, parent2)
            new_population.append(child)
        new_population = [self.mutate(individual) for individual in new_population]
        return new_population

    def select_population(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        probabilities = [1 - (score / total_fitness) for score in fitness_scores]
        probabilities = [p / sum(probabilities) for p in probabilities]
        selected = random.choices(population, weights=probabilities, k=self.population_size // 2)
        return selected

    def crossover(self, parent1, parent2):
        child = parent1.copy()
        for row in range(9):
            if random.random() > 0.5:
                child[row] = parent2[row]
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            row = random.randint(0, 8)
            cols = [col for col in range(9) if self.grid[row][col] == 0]
            if len(cols) > 1:
                col1, col2 = random.sample(cols, 2)
                individual[row][col1], individual[row][col2] = individual[row][col2], individual[row][col1]
        return individual


if __name__ == "__main__":
    grid = [
        [0, 3, 4, 6, 7, 8, 9, 1, 0],
        [6, 0, 2, 1, 0, 5, 3, 0, 8],
        [1, 9, 0, 3, 4, 2, 0, 6, 7],
        [8, 5, 9, 0, 6, 0, 4, 2, 3],
        [0, 2, 0, 8, 0, 3, 0, 9, 0],
        [7, 1, 3, 0, 2, 0, 8, 5, 6],
        [9, 6, 0, 5, 0, 7, 0, 8, 4],
        [2, 0, 7, 4, 1, 9, 6, 0, 5],
        [0, 4, 5, 2, 0, 6, 1, 7, 0]
    ]

    solver = SudokuGeneticSolver(grid)
    solution, generation = solver.solve_with_visualization()

    if solution is not None:
        print("Sudoku solved!")
        print(np.array(solution))
        print(f"Solved in {generation} generations.")
    else:
        print("No solution found.")