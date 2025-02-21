# core/cli.py
import numpy as np
from utils.SeaEcho_water_bubble import seawater, air_bubble

MODEL_MAP = {
    1: "Medwin_Clay",
    2: "Breathing",
    3: "Thuraisingham",
    4: "Modal",
    5: "Weston_Medwin",
    6: "Anderson_Weston",
    7: "Ainslie_Leighton"
}

# Error handling

def _validate_models(input_str):
    """Validate and parse model selection input."""
    try:
        selected_nums = [int(num.strip()) for num in input_str.split(",")]
        invalid_nums = [num for num in selected_nums if num not in MODEL_MAP]
        if invalid_nums:
            raise ValueError(f"Invalid model numbers: {invalid_nums}")
        return [MODEL_MAP[num] for num in selected_nums]
    except ValueError as e:
        print(f"Error: {e}")
        print("Please enter comma-separated numbers from the model list")
        return None

def _validate_float(prompt, min_val=None, max_val=None):
    """Validate and return a float input with optional range checking."""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be ≥ {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be ≤ {max_val}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def _validate_frequency_range():
    """Validate and parse frequency range input."""
    while True:
        try:
            range_input = input("Enter range (kHz) [min-max]: ")
            f_min, f_max = map(float, range_input.split("-"))
            if f_min >= f_max:
                raise ValueError("Max must be greater than min")
            return f_min, f_max
        except ValueError as e:
            print(f"Invalid range format: {e}. Use format like '10-50'")

def _validate_frequency_input():
    """Handle frequency input with validation."""
    freq_type = ""
    while freq_type not in ["single", "range"]:
        freq_type = input("Frequency type? (single/range): ").lower()
        if freq_type not in ["single", "range"]:
            print("Invalid choice. Please enter 'single' or 'range'")

    if freq_type == "range":
        f_min, f_max = _validate_frequency_range()
        steps = int(_validate_float("Number of steps: ", min_val=1))
        freq_range = np.linspace(f_min, f_max, steps)
        
        freq_discrete = np.array([])
        discrete_input = input("Additional discrete freqs (kHz, comma-separated): ").strip()
        if discrete_input:
            try:
                freq_discrete = np.array(list(map(float, discrete_input.split(","))))
            except ValueError:
                print("Invalid discrete frequencies. Using only range values.")
        
        frequencies = np.sort(np.unique(np.concatenate([freq_range, freq_discrete])))
    else:
        center_freq = _validate_float("Center frequency (kHz): ", min_val=0.1)
        frequencies = np.linspace(center_freq-10, center_freq+10, 100)
        freq_discrete = np.array([center_freq])

    return frequencies, freq_discrete

# User input

def get_user_input():
    """Collect and validate all user inputs."""
    print("=== Target Strength Computation ===")
    
    # Model selection with validation
    selected_models = None
    while selected_models is None:
        print("\nAvailable Models:")
        for num, model in MODEL_MAP.items():
            print(f"{num}. {model}")
        model_input = input("Select models (comma-separated numbers): ")
        selected_models = _validate_models(model_input)

    # Frequency input with validation
    frequencies, freq_discrete = _validate_frequency_input()

    # Environmental parameters with validation
    print("\nEnvironmental Parameters:")
    T = _validate_float("Temperature (°C): ", min_val=-2, max_val=40)
    S = _validate_float("Salinity (psu): ", min_val=0, max_val=40)
    z = _validate_float("Depth (m): ", min_val=0)
    d_mm = _validate_float("Bubble diameter (mm): ", min_val=0.01)

    return {
        'frequencies': frequencies,
        'freq_discrete': freq_discrete,
        'T': T,
        'S': S,
        'z': z,
        'd': d_mm / 1000,  # Convert mm to m
        'models': selected_models
    }

if __name__ == "__main__":
    try:
        params = get_user_input()
        print("\nParameters validated successfully!")
        print(f"Selected models: {', '.join(params['models'])}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nCritical error: {str(e)}")