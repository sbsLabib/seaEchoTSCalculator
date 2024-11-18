from mpmath import nsum, besselj, hankel1, diff, log10, sqrt, pi
from utils.math_utils import (
    spherical_bessel_j,
    spherical_bessel_j_derivative,
    spherical_hankel1,
    spherical_hankel1_derivative,
)

def calculate_modal_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Modal Solution.

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties, including density (rho), temperature (T), and salinity.
    bubble : object
        Bubble properties, including diameter (d), adiabatic index (gamma),
        and molecular weight (Mm).

    Returns:
    --------
    float
        Target Strength (TS) in decibels (dB).

    Variables:
    ----------
    a : float
        Bubble radius (m), derived from diameter.
    omega : float
        Angular frequency in radians per second.
    k : float
        Wave number in water (1/m).
    R : float
        Universal gas constant (J/(mol·K)).
    cg : float
        Sound speed in the bubble gas (m/s).
    hc : float
        Ratio of gas sound speed to water sound speed.
    gp : float
        Density ratio of gas to water.
    kg : float
        Wave number in gas (1/m).
    ka : float
        Dimensionless wave number in water.
    kga : float
        Dimensionless wave number in gas.
    L : complex
        Modal scattering amplitude.
    sigma : float
        Backscattering cross-section (m^2).
    TS : float
        Target Strength (dB), derived from sigma.
    """
    # Bubble radius (m)
    a = bubble.d / 2

    # Angular frequency in radians/sec
    omega = 2 * pi * f * 1000

    # Wave number in water
    k = omega / c

    # Gas constant, J/(mol·K)
    R = 8.31446261815324

    # Sound speed in the bubble gas (m/s)
    cg = sqrt(bubble.gamma * R * (water.T + 273.15) / bubble.Mm)

    # Sound speed ratio (gas to water)
    hc = cg / c

    # Density ratio (gas to water)
    gp = bubble.rho / water.rho

    # Wave number in gas
    kg = omega / cg

    # Dimensionless wave numbers
    ka = k * a
    kga = kg * a

    def series_term(n, ka, kga):
        """
        Compute a single term in the infinite series for modal solution.

        Parameters:
        -----------
        n : int
            Series index.
        ka : float
            Dimensionless wave number in water.
        kga : float
            Dimensionless wave number in gas.

        Returns:
        --------
        complex
            Contribution of the nth term to the modal scattering amplitude.
        """
        numerator = (
            spherical_bessel_j_derivative(n, kga) * spherical_bessel_j(n, ka)
            - gp * hc * spherical_bessel_j(n, kga) * spherical_bessel_j_derivative(n, ka)
        )
        denominator = (
            spherical_bessel_j_derivative(n, kga) * spherical_hankel1(n, ka)
            - gp * hc * spherical_bessel_j(n, kga) * spherical_hankel1_derivative(n, ka)
        )
        return (-1)**n * (2 * n + 1) * (numerator / denominator)

    # Summing the series with a cutoff for convergence
    max_n = 50  # Adjustable upper limit for series convergence
    L = 1j * a / ka * sum(series_term(n, ka, kga) for n in range(max_n))

    # Compute backscattering cross-section (sigma)
    sigma = abs(L)**2

    # Target Strength (TS) in decibels
    TS = 10 * log10(sigma)

    return TS
