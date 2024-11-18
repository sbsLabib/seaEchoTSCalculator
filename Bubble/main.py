import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from utils.physical_properties import sound_speed
from models.breathing_model import calculate_breathing_ts
from models.thuraisingham_model import calculate_thuraisingham_ts
from models.modal_solution import calculate_modal_ts
from models.medwin_clay_model import calculate_medwin_clay_ts
from utils.SeaEcho_water_bubble import seawater, air_bubble
from plots.plot_utils import plot_ts_vs_ka


def get_user_input():
    """
    Gather user input for frequency range, discrete frequencies, and seawater properties.
    """
    print("=== Target Strength Computation ===")

    # Frequency range input
    freq_range = input("Enter frequency range (e.g., 10-50 kHz): ")
    f_min, f_max = map(float, freq_range.split("-"))
    steps = int(input("Enter the number of steps between the range: "))
    freq_range_values = np.linspace(f_min, f_max, steps)

    # Discrete frequency input
    freq_discrete_input = input("Enter discrete frequencies (e.g., 30, 45 kHz): ")
    if freq_discrete_input.strip():
        freq_discrete_values = list(map(float, freq_discrete_input.split(",")))
    else:
        freq_discrete_values = []

    # Combine range and discrete frequencies
    frequencies = sorted(list(set(freq_range_values).union(set(freq_discrete_values))))

    # Seawater properties
    T = float(input("Enter temperature (°C): "))
    S = float(input("Enter salinity (psu): "))
    z = float(input("Enter depth (m): "))

    # Bubble diameter
    d_mm = float(input("Enter bubble diameter (mm): "))  # Input in mm
    d = d_mm / 1000  # Convert to meters (store internally as diameter)

    return frequencies, freq_discrete_values, T, S, z, d


def process_frequency(f, c, water, bubble):
    """
    Compute Target Strength (TS) for a given frequency using all models.

    Parameters:
    -----------
    f : float
        Frequency in kHz.
    c : float
        Speed of sound in seawater (m/s).
    water : object
        Seawater properties.
    bubble : object
        Bubble properties.

    Returns:
    --------
    dict
        Computed TS values for each model and the ka value.
    """
    k = 2 * np.pi * f * 1000 / c  # Wave number in water
    a = bubble.d / 2  # Bubble radius
    ka = k * a

    # Compute TS using different models
    ts_values = {
        "ka": ka,
        "Medwin_Clay": calculate_medwin_clay_ts(f, c, water, bubble),
        "Breathing": calculate_breathing_ts(f, c, water, bubble),
        "Thuraisingham": calculate_thuraisingham_ts(f, c, water, bubble),
        "Modal": calculate_modal_ts(f, c, water, bubble),
    }
    return ts_values


def main():
    """
    Main function for computing Target Strength using various models.
    """
    # Get user input
    frequencies, freq_discrete_values, T, S, z, d = get_user_input()

    # Create seawater and bubble objects
    water = seawater(T, z, S)
    bubble = air_bubble(water, T, z, S, d)  # Pass diameter directly

    # Compute sound speed
    c = sound_speed(T, S, z)

    # Prepare results storage
    ts_results = {
        "Medwin_Clay": [],
        "Breathing": [],
        "Thuraisingham": [],
        "Modal": [],
    }
    ka_values = []

    # Parallel processing of frequencies
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_frequency, frequencies, [c] * len(frequencies), [water] * len(frequencies), [bubble] * len(frequencies)))

    # Collect results
    for res in results:
        ka_values.append(res["ka"])
        ts_results["Medwin_Clay"].append(res["Medwin_Clay"])
        ts_results["Breathing"].append(res["Breathing"])
        ts_results["Thuraisingham"].append(res["Thuraisingham"])
        ts_results["Modal"].append(res["Modal"])

    # Convert results to numpy arrays
    ka_values = np.array(ka_values)
    for key in ts_results:
        ts_results[key] = np.array(ts_results[key])

    # Plot results
    plot_results(ka_values, freq_discrete_values, ts_results, c, bubble)


def plot_results(ka_values, freq_discrete_values, ts_results, c, bubble):
    """
    Plot Target Strength results versus ka on a logarithmic x-axis.

    Parameters:
    -----------
    ka_values : array-like
        ka values (dimensionless).
    freq_discrete_values : list
        Specific user-provided discrete frequencies to highlight.
    ts_results : dict
        Dictionary containing TS results for each model.
    c : float
        Speed of sound in seawater (m/s).
    bubble : object
        Bubble properties, needed to calculate ka for discrete frequencies.
    """
    # Prepare labels for discrete frequencies
    discrete_ka_values = []
    discrete_labels = []
    if freq_discrete_values:
        for f in freq_discrete_values:
            ka = 2 * np.pi * f * 1000 / c * (bubble.d / 2)  # Calculate k * a
            discrete_ka_values.append(ka)
            discrete_labels.append(f"{f} kHz")
            print(f"DEBUG: Discrete Frequency {f} kHz -> k*a = {ka:.4f}")

    # Call the plotting utility
    plot_ts_vs_ka(ka_values, ts_results, discrete_ka_values, discrete_labels)

    # Print results for discrete frequencies
    print("\n=== Results for Discrete Frequencies ===")
    for f, ka in zip(freq_discrete_values, discrete_ka_values):
        print(f"Discrete Frequency: {f} kHz (ka={ka:.2f})")
        for model, ts_values in ts_results.items():
            idx = np.argmin(np.abs(ka_values - ka))
            ts_value = ts_values[idx]
            # Convert ts_value to float to avoid mpf formatting issues
            print(f"  {model}: {float(ts_value):.2f} dB")


if __name__ == "__main__":
    main()
