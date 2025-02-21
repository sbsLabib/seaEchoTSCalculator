import mpmath
import numpy as np

def TS_solid_sphere(f, a, sphere_material, water):
    """
    Calculate Target Strength (TS) of a solid sphere.

    Parameters:
    ----------
    f : float
        Sonar frequency (kHz).
    a : float
        Sphere radius (m).
    sphere_material : object
        Material properties of the sphere.
    water : object
        Properties of the surrounding water.
    
    Returns:
    --------
    TS : float
        Target Strength (dB).
    """
    omega = 2 * np.pi * f * 1000  # Radians/sec
    k = omega / water.c           # Wave number in water

    def eta_n(l):
        """
        Compute phase shift (eta_n) for the nth order.
        """
        q1 = k * a * water.c / sphere_material.c_lon
        q2 = k * a * water.c / sphere_material.c_trans

        def jj(n, z):
            if n == -2:
                return -mpmath.cos(z) / z**2 - mpmath.sin(z) / z
            elif n == -1:
                return mpmath.cos(z) / z
            else:
                return mpmath.besselj(n + 0.5, z) * mpmath.sqrt(mpmath.pi / (2 * z))

        def j1(n, z):
            """
            First derivative of spherical Bessel function of the first kind.
            """
            return (jj(n - 1, z) - jj(n + 1, z)) / 2 - jj(n, z) / (2 * z)

        def j2(n, z):
            """
            Second derivative of spherical Bessel function of the first kind.
            """
            return (z**2 * jj(n - 2, z) - 2 * z**2 * jj(n, z) + jj(n + 2, z)
                    - 2 * z * jj(n - 1, z) + 2 * z * jj(n + 1, z) + 3 * jj(n, z)) / (4 * z**2)

        def yy(n, z):
            if n == -1:
                return mpmath.sin(z) / z
            else:
                return mpmath.bessely(n + 0.5, z) * mpmath.sqrt(mpmath.pi / (2 * z))

        def y1(n, z):
            """
            First derivative of spherical Bessel function of the second kind.
            """
            return (yy(n - 1, z) - yy(n + 1, z)) / 2 - yy(n, z) / (2 * z)

        A1 = 2 * l * (l + 1) * (q1 * j1(l, q1) - jj(l, q1))
        A2 = (l**2 + l - 2) * jj(l, q2) + q2**2 * j2(l, q2)

        alpha = 2 * (sphere_material.rho / water.rho) * (sphere_material.c_trans / water.c)**2
        beta = 2 * (sphere_material.rho / water.rho) * (sphere_material.c_lon / water.c)**2 - alpha

        B1 = k * a * (A2 * q1 * j1(l, q1) - A1 * jj(l, q2))
        B2 = A2 * q1**2 * (beta * jj(l, q1) - alpha * j2(l, q1)) - A1 * alpha * (jj(l, q2) - q2 * j1(l, q2))

        numerator = B2 * j1(l, k * a) - B1 * jj(l, k * a)
        denominator = B2 * y1(l, k * a) - B1 * yy(l, k * a)
        return mpmath.atan(-numerator / denominator)

    # Compute form function
    form_function = -2.0 / (k * a) * mpmath.nsum(
        lambda n: (-1)**n * (2 * n + 1) * mpmath.sin(eta_n(n)) * mpmath.exp(1j * eta_n(n)),
        [0, mpmath.inf],
    )

    # Compute Target Strength
    TS = 10 * mpmath.log10(a**2 * abs(form_function)**2 / 4.0)
    return TS
