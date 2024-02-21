import numpy as np
from wind_load import Wind_load
from params import Params
import matplotlib.pyplot as plt

params = Params()

# In the event of NTM case, Merhad said V_hub = 0.7 * V_ref

wl_EN = Wind_load(time=600, hyperparameters=params, V_hub=params.V_ref, fs=2) 


# import wind speed time series from Matthew
matthew_ws = np.loadtxt('data/interp_windspeed.txt')

# remove the last row for keeping consistent with the shape: 600s * 2Hz = 1200
matthew_ws = matthew_ws[0:-1]

###  computing drag force `f` for the elements ###
ft = wl_EN.cp_dragforce_f(wind_speed_series=np.transpose(matthew_ws[:, :-1]))
# pad zeros to the end .. 60 seconds
ft_0padded = wl_EN.zero_padding(input_series=ft, duration=60)
# save it to Francesca
wl_EN.save_wind_load_series(ts=ft_0padded, name='matthew_load_elements_0padded', style='Francesca')



### compute nodal force ###
# compute the load for the rotor at the hub
F_hub = wl_EN.cp_wind_loads_F_hub_external(external=matthew_ws[:, -1])
# pad zeros to the end .. 60 seconds
F_hub_0padded = wl_EN.zero_padding(input_series=F_hub, duration=60)
wl_EN.save_wind_load_series(ts=F_hub_0padded, name='Matthew_load_nodal_hub_0padded', style='ignore')

### a final check of the wind speed series at the highest node ###
# plot the wind speed series at the highest node
wl_EN.plot_wind_speed_series(np.transpose(matthew_ws), node_index=-1)