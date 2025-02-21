# core/plotter.py
import numpy as np
from plots.plot_utils import plot_ts_vs_frequency

def plot_results(data):
    """Main plotting function."""
    params = data['params']
    results = data['results']
    
    # Call with corrected parameter names
    plot_ts_vs_frequency(
        frequencies=params['frequencies'],
        ts_results=results['ts'],
        discrete_frequencies=params['freq_discrete'],
        discrete_labels=[f"{f} kHz" for f in params['freq_discrete']]
    )
    
    _print_discrete_results(data)


def _print_discrete_results(data):
    """Print results for discrete frequencies."""
    params = data['params']
    results = data['results']
    
    # Convert to numpy array if needed
    freqs_array = np.array(params['frequencies'])
    
    print("\n=== Discrete Frequency Results ===")
    for f in params['freq_discrete']:
        print(f"\nFrequency: {f} kHz")
        idx = np.argmin(np.abs(freqs_array - f))
        
        for model in params['models']:
            ts_value = results['ts'][model][idx]
            print(f"  {model}: {float(ts_value):.2f} dB")