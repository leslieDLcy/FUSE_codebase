""" Hyperparameters for the wind turbine loading case """

from dataclasses import dataclass
import numpy as np

'''
    notes:
'''

@dataclass(frozen=True)  # Instances of this class are immutable.
class Params:
    
    # From Simens, they have two values 68.3 and 80;
    z_hub = 73.5 

    # height of nodes
    # from Francesca
    z = np.array([42.55, 45.434, 48.318, 51.202, 54.086, 56.97, 59.854, 62.738, 65.622, 68.506, 71.39])

    delta_h = 10
    
    Iref = 0.16
    c=2

    V_ave = 8.9
    V_ref = 50

    # to compute wind loads Eq.(2) of paper Moira Di Paolo

    p = 1.225 # air density
    cd = 0.5 # drag coefficient
    # area of elements
    An = np.array([0.496861728, 0.295312851, 0.282306657, 0.269300464, 0.25629427, 0.243288077, 0.229559317, 0.216553123, 0.20354693, 0.190540736, 0.177534542])






    @property
    # template for property
    def sth(self):
        """ template for property"""

        return int(round(self.patch_window_seconds / self.stft_hop_seconds))