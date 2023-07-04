import numpy as np
from scipy.special import jv


class AbsorberModelInterface:
    """Base class interface for Absorber Models

    Args:
        f (float): Frequency
        air_density (float): Density of air
        sigma (float): Flow resistivity
        omega (float): Angular frequency
    """

    f = air_density = sigma = omega = 0.0

    def __init__(self, f, air_density, air_speed, sigma, L1, viscosity):
        self.f = f
        self.air_density = air_density
        self.air_speed = air_speed
        self.sigma = sigma
        self.L1 = L1
        self.omega = 2 * np.pi * self.f
        self.viscosity = viscosity


class Porous_Absorber(AbsorberModelInterface):
    """Delany & Bazley Empirical Model

    Args:
        f (float): Frequency
        air_density (float): Density of air
        air_speed (float): Speed of air
        sigma (float): Flow resistivity

    Returns:
        Zp (float): Surface impedance
        kp (float): Wave number
        Tp (float): Transfer Matrix of the absorber
    """

    def __init__(self, f, air_density, air_speed, sigma, L1, viscosity, theta):
        super().__init__(f, air_density, air_speed, sigma, L1, viscosity)

        self.theta = theta
        self.X = (self.air_density * self.f) / self.sigma

    def calculate_aux_values(self):
        pass

    def get_kp(self):
        kp = self.omega / self.air_speed * (1 + 0.0978 * self.X ** (-0.7) - 1j * 0.189 * self.X ** (-0.595))
        return kp

    def get_Zp(self):
        Zp = self.air_density * self.air_speed * (1 + 0.0571 * self.X ** (-0.754) - 1j * 0.087 * self.X ** (-0.732))
        return Zp

    def get_Tp(self):
        kp = self.get_kp()
        Zp = self.get_Zp()
        kp_x = kp * np.sin(self.theta)
        kp_z = np.sqrt(kp ** 2 - kp_x ** 2)

        Tp = np.array([[np.cos(kp_z * self.L1), 1j * Zp * (kp / kp_z) * np.sin(kp_z * self.L1)],
                       [(1j / Zp) * (kp_z / kp) * np.sin(kp_z * self.L1), np.cos(kp_z * self.L1)]])
        return Tp


class PerforatedPlate_Absorber(AbsorberModelInterface):
    """MAA´s Model

    Args:
        d_hole (float): Diameter of hole
        a (float): Distance between holes
        phi (float): Porosity
        s (float): Ratio of the holes' diameter to the boundary layer thickness
        S (float): Area of the edge effects
        e (float): DONT KNOW THE NAME
        F_e (float): Fok function

    Returns:
        Zp (float): Surface impedance
        kp (float): Wave number
        Tp (float): Transfer Matrix of the absorber
    """

    def __init__(self, f, air_density, air_speed, sigma, L1, viscosity, theta, d_hole, a):
        super().__init__(f, air_density, air_speed, sigma, L1, viscosity)

        self.theta = theta
        self.d_hole = d_hole
        self.a = a

    def get_kp(self):
        kp = self.omega / self.air_speed
        return kp

    def get_Zp(self):
        self.phi = (np.pi / 4) * (self.d_hole / self.a) ** 2
        self.e = 1.1284 * np.sqrt(self.phi)
        self.S = 2 * np.sqrt(self.a ** 2)
        self.s = self.d_hole * np.sqrt(self.air_density * self.omega / 4 / self.viscosity)
        self.F_e = (1 - 1.4092 * self.e + 0.33818 * (self.e ** 3) + 0.06793 *
                    (self.e ** 5) - 0.02287 * (self.e ** 6) + 0.03015 *
                    (self.e ** 7) - 0.01641 * (self.e ** 8)) ** (-1)
        J_0 = jv(0, self.s * np.sqrt(-1j))
        J_1 = jv(1, self.s * np.sqrt(-1j))
        Zp = (np.sqrt(2 * self.air_density * self.omega * self.viscosity) / 2 * self.phi +
              1j * (self.omega * self.air_density / self.phi) * (0.85 * self.d_hole / self.F_e +
                                                                 self.L1 * (1 - (2 / (self.s * np.sqrt(-1j))) *
                                                                            (J_1 * np.sqrt(
                                                                                self.s * -1j) / J_0 * np.sqrt(
                                                                                self.s * -1j))) ** (-1)))
        return Zp

    def get_Tp(self):
        Tp = np.array([[1, self.get_Zp()],
                       [0, 1]])
        return Tp


class Air_Absorber(AbsorberModelInterface):
    """Air Model
    """

    def __init__(self, f, air_density, air_speed, sigma, L1, viscosity, theta):
        super().__init__(f, air_density, air_speed, sigma, L1, viscosity)

        self.theta = theta

    def get_kp(self):
        kp = 2 * np.pi * self.f / self.air_speed
        return kp

    def get_Zp(self):
        Zp = self.air_density * self.air_speed
        return Zp

    def get_Tp(self):
        kp = self.get_kp()
        Zp = self.get_Zp()
        kp_x = kp * np.sin(self.theta)
        kp_z = np.sqrt(kp ** 2 - kp_x ** 2)
        Tp = np.array([[np.cos(kp_z * self.L1), 1j * Zp * (kp / kp_z) * np.sin(kp_z * self.L1)],
                       [(1j / Zp) * (kp_z / kp) * np.sin(kp_z * self.L1), np.cos(kp_z * self.L1)]])
        return Tp
