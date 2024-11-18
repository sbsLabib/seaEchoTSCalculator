import numpy as np

def calculate_breathing_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Breathing model.

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties, including density (rho), viscosity (mu), and surface tension (sigma).
    bubble : object
        Bubble properties, including diameter (d), specific heat (Cp), thermal conductivity (K_th),
        adiabatic index (gamma), and gas pressure (Pg).

    Returns:
    --------
    float
        Target Strength (TS) in decibels (dB).

    Variables:
    ----------
    omega : float
        Angular frequency in radians per second.
    a : float
        Bubble radius (m), derived from diameter.
    Dp : float
        Thermal diffusivity of the bubble gas.
    beta_vis : float
        Viscous damping factor.
    omega0_squared : float
        Resonant angular frequency squared, including effects of compressibility and surface tension.
    sigma_bs : float
        Backscattering cross-section (m^2).
    TS : float
        Target Strength (dB), derived from sigma_bs.
    """
    omega = 2 * np.pi * f * 1000  # Angular frequency (rad/s)
    a = bubble.d / 2  # Bubble radius (m)

    # Thermal diffusivity
    Dp = bubble.K_th / (bubble.rho * bubble.Cp)
    beta_vis = 2 * water.mu / (water.rho * a**2)

    # Resonant angular frequency squared
    omega0_squared = (
        3 * bubble.gamma * bubble.Pg / (water.rho * a**2)
        - 2 * water.sigma / (water.rho * a**3)
    )

    # Scattering cross-section
    sigma_bs = a**2 / (
        (omega0_squared / omega**2 - 1 - 2 * beta_vis / omega)**2
        + (2 * beta_vis / omega)**2
    )

    # Target Strength (TS)
    TS = 10 * np.log10(sigma_bs)
    return TS
