import numpy as np

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