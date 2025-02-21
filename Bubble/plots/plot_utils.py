import matplotlib.pyplot as plt

def plot_ts_vs_frequency(frequencies, ts_results, discrete_frequencies=None, discrete_labels=None):
    """
    Plot Target Strength (TS) versus frequency on a logarithmic x-axis using Matplotlib.

    Parameters:
    -----------
    frequencies : array-like
        Frequencies in kHz.
    ts_results : dict
        Dictionary containing TS results for each model.
    discrete_frequencies : list, optional
        Specific user-provided discrete frequencies to highlight.
    discrete_labels : list, optional
        Labels for the discrete frequencies.
    """
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot TS vs. frequency for each model
    for model, ts_values in ts_results.items():
        ax.semilogx(frequencies, ts_values, label=model, linestyle='-', linewidth=2)

    # Highlight discrete frequencies
    if discrete_frequencies:
        for freq, label in zip(discrete_frequencies, discrete_labels):
            ax.axvline(x=freq, color='gray', linestyle='--', alpha=0.5)
            ax.text(freq, min(ts_values), label, rotation=90, verticalalignment='bottom', fontsize=10)

    # Add labels and title
    ax.set_xlabel("Frequency (kHz)", fontsize=12)
    ax.set_ylabel("Target Strength (TS) [dB]", fontsize=12)
    ax.set_title("Target Strength vs Frequency", fontsize=14)

    # Add grid and legend
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend(title="Model", fontsize=10, title_fontsize=12)

    # Save the plot to a file
    plt.savefig("ts_vs_frequency_plot.png", dpi=300, bbox_inches="tight")
    
    # Close the plot to free up memory
    plt.close()