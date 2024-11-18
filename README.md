# Underwater Bubble Target Strength Computational Framework

## Overview

This project provides a comprehensive computational framework for analyzing the **Target Strength (TS)** of underwater gas bubbles based on acoustic backscattering. The framework implements multiple mathematical models and includes features for high-precision numerical calculations, parallel processing, and advanced visualization.

The project is designed for researchers, engineers, and oceanographers investigating acoustic scattering phenomena, including applications in underwater gas leakage detection, marine ecology, and acoustic oceanography.

---

## Features

- **Implemented Models**:
  - **Medwin and Clay Model**: Classical TS model for small bubbles.
  - **Thuraisingham Model**: Enhanced TS estimation considering thermal and viscous damping.
  - **Breathing Model**: TS calculation using simplified breathing mode.
  - **Modal Solution**: High-precision solution for wide \(ka\) ranges.
- **High Precision**:
  - Mathematical functions such as Bessel and Hankel functions implemented with `mpmath` for numerical stability and accuracy.
- **Dynamic Inputs**:
  - Frequency ranges and discrete frequency options.
  - Adjustable seawater properties (temperature, salinity, depth).
  - User-defined bubble diameters.
- **Parallel Processing**:
  - TS computations parallelized across frequency ranges for improved performance.
- **Interactive Visualization**:
  - \(ka\) (wave number times bubble radius) vs TS plots with logarithmic scaling.
  - Frequency vs TS plots for specific cases.
- **User-Friendly Interface**:
  - Text-based input prompts for seamless data entry.
  - Clear and labeled outputs for discrete frequencies.

---

## Project Structure

The code is modularized for clarity and reusability. Here's an overview of the directory structure:

