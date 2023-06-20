from src import models, utils
import numpy as np

class AbsorptionCoeff:
    '''Absorption coefficient calculator for a given frequency range and a given angle of incidence.

    Args:
        T (list): List of Transfer Matrix.
        theta (float): Angle of incidence in degrees.
        L1 (float): Thickness of the first layer in mm.

    '''

    # def __init__(self, theta, L1, f_min, f_max, absorber_layers: models.AbsorberModelInterface, air_density, air_speed):
    #     self.alphas = np.array([])
    #     self.theta = theta
    #     self.L1 = L1
    #     self.f_min = f_min
    #     self.f_max = f_max
    #     self.absorber_layers = absorber_layers
    #     self.air_density = air_density
    #     self.air_speed = air_speed

    def __init__(self, T, theta):
        self.T = T
        self.theta = theta

    def abs_coeff(self):
        T_total = self.T[0]
        for i in range(1, len(self.T)):
            T_total = np.dot(T_total, self.T[i])

        R = (T_total[0, 0]*np.cos(self.theta) - T_total[1, 0]) / (T_total[0, 0]*np.cos(self.theta) + T_total[1, 0])
        alpha = 1 - np.abs(R) ** 2
        return alpha