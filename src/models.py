import numpy as np
from scipy.special import jv

class AbsorberModelInterface:
    # an interface upon which each absorber model will be implemented

    f = air_density = phi = alpha_inf = sigma = gamma = P0 = viscosity_L = \
         therm_L = Pr = viscosity = 0.0
    
    def __init__(self, f, air_density, phi, alpha_inf, sigma, gamma, P0,  viscosity_L, \
         therm_L, Pr, viscosity):
        self.f = f
        self.air_density = air_density
        self.phi = phi
        self.alpha_inf = alpha_inf
        self.sigma = sigma
        self.gamma = gamma
        self.P0 = P0
        self.viscosity_L = viscosity_L
        self.therm_L = therm_L
        self.Pr = Pr
        self.viscosity = viscosity

    def calculate_aux_values(self):
        pass
    
    def get_kp(self):
        pass

    def get_Zp(self):
        pass

    def set_f(self, new_f):
        self.f = new_f

# Poröser Absorber
# Acoustic Waves p.128
# JAC-Modell
# Porosität des porösen Materials (Φ)
# density der Flüssigkeit (normalerweise Luft) (ρ)
# viscosity des Fluids (η)
# Strömungswiderstand des porösen Materials (σ)
# Frequenz der Schallwelle (f)
# Thermische Parameter eines porösen Materials (Pr, Le)
# Wärmekapazität des porösen Materials (Cp)
# Porengröße des porösen Materials (d)
class Porous_Absorber(AbsorberModelInterface):

    def __init__(self, f, air_density, phi, alpha_inf, sigma, gamma, P0,  viscosity_L,
                 therm_L, Pr, viscosity):
        super().__init__(f, air_density, phi, alpha_inf, sigma, gamma, P0, viscosity_L,
                         therm_L, Pr, viscosity)
        
        self.K0 = self.gamma * self.P0
        self.calculate_aux_values()
    
    def calculate_aux_values(self):
        '''JAC Model'''
        self.omega = 2 * np.pi * self.f
        self.G1 = self.sigma * self.phi / (self.alpha_inf * self.air_density * self.omega)
        self.G2 = 4*((self.alpha_inf)**2) * self.air_density * self.viscosity * self.omega / ((self.sigma*self.phi*self.viscosity_L)**2)

        self.G1_dot = 8*self.viscosity / (self.air_density * self.Pr * ((self.therm_L)**2) * self.omega)

        self.G2_dot = self.air_density * self.Pr * ((self.therm_L)**2) * self.omega / (16*self.viscosity)

        self.air_density_p = self.air_density * self.alpha_inf * (1- 1j*self.G1*np.sqrt(1+1j*self.G2)) / self.phi

        self.K_p = self.K0*self.phi**(-1) / (self.gamma - (self.gamma-1)*((1- 1j*self.G1_dot*np.sqrt(1+ 1j*self.G2_dot))**-1))

    def get_kp(self):
        return self.omega * np.sqrt(self.air_density_p/self.K_p)
    
    def get_Zp(self):
        return np.sqrt(self.air_density_p*self.K_p)
    
    def set_f(self, new_f):
        super().set_f(new_f)
        self.calculate_aux_values()


class PerforatedPlate_Absorber(AbsorberModelInterface):

    def __init__(self, f, d_hole, a, L1, air_density, viscosity, air_c, L2):
        super().__init__(f, d_hole, a, L1, air_density, viscosity, air_c, L2)

        self.d_hole = d_hole
        self.a = a
        self.omega = 2 * np.pi * self.f
        self.phi = (np.pi/4) * (self.d_hole**2) / (self.a**2)

    def calculate_aux_values(self):
        '''MAA1 Model'''
        s = self.d_hole * np.sqrt(self.air_density * self.omega / 4 / self.viscosity) # ratio of the diameter of the
        # perforations to the boundary layer thickness for 1 < s < 10
        S = a ** 2  # area of the edge effects
        D = 2 * np.sqrt(S / np.pi)
        e = 1.1284 * np.sqrt(self.phi)
        # D = L0
        # e = d/D
        F_e = (1 - 1.4092 * e + 0.33818 * (e ** 3) + 0.06793 * (e ** 5) - 0.02287 * (e ** 6) + 0.03015 * (
                    e ** 7) - 0.01641 * (e ** 8)) ** (-1) # Fok function - reactive part considering hole edge effects

        J_0 = jv(0, s * np.sqrt(-1j))  # J0 and J1 are the Bessel functions of the zero order and the first order
        J_1 = jv(1, s * np.sqrt(-1j))

        k0 = omega / c0  # wavenumber in medium
        Z0 = density_0 * c0  # impendence of air medium

        Z_p = (sqrt(2 * density_0 * omega * viscosity) / 2 / phi) + (1j * omega * density_0 / phi) * (
                0.85 * d / F_e + t * (1 - 2 * J_1 / (s * sqrt(-1j)) / J_0) ** (-1))

# def JAC(f: float,
#         density: float,
#         phi: float,
#         alpha_inf: float,
#         sigma: float,
#         gamma: float,
#         P0: float,
#         viscosity_L: float,
#         therm_L: float,
#         Pr: float,
#         viscosity: float
#         ) -> float:
#
#     K0 = gamma * P0
#     omega = 2*np.pi*f
#     G1 = sigma * phi / (alpha_inf * density * omega)
#
#     G2 = 4*((alpha_inf)**2) * density * viscosity * omega / ((sigma*phi*viscosity_L)**2)
#
#     G1_dot = 8*viscosity / (density * Pr * ((therm_L)**2) * omega)
#
#     G2_dot = density * Pr * ((therm_L)**2) * omega / (16*viscosity)
#
#     density_p = density * alpha_inf * (1- 1j*G1*np.sqrt(1+1j*G2)) / phi
#
#     K_p = K0*phi**(-1) / (gamma - (gamma-1)*((1- 1j*G1_dot*np.sqrt(1+ 1j*G2_dot))**-1))
#
#     kp = omega * np.sqrt(density_p/K_p)
#     Zp = np.sqrt(density_p*K_p)
#
#     return Zp, kp