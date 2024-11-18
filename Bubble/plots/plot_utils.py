import matplotlib.pyplot as plt
import numpy as np

def plot_ts_vs_ka(ka_values, ts_results, discrete_ka_values=None, discrete_labels=None):
    """
    Plot Target Strength (TS) results versus ka on a logarithmic x-axis.

    Parameters:
    -----------
    ka_values : array-like
        ka values (dimensionless).
    ts_results : dict
        Dictionary containing TS results for each model.
    discrete_ka_values : array-like, optional
        Specific ka values to highlight.
    discrete_labels : list of str, optional
        Labels corresponding to discrete ka values.
    """
    plt.figure(figsize=(10, 6))

    # Plot each model
    for model, ts_values in ts_results.items():
        plt.plot(ka_values, ts_values, label=model)

    # Highlight discrete points
    if discrete_ka_values is not None and discrete_labels is not None:
        for ka, label in zip(discrete_ka_values, discrete_labels):
            for model, ts_values in ts_results.items():
                idx = np.argmin(np.abs(ka_values - ka))  # Find closest ka
                ts_value = ts_values[idx]
                plt.scatter(ka, ts_value, label=f"{model} @ {label}", marker="o")

    # Formatting
    plt.xscale("log")
    plt.xlabel(r"$ka$ (dimensionless)")
    plt.ylabel("Target Strength (dB)")
    plt.title("Target Strength vs $ka$")
    plt.legend()
    plt.grid(True)
    plt.savefig("ts_vs_ka_plot.png")
    plt.show()
