# utils/aw_utils.py

import numpy as np

def compute_resonance_frequency(gamma, P_0, rho_0, R_0):
    """Compute the resonance frequency of a bubble."""
    return np.sqrt((3 * gamma * P_0) / (rho_0 * R_0**2))

def compute_damping_factors(gamma, mu, rho_0, R_0, D):
    """Compute damping factors (viscous, thermal, and total)."""
    beta_viscous = 4 * mu / (rho_0 * R_0**2)
    beta_thermal = (3 * (gamma - 1) / gamma) * (D / (R_0**2))
    beta_0 = beta_viscous + beta_thermal
    return beta_viscous, beta_thermal, beta_0

def compute_dimensionless_correction(omega, R_0, c):
    """Compute dimensionless correction term (epsilon)."""
    return (omega * R_0) / c

def compute_scattering_cross_section_AW(omega, omega_0, beta_0, epsilon, R_0):
    """Compute scattering cross-section for Anderson-Weston model."""
    numerator = 4 * np.pi * R_0**2
    denominator = ((omega_0**2 / omega**2) - 1)**2 + (2 * (beta_0 / omega) + (omega_0**2 / omega**2) * epsilon)**2
    return numerator / denominator