import pandas as pd
from soduko_solver import SudokuGeneticSolver
import time
import matplotlib.pyplot as plt

def test_solver_with_params(grid, population_sizes=[100, 500, 1000, 3000, 5000]):
    results = []
    
    for pop_size in population_sizes:
        print(f"\nTesting with population size: {pop_size}")
        solver = SudokuGeneticSolver(
            grid=grid,
            population_size=pop_size,
            generations=1000,
            mutation_rate=0.4
        )
        
        # Csak a solve függvény futási idejét mérjük
        start_time = time.time()
        solution, generations = solver.solve_with_visualization()  # Ez használja a restart mechanizmust
        elapsed_time = time.time() - start_time
        
        result = {
            'Population Size': pop_size,
            'Elite Size': int(pop_size * 0.1),
            'Found Solution': solution is not None,
            'Generations': generations if generations else 'N/A',
            'Time (seconds)': round(elapsed_time, 2),
            'Success Rate': 'Success' if solution is not None else 'Failed'
        }
        results.append(result)
    
    # Eredmények DataFrame-be rendezése
    df = pd.DataFrame(results)
    
    # Táblázat vizualizálása és mentése PNG-ként
    plt.figure(figsize=(12, 4))
    table = plt.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        colColours=['#f2f2f2'] * len(df.columns)
    )
    
    # Táblázat formázása
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    plt.axis('off')
    plt.title('Sudoku Solver Test Results', pad=20)
    
    # Csak PNG mentése
    plt.savefig('sudoku_test_results.png', 
                bbox_inches='tight', 
                dpi=300,
                facecolor='white')
    plt.close()
    
    # Eredmények megjelenítése konzolon
    print("\nTest Results:")
    print(df.to_string())
    
    return df

if __name__ == "__main__":
    grid = [
        [0, 0, 0, 6, 7, 8, 0, 1, 2],
        [6, 0, 2, 1, 9, 5, 0, 4, 0],
        [1, 9, 0, 0, 4, 2, 5, 6, 0],
        [8, 5, 9, 0, 6, 1, 0, 2, 3],
        [4, 2, 0, 8, 5, 3, 0, 9, 1],
        [0, 1, 3, 0, 2, 4, 8, 0, 6],
        [9, 0, 1, 0, 3, 7, 2, 8, 0],
        [2, 0, 7, 4, 1, 9, 0, 3, 5],
        [3, 0, 5, 2, 0, 6, 1, 0, 9]
    ]
    
    # Különböző populáció méretekkel való tesztelés
    results_df = test_solver_with_params(
        grid,
        population_sizes=[100, 500, 1000, 3000, 5000]  # Módosított populáció méretek
    )