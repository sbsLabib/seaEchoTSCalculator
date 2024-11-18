import matplotlib.pyplot as plt

def plot_ts_vs_frequency(frequencies, ts_results, labels):
    """
    Plot Target Strength results versus frequency on a linear x-axis.

    Parameters:
    -----------
    frequencies : array-like
        Frequency values (kHz).
    ts_results : dict
        Dictionary containing TS results for each model.
    labels : list of str
        Labels for each TS result (e.g., models or conditions).
    """
    plt.figure(figsize=(8, 6))
    
    for model, ts_values in ts_results.items():
        plt.plot(frequencies, ts_values, label=model)
    
    plt.xlabel("Frequency (kHz)", fontsize=14)
    plt.ylabel("Target Strength (TS, dB)", fontsize=14)
    plt.title("Target Strength vs. Frequency", fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()  # Show the plot interactively instead of saving
