""" Hyperparameters for the wind turbine loading case """

from dataclasses import dataclass
from utils import moving_average
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
    
    Iref = 0.16
    c=2

    V_ave = 8.9
    V_ref = 50

    # to compute wind loads Eq.(2) of paper Moira Di Paolo

    p = 1.225 # air density
    cd = 0.5 # drag coefficient
    # area of elements
    An = np.array([0.496861728, 0.295312851, 0.282306657, 0.269300464, 0.25629427, 0.243288077, 0.229559317, 0.216553123, 0.20354693, 0.190540736, 0.177534542])

    # for computation of F and M only
    # plus 1 at the end
    # area_com = np.array([0.496861728, 0.295312851, 0.282306657, 0.269300464, 0.25629427, 0.243288077, 0.229559317, 0.216553123, 0.20354693, 0.190540736, 0.177534542, 0.177534542])

    # average height of the elements, nodes at the middle
    # area_ave = np.array([0.39608729, 0.28880975, 0.27580356, 0.26279737, 0.24979117, 0.2364237 , 0.22305622, 0.21005003, 0.19704383, 0.18403764, 0.17753454])


    # plus one height of the hub
    # heights_com = np.array([42.55, 45.434, 48.318, 51.202, 54.086, 56.97, 59.854, 62.738, 65.622, 68.506, 71.39, 75.3])


    Diameter = np.array([4.200, 4.110, 3.930, 3.750, 3.570, 3.390, 3.200, 3.020, 2.840, 2.660, 2.480])

    # @property
    # # template for property
    # def sth(self):
    #     """ template for property"""
    #     return int(round(self.patch_window_seconds / self.stft_hop_seconds))
    
    @property
    def area_com(self):
        """ plus 1 at the end """

        return np.append(arr=self.An, values=self.An[-1])
    

    @property
    def area_ave(self):
        """ plus 1 at the end """

        return moving_average(self.area_com, 2)


    @property
    def heights_com(self):
        """ height for computation, plus 1 at the end, plus a 0 at the front. """
        heights_com = np.insert(arr=self.z, obj=0, values=0.)
        return np.append(arr=heights_com, values=self.z_hub)


    @property
    def delta_h(self):
        """ template for property"""

        middle_h = moving_average(self.heights_com, 2)
        return np.diff(middle_h)


    @property
    def cross_sec_area(self):
        """ template for property"""

        return self.delta_h * self.Diameter