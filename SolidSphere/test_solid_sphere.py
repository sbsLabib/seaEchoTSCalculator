#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 21:10:34 2024

@author: wangbinb

This script is used to test Target Strength of a solid sphere for a 1 MHz 
Echosounder. 

This can be used for choose Tungsten ball for acoustic calibration.
Following Foote (1990), the design aim of target strengh is -40 dB.

The acoustic scattering of rigid spheres is computed using Appendix D in 
Berges (2015) PhD thesis. 
"""

import numpy as np
import matplotlib.pyplot as plt
import mpmath
import SeaEcho_water_bubble
import SeaEcho_solid_sphere
from SeaEcho_solid_sphere import TS_solid_sphere

plt.close('all')
plt.style.use('fast')


"""
Main program, examine one sphere at different frequencies 
"""
# Define parameters
# f = np.linspace(0, 1200, 1000)  # Frequency range in kHz
# d = np.array([2.38e-3, 2.5e-3, 12.7e-3, 25.4e-3])  # Diameters in meters
# a = d / 2.0  # Radii of the spheres
# freshwater = SeaEcho_water_bubble.seawater(20, 1, 0)  # Freshwater environment

# # Loop over each diameter and generate TS plot for each
# for ai in a:
#     TS = np.zeros(len(f))  # Initialize TS array for this radius
    
#     # Loop over frequencies and calculate TS for this radius
#     for i, fi in enumerate(f):
#         TS[i] = TS_solid_sphere(fi, ai, SeaEcho_solid_sphere.Tungsten(), freshwater)
    
#     # Create a new figure for each diameter
#     plt.figure()
    
#     # Plot TS vs frequency
#     plt.plot(f, TS, label=f'd = {ai * 2 * 1e3:.2f} mm')
    
#     # Customize the plot
#     plt.xlabel('Frequency (kHz)')
#     plt.ylabel(r'TS (dB re 1 m$^2$ @ 1m)')
#     plt.title(f'Target Strength vs Frequency for Diameter {ai * 2 * 1e3:.2f} mm')
#     plt.legend()
    
#     # Save the plot to a unique file for this diameter
#     plt.savefig(f'TS_sphere_freq_d_{ai * 2 * 1e3:.2f}mm.pdf')
    
#     # Close the figure to avoid overwriting
#     plt.close()

# """
# Program 2, examine different spheres at 1 MHz
# """
# d = np.linspace(1,20) * 1e-3 # m
# a = d/2.0  
# f = 1000.0 
# TS = np.zeros(len(d))
# for i, ai in enumerate(a):
#     TS[i] = TS_solid_sphere(f, ai, SeaEcho_solid_sphere.Tungsten(),freshwater)

# plt.figure(2)
# plt.plot(d*1e3,TS)
# plt.xlabel('Sphere diameter (mm)')
# plt.ylabel(r'TS (dB re 1 m$^2$ @ 1m)')
# plt.savefig('TS_sphere_diameter_1.pdf')

"""
Program 3, test the response of solid ball to the frequency around the trasmission
"""

# Frequency and sphere diameter used in laboratory
f = np.linspace(10, 1250, 2000)  # Frequency range in kHz
d = 2.5e-3  # Diameter in meters (25.4 mm)
a = d / 2.0  # Radius of the sphere

# freshwater environment (temperature = 20°C, depth = 1m, salinity = 0)
freshwater = SeaEcho_water_bubble.seawater(20, 1, 0)

# array for TS values for the frequency range
TS = np.zeros(len(f))

# Loop over frequencies and calculate TS for this diameter
for i, fi in enumerate(f):
    TS[i] = TS_solid_sphere(fi, a, SeaEcho_solid_sphere.Tungsten(), freshwater)

# Plotting the results for 25.4 mm sphere
plt.figure()
plt.plot(f, TS, label=f'd = {d * 1e3:.2f} mm')

# Customize the plot
plt.xlabel('Frequency (kHz)')
plt.ylabel(r'TS (dB re 1 m$^2$ @ 1m)')
plt.title(f'Target Strength vs Frequency for Diameter {d * 1e3:.2f} mm')
plt.legend()

# Save the figure
plt.savefig(f'TS_sphere_transmission_compression_{d * 1e3:.2f}mm.pdf')

# Save the data to a compressed .npz file
data_to_save = np.vstack((f, TS))
np.savez(f'Target_strength_solid_sphere_{d * 1e3:.2f}mm.npz', frequency=f, diameter=d, TS=TS)

# Show the plot
plt.show()


# Export the data to a CSV file
csv_filename = f'Target_strength_solid_sphere_{d * 1e3:.2f}mm.csv'
header = 'Frequency (kHz), Target Strength (dB)'
data_to_export = np.column_stack((f, TS))  # Combine frequency and TS into two columns

# Try to write the CSV file and handle any errors
try:
    np.savetxt(csv_filename, data_to_export, delimiter=',', header=header, comments='', fmt='%.6f')
    print(f"CSV file '{csv_filename}' has been successfully written.")
except Exception as e:
    print(f"Error writing the CSV file: {e}")

# Show the plot
plt.show()
    
# plt.xlabel('Frequency (kHz)')
# plt.ylabel(r'TS (dB re 1 m$^2$ @ 1m)')
# plt.legend()
# plt.savefig('TS_sphere_transmission_compression.pdf')

# data_to_save = np.vstack((f,TS))
# np.savez('Target_strengh_solid_sphere.npz', name1=f, name2=d, name3=TS)
# with open('Target_strengh_solid_sphere.npy', 'wb') as ff:
#     np.save(ff, data_to_save)