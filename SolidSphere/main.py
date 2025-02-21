from concurrent.futures import ProcessPoolExecutor
import numpy as np
from utils.SeaEcho_water_bubble import seawater
from utils.sphere_properties import Tungsten
from models.sphere_Target_strength import TS_solid_sphere
from plots.plot_utils import plot_ts_vs_frequency


def compute_ts_for_frequency(f, radius, tungsten, water):
    """
    Compute Target Strength (TS) for a single frequency.
    """
    return TS_solid_sphere(f, radius, tungsten, water)


def get_user_input():
    """
    Gather user input for frequency range, discrete frequencies, and seawater properties.
    """
    print("=== Solid Sphere Target Strength Computation ===")

    # Frequency range input
    freq_range = input("Enter frequency range (e.g., 10-50): ")
    f_min, f_max = map(float, freq_range.split("-"))
    steps = int(input("Enter the number of steps between the range: "))
    freq_range_values = np.linspace(f_min, f_max, steps)

    # Discrete frequency input
    freq_discrete_input = input("Enter discrete frequencies (e.g., 30, 45): ")
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

    # Sphere radius input
    radius_mm = float(input("Enter sphere radius (mm): "))  # Input in mm
    radius = radius_mm / 1000  # Convert to meters directly (radius, not diameter)

    return frequencies, freq_discrete_values, T, S, z, radius


def main():
    """
    Main function for computing Target Strength of a solid sphere using parallelization.
    """
    # Get user input
    frequencies, freq_discrete_values, T, S, z, radius = get_user_input()

    # Create seawater and material objects
    water = seawater(T, z, S)
    tungsten = Tungsten()

    # Use ProcessPoolExecutor to parallelize frequency computations
    with ProcessPoolExecutor() as executor:
        ts_results = list(executor.map(compute_ts_for_frequency, frequencies,
                                       [radius] * len(frequencies),
                                       [tungsten] * len(frequencies),
                                       [water] * len(frequencies)))

    # Convert results to numpy array
    ts_results = np.array(ts_results)

    # Prepare for plotting
    ts_data = {"Solid Sphere Model": ts_results}

    # Plot results (showing the plot directly)
    plot_ts_vs_frequency(frequencies, ts_data, labels=["Solid Sphere"])

    # Print results for discrete frequencies
    print("\n=== Results for Discrete Frequencies ===")
    for f in freq_discrete_values:
        idx = frequencies.index(f)
        ts_value = ts_results[idx]
        print(f"Frequency: {f} kHz -> TS: {float(ts_value):.2f} dB")


if __name__ == "__main__":
    main()
