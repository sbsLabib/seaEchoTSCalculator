# main.py
from core.cli import get_user_input
from core.processor import run_calculations
from core.plotter import plot_results

def main():
    # Get parameters from user
    params = get_user_input()
    
    # Run TS calculations
    results = run_calculations(params)
    
    # Visualize and report results
    plot_results(results)

if __name__ == "__main__":
    main()