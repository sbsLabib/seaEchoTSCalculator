import numpy as np
from utils.physical_properties import resonance_freq, damping_constant

def calculate_medwin_clay_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Medwin and Clay model.

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties, including density (rho), pressure (P), and viscosity (mu).
    bubble : object
        Bubble properties, including diameter (d), specific heat (Cp), thermal conductivity (K_th),
        adiabatic index (gamma), and gas pressure (Pg).

    Returns:
    --------
    float
        Target Strength (TS) in decibels (dB).

    Variables:
    ----------
    a : float
        Bubble radius (m), derived from diameter.
    f_b : float
        Resonance frequency without corrections (Hz).
    f_R : float
        Resonance frequency with corrections (Hz).
    correction_params : array-like
        Correction parameters [b, d/b, beta].
    delta : float
        Damping constant, including scattering, thermal, and viscous components.
    sigma_bs : float
        Backscattering cross-section (m^2).
    TS : float
        Target Strength (dB), derived from sigma_bs.
    """
    a = bubble.d / 2  # Bubble radius (m)

    # Compute resonance frequency and damping constant
    f_b, f_R, correction_params = resonance_freq(f, c, water, bubble)
    delta = damping_constant(f, c, water, bubble)

    # Scattering cross-section
    sigma_bs = a**2 / (
        (f_R / (f * 1e3) - 1)**2 + delta**2
    )

    # Target Strength (TS)
    TS = 10 * np.log10(sigma_bs)
    return TS

