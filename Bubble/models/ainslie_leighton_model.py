# models/ainslie_leighton_model.py

import numpy as np
from utils.ainslie_leighton_utils import compute_resonance_frequency, compute_viscous_damping, compute_thermal_damping, compute_dimensionless_correction, compute_resonance_frequency_correction, compute_scattering_cross_section_AL


def calculate_ainslie_leighton_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Ainslie-Leighton model.

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
    float
        Computed TS value in dB.
    """
    omega = 2 * np.pi * f * 1000  # Convert kHz to rad/s
    R_0 = bubble.d / 2  # Bubble radius

    # Compute initial resonance frequency
    omega_0_initial = compute_resonance_frequency(bubble.gamma, water.P, water.rho, R_0)

    # Compute damping factors
    beta_viscous = compute_viscous_damping(water.mu, water.rho, R_0)
    epsilon_0 = compute_dimensionless_correction(omega_0_initial, R_0, c)
    beta_thermal = compute_thermal_damping(bubble.gamma, bubble.K_th / (water.rho * water.cp), R_0, omega_0_initial)
    beta_0 = beta_viscous + beta_thermal

    # Apply resonance frequency correction
    omega_0 = compute_resonance_frequency_correction(omega_0_initial, beta_0, epsilon_0)

    # Compute scattering cross-section
    epsilon = compute_dimensionless_correction(omega, R_0, c)
    beta_thermal = compute_thermal_damping(bubble.gamma, bubble.K_th / (water.rho * water.cp), R_0, omega)
    beta_0 = beta_viscous + beta_thermal

    sigma_AL = compute_scattering_cross_section_AL(omega, omega_0, beta_0, epsilon, R_0)

    # Compute TS
    return 10 * np.log10(sigma_AL)