#TRACK procedue

#module imports
import math as m
import numpy as np
import matplotlib.pyplot as plt

#Inputs
RS = ([0.2045722954607165], [-0.7510041403438963], [0.6304676042834403])  #Position Vector of Radar Station, Units: DU
VS = ([0.04418432], [0.01203574], [0])                                    #Velocity Vector of Radar Station, Units: DU/TU
latitude = 39.007                                                   #Latitude, Units (degrees) (north is positive)
longitude = 285.2375765519521                                       #Longitude, Units (degrees) (east is positive)
slant_range = 504.68                                                #Slant range, Units: km
slant_rate = 2.08                                                   #Slant range, Units: km/s
elevation_angle = 30.7                                              #Elevation angle, Units: degrees
elevation_rate = 0.07                                               #Elevation rate, Units: degrees/sec
azimuth_angle = 105.6                                               #Azimuth angle, Units: degrees
azimuth_rate = 0.05                                                 #Azimuth rate, Units: degrees/sec

#Conversions to canonical units
lat = m.radians(latitude)
long = m.radians(longitude)
rho = slant_range / 6378.145            #6378.145 km / 1 DU
rho_dot = slant_rate / 7.90536828       #7.90536828 km/s / 1 DU/TU
el = m.radians(elevation_angle)
el_dot = m.radians(elevation_rate) / (1.239446309*(10**(-3)))
az = m.radians(azimuth_angle)
az_dot = m.radians(azimuth_rate) / (1.239446309*(10**(-3)))


if __name__ == "__main__":
    rho_vect = ([-rho*m.cos(el)*m.cos(az)],[rho*m.cos(el)*m.sin(az)],[rho*m.sin(el)])
    rho_dot_vect = ([-rho_dot*m.cos(el)*m.cos(az)+rho*m.sin(el)*el_dot*m.cos(az)+rho*m.cos(el)*m.sin(az)*az_dot],
                    [rho_dot*m.cos(el)*m.sin(az)-rho*m.sin(el)*el_dot*m.sin(az)+rho*m.cos(el)*m.cos(az)*az_dot],
                    [rho_dot*m.sin(el)+rho*m.cos(el)*el_dot])
    rotation_matrix = ([m.sin(lat)*m.cos(long), -m.sin(long), m.cos(lat)*m.cos(long)],
                       [m.sin(lat)*m.sin(long), m.cos(long), m.cos(lat)*m.sin(long)],
                       [-m.cos(lat), 0, m.sin(lat)])

    r_sat_ijk = np.dot(rotation_matrix, rho_vect) + RS
    v_sat_ijk = np.dot(rotation_matrix, rho_dot_vect) + VS

    print(long)
    print("Satellite Position Vector: ", r_sat_ijk)
    print("Satellite Velocity Vector: ", v_sat_ijk)    
    
    
    
