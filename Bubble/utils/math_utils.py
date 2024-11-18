from mpmath import besselj, hankel1, diff, sqrt, pi

def spherical_bessel_j(n, x):
    """
    Compute the spherical Bessel function of the first kind j_n(x) using mpmath.

    Parameters:
    -----------
    n : int
        Order of the Bessel function.
    x : float or mpmath.mpf
        Argument of the function.

    Returns:
    --------
    mpmath.mpf
        Value of the spherical Bessel function.
    """
    return sqrt(pi / (2 * x)) * besselj(n + 0.5, x)

def spherical_bessel_j_derivative(n, x):
    """
    Compute the derivative of the spherical Bessel function of the first kind j_n(x) using mpmath.

    Parameters:
    -----------
    n : int
        Order of the Bessel function.
    x : float or mpmath.mpf
        Argument of the function.

    Returns:
    --------
    mpmath.mpf
        Derivative of the spherical Bessel function.
    """
    bessel_j = besselj(n + 0.5, x)
    bessel_j_prime = diff(lambda t: besselj(n + 0.5, t), x)
    return sqrt(pi / (2 * x)) * (bessel_j_prime - (0.5 / x) * bessel_j)

def spherical_hankel1(n, x):
    """
    Compute the spherical Hankel function of the first kind h_n^(1)(x) using mpmath.

    Parameters:
    -----------
    n : int
        Order of the Hankel function.
    x : float or mpmath.mpf
        Argument of the function.

    Returns:
    --------
    mpmath.mpf
        Value of the spherical Hankel function.
    """
    return sqrt(pi / (2 * x)) * hankel1(n + 0.5, x)

def spherical_hankel1_derivative(n, x):
    """
    Compute the derivative of the spherical Hankel function of the first kind h_n^(1)(x) using mpmath.

    Parameters:
    -----------
    n : int
        Order of the Hankel function.
    x : float or mpmath.mpf
        Argument of the function.

    Returns:
    --------
    mpmath.mpf
        Derivative of the spherical Hankel function.
    """
    hankel1_val = hankel1(n + 0.5, x)
    hankel1_prime = diff(lambda t: hankel1(n + 0.5, t), x)
    return sqrt(pi / (2 * x)) * (hankel1_prime - (0.5 / x) * hankel1_val)
