import numpy as np
class BaseModel():
    '''Klasse für das Basismodell.'''
    def __init__(self, k1, L1, Z1, k2, L2, Z2):
        self.k1 = k1
        self.L1 = L1
        self.Z1 = Z1
        self.k2 = k2
        self.L2 = L2
        self.Z2 = Z2

    def tmm(self):
        # T1, T2, T3 definieren
        T1 = np.array([[np.cos(k1 * L1), 1j * Z1 * np.sin(k1 * L1)],
                       [(1j / Z1) * np.sin(k1 * L1), np.cos(k1 * L1)]])

        T2 = np.array([[np.cos(k2 * L2), 1j * Z2 * np.sin(k2 * L2)],
                       [(1j / Z2) * np.sin(k2 * L2), np.cos(k2 * L2)]])

        # T_total berechnen
        T_total = np.dot(T1, T2)

        return T_total

class JAC(BaseModel):
    '''Klasse für das poröse Modell.'''

    def __init__(self,
                    f: float,
                    dichte: float,
                    phi: float,
                    alpha_unend: float,
                    sigma: float,
                    gamma: float,
                    P0: float,
                    viskosität_L: float,
                    thermisch_L: float,
                    Pr: float,
                    viskosität: float
                    ) -> None:
            self.f = f
            self.dichte = dichte
            self.phi = phi
            self.alpha_unend = alpha_unend
            self.sigma = sigma
            self.gamma = gamma
            self.P0 = P0
            self.viskosität_L = viskosität_L
            self.thermisch_L = thermisch_L
            self.Pr = Pr
            self.viskosität = viskosität

    def calculate_tmm(self):
        T_total = self.tmm(self)
# Poröser Modell
def JAC(f: float,
        dichte: float,
        phi: float, 
        alpha_unend: float,
        sigma: float,
        gamma: float,
        P0: float,
        viskosität_L: float,
        thermisch_L: float,
        Pr: float,
        viskosität: float
        ) -> float:

    K0 = gamma * P0
    omega = 2*np.pi*f
    G1 = sigma * phi / (alpha_unend * dichte * omega)

    G2 = 4*((alpha_unend)**2) * dichte * viskosität * omega / ((sigma*phi*viskosität_L)**2)

    G1_dot = 8*viskosität / (dichte * Pr * ((thermisch_L)**2) * omega)

    G2_dot = dichte * Pr * ((thermisch_L)**2) * omega / (16*viskosität)

    dichte_p = dichte * alpha_unend * (1- 1j*G1*np.sqrt(1+1j*G2)) / phi

    K_p = K0*phi**(-1) / (gamma - (gamma-1)*((1- 1j*G1_dot*np.sqrt(1+ 1j*G2_dot))**-1))

    kp = omega * np.sqrt(dichte_p/K_p)
    Zp = np.sqrt(dichte_p*K_p)

    return Zp, kp