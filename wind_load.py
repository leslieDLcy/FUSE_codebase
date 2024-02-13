import numpy as np
import matplotlib.pyplot as plt
from utils import moving_average

class Wind_load:


    def __init__(self, time, hyperparameters, V_hub, fs=100):
        self.time = time  # length of simulation (seconds)
        self.hyperparameters = hyperparameters
        self.V_hub = V_hub
        self.fs = fs


    def get_wind_speed_z(self, wind_model, turbulence_model):
        """ Return a sample of wind speed for all the heights z at time t """

        # compute the mean wind speed at height z
        u = np.random.uniform(low=0, high=1, size=1)

        if wind_model == 'normal':
            V_z = self.V_hub * (self.hyperparameters.z / self.hyperparameters.z_hub)**0.2

            # a sample of wind speed distribution
            # u = np.random.uniform(low=0, high=1, size=len(V_z))
            sample_z = np.sqrt(- (4 * V_z**2 / np.pi ) * np.log(1 - u))

        elif wind_model == 'extreme':
            # gaussian mean
            V_z = 1.4 * self.hyperparameters.V_ref * (self.hyperparameters.z / self.hyperparameters.z_hub)**0.11
            sample_z = V_z

        # the second level distribution (Gaussian)
        # determine the sigma of the second level distribution
        if turbulence_model == 'normal':
            sigma1 = self.hyperparameters.Iref * (0.75 * self.V_hub + 5.6)
        elif turbulence_model == 'extreme':
            sigma1 = 2 * self.hyperparameters.Iref * (0.072 * (self.hyperparameters.V_ave/self.hyperparameters.c + 3) * (self.V_hub/self.hyperparameters.c -4) + 10)
        
        return sample_z, sigma1



    def cp_wind_speed_interpolation(self, V_z):
        """ interpolate the wind speed between two nodes 
        
        steps:
            1. compute the wind speed for each node as usual (i.e. `sample_z`)   
            2. linearly interpolate the wind speed between two nodes
        """
        # append a zero at the front and then compute the moving average
        ave_speed_elements = np.insert(arr=V_z, obj=0, values=0.)
        ave_speed_elements = moving_average(ave_speed_elements, 2)
        return ave_speed_elements




    def get_wind_speed_z_interpolation(self, wind_model, turbulence_model):
        """ Return a sample of wind speed for all the heights z at time t """

        # compute the mean wind speed at height z
        u = np.random.uniform(low=0, high=1, size=1)

        if wind_model == 'normal':
            V_z = self.V_hub * (self.hyperparameters.z / self.hyperparameters.z_hub)**0.2

            V_z = self.cp_wind_speed_interpolation(V_z)

            # a sample of wind speed distribution
            # u = np.random.uniform(low=0, high=1, size=len(V_z))
            sample_z = np.sqrt(- (4 * V_z**2 / np.pi ) * np.log(1 - u))

        elif wind_model == 'extreme':
            
            # gaussian mean
            V_z = 1.4 * self.hyperparameters.V_ref * (self.hyperparameters.z / self.hyperparameters.z_hub)**0.11
            sample_z = V_z

        # the second level distribution (Gaussian)
        # determine the sigma of the second level distribution
        if turbulence_model == 'normal':
            sigma1 = self.hyperparameters.Iref * (0.75 * self.V_hub + 5.6)
        elif turbulence_model == 'extreme':
            sigma1 = 2 * self.hyperparameters.Iref * (0.072 * (self.hyperparameters.V_ave/self.hyperparameters.c + 3) * (self.V_hub/self.hyperparameters.c -4) + 10)
        
        return sample_z, sigma1











    def get_wind_speed_series(self, mu, sigma):

        """ assume i.i.d. Gaussian process samples 
        
        args:
            mu: mean of the Gaussian process;
            sigma: standard deviation of the Gaussian process;
            fs: sampling frequency;
        return:
            heigh * time matrix of wind speed;
        """
        sigma_array = np.repeat(sigma, len(mu))
        ts = np.array([np.random.normal(mu, sigma, size=self.time * self.fs) for mu, sigma in zip(mu, sigma_array)])

        return ts


    def save_wind_speed_series(self, ts):
        np.savetxt("wind_speed_series.csv", ts, delimiter=",")



    def plot_wind_speed_series(self, ts, node_index):

        """ Plot the wind speed time series at node_index 
        
        args:
            node_index: the index of node (from bottom to top)
        """

        fig, ax = plt.subplots(figsize=(10, 3))
        xaxis = np.linspace(0, self.time, self.time * self.fs)
        ax.plot(xaxis, ts[node_index])
        ax.set_xlabel('time (s)')
        ax.set_ylabel('wind speed (m/s)')
        ax.set_title('wind speed at height the {}m'.format(self.hyperparameters.z[node_index]))


    def cp_dragforce_f(self, wind_speed_series):
        """ Implementing the Eq. (2) to compute drag force 
        f only not F
        """

        linear_scale = 0.5 * self.hyperparameters.p * self.hyperparameters.cd 
        middle = [a * b**2 for a, b in zip(self.hyperparameters.Diameter, wind_speed_series)]
        return linear_scale * np.array(middle)



    """ a copy of Francesca's idea w.r.t the area to use in Eq. 2"""
    # def cp_dragforce_f(self, wind_speed_series):
    #     """ Implementing the Eq. (2) to compute drag force 
    #     f only not F
    #     """

    #     linear_scale = 0.5 * self.hyperparameters.p * self.hyperparameters.cd 
    #     middle = [a * b**2 for a, b in zip(self.hyperparameters.An, wind_speed_series)]
    #     return linear_scale * np.array(middle)




    def get_wind_loads_F(self, wind_speed_series):
        """ Implementing the Eq. (2) to compute drag force 
        
        computing F
        """

        linear_scale = 0.5 * self.hyperparameters.p * self.hyperparameters.cd * self.hyperparameters.delta_h
        middle = [a * b**2 for a, b in zip(self.hyperparameters.cross_sec_area, wind_speed_series)]
        result = [scalar * vector for scalar, vector in zip(linear_scale, np.array(middle))]
        return np.array(result)




    def cp_wind_loads_F_hub(self, sigma):

        """
        
        steps:
            1. wind speed at hub height;
            2. uniform f with the hub area;
        """
        # compute wind speed series at hub height
        ws_hub = self.get_Vhub_series(sigma=sigma)

        # the second step
        linear_scale = 0.5 * self.hyperparameters.p * self.hyperparameters.cd
        F_hub_height = ws_hub**2 * self.hyperparameters.rotor_area
        return np.array(F_hub_height) * linear_scale
    



    def compute_moments(self, ft):
        """ q* (l^)2 / 8 """

        return np.array([q*(l**2) for q, l in zip(ft, self.hyperparameters.delta_h)])





    def plot_wind_loads(self, wind_loads, node_index):

        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(wind_loads[node_index])
        ax.set_xlabel('time (s)')
        ax.set_ylabel('drag forces')
        ax.set_title('drag forces at the height {}m'.format(self.hyperparameters.z[node_index]))


    def save_wind_load_series(self, ts, name, style='Francesca'):
        # np.savetxt(f"{name}.csv", ts, delimiter=",")
        if style == 'Francesca':
            ts = np.transpose(ts)
        elif style == 'igonre':
            pass
        np.savetxt(f"{name}.txt", ts, delimiter=",", newline="\n")


    def get_turbulence():
        """ Return turbulence at time t """
        pass


    def get_Vhub_series(self, sigma):
        return np.random.normal(loc=self.hyperparameters.V_ref, scale=sigma, size=self.time * self.fs)