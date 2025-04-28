import os
import matplotlib.pyplot as plt

def plot_ts_vs_frequency(frequencies, ts_results, labels,
                         filename="ts_vs_frequency_sphere.png"):
    """
    Plot Target Strength results versus frequency on a linear x-axis and save it.
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

    # __file__ is …/SolidSphere/plots/plot_utils.py
    # Go up two dirs to reach …/SolidSphere
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base_dir, filename)
    
    # Make sure the directory exists (should, but just in case)
    os.makedirs(base_dir, exist_ok=True)

    plt.savefig(save_path)
    plt.close()
    # If you still want to pop up the window when debugging:
    plt.show()