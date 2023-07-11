import numpy as np


class AbsorptionCoeff:
    """Absorption coefficient calculator for a given frequency range and a given angle of incidence.

    Args:
        T (list): List of Transfer Matrix.
        Z0 (float): Impedance of the air.
        theta (float): Angle of incidence in degrees.

    Returns:
        alpha (float): Absorption coefficient.
    """

    def __init__(self, T, Z0, theta):
        self.T = T
        self.Z0 = Z0
        self.theta = theta

    def abs_coeff(self):
        T_total = self.T[0]
        for i in range(1, len(self.T)):
            T_total = np.matmul(T_total, self.T[i])

        R = (T_total[0, 0] * np.cos(self.theta) - self.Z0 * T_total[1, 0]) / (
                    T_total[0, 0] * np.cos(self.theta) + self.Z0 * T_total[1, 0])
        alpha = 1 - (np.abs(R) ** 2)
        return alpha
