# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:37:43 2023

This scipt defines a class that provides properties of Tungsten 
solid sphere and the calculation of Target strength of the solid ball

Reference: TAMOC model. 

@author: wangbinb
"""

import numpy as np
import matplotlib.pyplot as plt
import mpmath
import SeaEcho_water_bubble

class Tungsten():
        """
        Parameters (MacLennan and Dunn 1984, Foote 1990):
        -------------------------------------
                rho   - density (kg/m^3)
                c_lon - longitudinal sound speed (m/s)
                c_trans - transverse sound speed (m/s)               
        """
        def __init__(self):
            self.rho = 14900
            self.c_lon = 6853
            self.c_trans = 4171

def TS_solid_sphere(f, a, sphere_material, water):
    """
    %     Parameters
    %     ----------
    %     f : 
    %         sonar frequency (KHz)
    %     a : 
    %         sphere radius (m)
    
    """
    omega = 2 * np.pi * f * 1000    # radians/sec
    k = omega/water.c    
    
    def eta_n(l):
        q1 = k*a*water.c/sphere_material.c_lon
        q2 = k*a*water.c/sphere_material.c_trans
        
        """
        Using the script on https://www.fisheries.noaa.gov/data-tools/standard-sphere-target-strength-calculator
        This equations are identical to those in Appendix D in Berges thesis, just using different notations.
        """
        def jj(n,z):
            if n==-2:
                return -mpmath.cos(z) / (z**2) - mpmath.sin(z) / z;
            elif n==-1:
                return mpmath.cos(z) / z
            else:
                return mpmath.besselj(n + .5, z) * np.sqrt(np.pi / (2 * z))

        def j1(n,z):
            """
            Calculate the first derivative of the spherical bessel function
			of the first kind.  n is always integer. 
            """
            return (jj(n - 1, z) - jj(n + 1, z)) / 2 - jj(n, z) / (2 * z);

        def j2(n,z):
            """
            Calculate the second derivative of the spherical bessel function of the
			first kind.
            """
            return (z**2 * jj(n - 2, z) - 2 * z**2 * jj(n, z) +\
                     jj(n + 2, z) - 2 * z * jj(n - 1, z) + 2 * z * jj(n + 1, z) +\
                     3 * jj(n, z)) / (4 * z**2)
                
        def yy(n,z):
            """
            Calculate the spherical bessel function of the second kind.
            """
            if n==-1:
                return mpmath.sin(z) / z
            else: 
                return mpmath.bessely(n + .5, z) * np.sqrt(np.pi / (2 * z))
                
        def y1(n,z):
            """
            Calculate the first derivative of the spherical bessel function	of the 
			second kind.
            """
            return (yy(n - 1, z) - yy(n + 1, z)) / 2 - yy(n, z) / (2 * z)
        
        A1 = 2 * l * (l + 1) * (q1 * j1(l, q1) - jj(l, q1))		
        A2 = (l**2 + l - 2) * jj(l, q2) + q2**2 * j2(l, q2)
        
        alpha = 2*(sphere_material.rho/water.rho)*(sphere_material.c_trans/water.c)**2
        beta = 2*(sphere_material.rho/water.rho)*(sphere_material.c_lon/water.c)**2 - alpha
        
        B1 = k*a * (A2 * q1 * j1(l, q1) - A1 * jj(l, q2))
        B2 = A2 * q1**2 * (beta * jj(l, q1) - alpha * j2(l, q1)) - A1 * alpha * (jj(l, q2) - q2 * j1(l, q2))
        
        eta_n = mpmath.atan(-1 * (B2 * j1(l, k*a) - B1 * jj(l, k*a)) / (B2 * y1(l, k*a) - B1 * yy(l, k*a)))
        
        return eta_n
    
    form_function = -2.0 / (k*a) * \
        mpmath.nsum( \
            lambda n: (-1)**n * (2*n+1) * \
                mpmath.sin(eta_n(n)) * mpmath.exp(1j*eta_n(n)),\
                [0, mpmath.inf])
    
    
    
    TS = 10 * mpmath.log10(a**2 * abs(form_function)**2 /4.0)
    return TS
