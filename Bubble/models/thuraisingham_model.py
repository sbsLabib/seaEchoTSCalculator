import numpy as np

def calculate_thuraisingham_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Thuraisingham model.

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties, including density (rho) and viscosity (mu).
    bubble : object
        Bubble properties, including diameter (d), thermal conductivity (K_th),
        specific heat (Cp), adiabatic index (gamma), and gas pressure (Pg).

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
    X : float
        Dimensionless thermal damping parameter.
    GAMMA : complex
        Generalized compressibility factor, combining real (ReG) and imaginary (ImG) parts.
    beta_th : float
        Thermal damping term.
    beta_vis : float
        Viscous damping term.
    beta0 : float
        Total damping factor.
    omega0_squared : float
        Resonant angular frequency squared.
    ka : float
        Dimensionless wave number, product of k and a.
    sigma_bs : float
        Backscattering cross-section (m^2).
    TS : float
        Target Strength (dB), derived from sigma_bs.
    """
    omega = 2 * np.pi * f * 1000  # Angular frequency (rad/s)
    a = bubble.d / 2  # Bubble radius (m)

    # Thermal diffusivity
    Dp = bubble.K_th / (bubble.rho * bubble.Cp)
    X = np.sqrt(2 * omega / Dp) * a
    tanh_term = np.tanh((1 + 1j) * X / 2)

    # Generalized compressibility
    GAMMA = bubble.gamma / (
        1 - ((1 + 1j) * X / 2 / tanh_term - 1) * (6j * (bubble.gamma - 1) / X**2)
    )
    ReG = GAMMA.real
    ImG = GAMMA.imag

    # Damping terms
    beta_th = 3 * bubble.Pg / (2 * water.rho * a**2 * omega) * ImG
    beta_vis = 2 * water.mu / (water.rho * a**2)
    beta0 = beta_th + beta_vis

    # Resonant angular frequency squared
    omega0_squared = (
        3 * ReG * bubble.Pg / (water.rho * a**2)
        - 2 * water.sigma / (water.rho * a**3)
    )

    # Scattering cross-section
    ka = omega / c * a
    numerator = omega0_squared / omega**2 - 1 - 2 * ka * beta0 / omega
    denominator = 2 * beta0 / omega + ka * omega0_squared / omega**2
    sigma_bs = a**2 * (np.sin(ka) / ka)**2 / (1 + ka**2) / (
        numerator**2 + denominator**2
    )

    # Target Strength (TS)
    TS = 10 * np.log10(sigma_bs)
    return TS
