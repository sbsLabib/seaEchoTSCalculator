# models/anderson_weston_model.py

import numpy as np
from utils.aw_utils import (
    compute_resonance_frequency,
    compute_damping_factors,
    compute_dimensionless_correction,
    compute_scattering_cross_section_AW,
)

def calculate_aw_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Anderson-Weston model.

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

    # Compute resonance frequency
    omega_0 = compute_resonance_frequency(bubble.gamma, water.P, water.rho, R_0)

    # Compute damping factors
    beta_viscous, beta_thermal, beta_0 = compute_damping_factors(
        bubble.gamma, water.mu, water.rho, R_0, bubble.K_th / (water.rho * water.cp)
    )

    # Compute dimensionless correction
    epsilon = compute_dimensionless_correction(omega, R_0, c)

    # Compute scattering cross-section
    sigma_AW = compute_scattering_cross_section_AW(omega, omega_0, beta_0, epsilon, R_0)

    # Compute TS
    return 10 * np.log10(sigma_AW)