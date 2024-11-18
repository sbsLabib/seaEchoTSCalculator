class Tungsten:
    """
    Properties of Tungsten solid sphere.

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
