# utils/ainslie_leighton_utils.py

import numpy as np

def compute_resonance_frequency(gamma, P_0, rho_0, R_0):
    """Compute the resonance frequency of a bubble."""
    return np.sqrt((3 * gamma * P_0) / (rho_0 * R_0**2))

def compute_viscous_damping(mu, rho_0, R_0):
    """Compute viscous damping."""
    return 4 * mu / (rho_0 * R_0**2)

def compute_thermal_damping(gamma, D, R_0, omega):
    """Compute thermal damping with frequency dependence."""
    thermal_time = R_0**2 / D
    return (3 * (gamma - 1) * omega * thermal_time) / (gamma * (1 + (omega * thermal_time)**2))

def compute_dimensionless_correction(omega, R_0, c):
    """Compute dimensionless correction term (epsilon)."""
    return (omega * R_0) / c

def compute_resonance_frequency_correction(omega_0_initial, beta_0, epsilon_0):
    """Apply correction to resonance frequency."""
    correction = 1 - (2 * beta_0**2 / omega_0_initial**2) - (epsilon_0**2 / 2)
    return omega_0_initial * np.sqrt(correction)