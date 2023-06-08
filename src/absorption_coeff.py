import models
import numpy as np
import utils

class AbsorptionCoeff:

    # soll das hier auch in utils.py eurer Meinung nach?
    # absorber_layers sollte auch eine Liste von Modellen sein können

    def __init__(self, L1, L2, f_min, f_max, absorber_layers: models.AbsorberModelInterface, air_density, air_c, angle):
        self.alphas = np.array([])
        self.L1 = L1
        self.L2 = L2
        self.f_min = f_min
        self.f_max = f_max
        self.absorber_layers = absorber_layers
        self.air_density = air_density # luft_dichte
        self.air_c = air_c # Luft_c
        self.impedance = self.air_density * self.air_c
        self.angle = angle # Einfallswinkel

    def absorption_coeffs(self):
        for f in range(self.f_min, self.f_max):
            try:
                self.absorber_layers.set_f(f) 
                Z1 = self.absorber_layers.get_Zp()
                k1 = self.absorber_layers.get_kp()
                k2 = 2 * np.pi * f / self.air_c
                
                # Berechnung der TMM-Matrix
                T_total = utils.tmm(k1,self.L1,Z1,k2,self.L2,self.impedance)

                # Absorptionsgrad berechnen -> gehört das in tmm-fkt?
                R = (T_total[0, 0] - T_total[1, 0]*self.impedance) / (T_total[0, 0] + T_total[1, 0]*self.impedance) # Reflexionskoeffizient
                alpha = 1 - np.abs(R) ** 2
                self.alphas = np.append(self.alphas, alpha)

            except (ZeroDivisionError, ValueError):
                print('biite richtig Zahl eingeben')