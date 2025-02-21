import numpy as np
import warnings

def sound_speed(T, S, z):
    """ 
    Compute sound speed in seawater using Medwin and Clay (1998).
    
    Parameters:
    -----------
    T : float
        Temperature (degrees Celsius).
    S : float
        Salinity (psu).
    z : float
        Depth (meters).
    
    Returns:
    --------
    float
        Sound speed in seawater (m/s).
    """
    # Cast all constants and inputs to float128
    T = np.float128(T)
    S = np.float128(S)
    z = np.float128(z)
    return (
        np.float128(1449.2)
        + np.float128(4.6) * T
        - np.float128(0.055) * T**2
        + np.float128(0.00029) * T**3
        + (np.float128(1.34) - np.float128(0.01) * T) * (S - np.float128(35))
        + np.float128(0.016) * z
    )

def resonance_freq(f, c, water, bubble):
    """
    Compute resonance frequency of bubbles with corrections.

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties (e.g., density, pressure, etc.).
    bubble : object
        Bubble properties (e.g., radius, gas properties).
    
    Returns:
    --------
    f_b : float
        Resonance frequency (Hz) without corrections.
    f_R : float
        Resonance frequency (Hz) with corrections.
    correction_params : numpy.ndarray
        Correction parameters [b, d/b, beta].
    """
    # Convert all inputs to float128
    f = np.float128(f)
    c = np.float128(c)
    omega = np.float128(2 * np.pi * f * 1000)  # Radians/sec
    a = np.float128(bubble.d / 2)  # Bubble radius (m)

    # Harmonic breathing frequency
    f_b = np.float128(1 / (2 * np.pi * a)) * np.sqrt(
        np.float128(3) * bubble.gamma * water.P / water.rho
    )

    # Correction factors
    tau = np.float128(water.sigma * 1e3)  # Surface tension (dyne/cm)
    P_dyn = np.float128(water.P * 10)  # Pressure (dyne/cm^2)
    rho_g = np.float128(bubble.rho_0 * 1e-3)  # Gas density (g/cm^3)
    Cp_g = np.float128(bubble.Cp * 0.2388)  # Specific heat (cal/g/°C)
    K_g = np.float128(bubble.K_th * 0.00239)  # Thermal conductivity (cal/cm/s/°C)

    # Compute X with full precision
    X = np.float128(a * 1e2 * np.sqrt(2 * omega * rho_g * Cp_g / K_g))

    # Corrections for surface tension and thermal conductivity
    d_over_b = np.float128(3 * (bubble.gamma - 1)) * (
        (X * (np.sinh(X) + np.sin(X)) - 2 * (np.cosh(X) - np.cos(X)))
        / (X**2 * (np.cosh(X) - np.cos(X)) + 3 * (bubble.gamma - 1) * X * (np.sinh(X) - np.sin(X)))
    )

    b = np.float128(1 / (1 + d_over_b**2))
    beta = np.float128(1 + 2 * tau / (P_dyn * a * 1e2) * (1 - 1 / (3 * bubble.gamma * b)))

    # Corrected resonance frequency
    f_R = f_b * np.sqrt(b * beta)
    correction_params = np.array([b, d_over_b, beta], dtype=np.float128)

    return f_b, f_R, correction_params

def damping_constant(f, c, water, bubble):
    """ 
    Compute damping constant of bubbles using Medwin and Clay (1998).

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties.
    bubble : object
        Bubble properties.
    
    Returns:
    --------
    float
        Total damping constant (delta).
    """
    # Convert all inputs to float128
    f = np.float128(f)
    c = np.float128(c)
    omega = np.float128(2 * np.pi * f * 1000)  # Radians/sec
    a = np.float128(bubble.d / 2)

    # Compute resonance frequencies with full precision
    f_b, f_R, correction_params = resonance_freq(f, c, water, bubble)

    # Compute damping components
    delta_r = omega * a / c  # Re-radiation damping
    delta_t = correction_params[1] * (f_R / (f * 1000))**2  # Thermal damping
    delta_nu = 4 * water.mu / (water.rho * omega * a**2)  # Viscous damping

    return np.float128(delta_r + delta_t + delta_nu)
