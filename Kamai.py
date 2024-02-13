import numpy as np
import matplotlib.pyplot as plt

class Kamai:
    def __init__(self, V_hub, sigma_1, z):
        """ we assume k=1 meaning longtitude direction """
        self.V_hub = V_hub 
        self.sigma_1 = sigma_1
        self.z = z
        self.f_axis = np.linspace(0, 0.5, 1000)  # frequency axis [Hz]



    @property
    def Lambda_1(self,):
        """ for the Eq. 5 on page 25 """

        if self.z > 60:
            return 42
        else:
            return 0.7 * self.z

    @property
    def L_k(self,):
        return self.Lambda_1 * 8.1
    

    def get_spectrum(self):
        
        chunk = self.L_k / self.V_hub
        
        numerator = 4 * self.sigma_1**2 * chunk
        denominator = (1 + 6 * self.f_axis * chunk)**(5/3)

        S_f = numerator / denominator
        
        return S_f
    

    def plot_spectrum(self, S_f, style='linear'):
        """ plot the spectrum 
        todo: add the loglog scale.
        """
        fig, ax = plt.subplots()
        ax.plot(self.f_axis, S_f)
        ax.set_ylabel('Power spectral Density')
        ax.set_xlabel('Frequency [Hz]')
        ax.grid(linestyle=':')
        if style == 'log':
            ax.set_yscale('log')
            ax.set_xscale('log')
            ax.set_title('Kaimal Spectrum (loglog scale)')
        else:
            ax.set_title('Kaimal Spectrum (linear scale)')

