#Project Site-Track

#import modules
import math as m
import numpy as np
import matplotlib.pyplot as plt

#inputs
latitude = 29.8                             #geodetic latitude (degrees)
theta_e = -78.5                             #longitude in east direction(degrees) (Long w is negative)
H = 0.004572                                #altitude above mean sea level (km)
date_list = [277, 12, 1970]                 #Date [day, month, year]
UT = [22, 10, 57.5]                         #Time [hour, minutes, seconds]

slant_range = 1510                          #Slant range, Units: km
slant_rate = 4.5                            #Slant range, Units: km/s
elevation_angle = 135                       #Elevation angle, Units: degrees
elevation_rate = 0.53                       #Elevation rate, Units: degrees/sec
azimuth_angle = 0                           #Azimuth angle, Units: degrees
azimuth_rate = 0.5                          #Azimuth rate, Units: degrees/sec

#constants and lookups
month_day = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
ae = 1                              #equatorial radius, Units: DU
e = 0.08182                         #eccentricity
omega = 6.300388099                 #angular rotation, Units: rad/day
GST_1970 = 100.229420782            #Greenwich Sidereal Time - Jan 1 1970
omega_vector = [0, 0, 0.0588336565] #angular rotation vector, Units: rad/TU

#Conversions to canonical units
lat = m.radians(latitude)
rho = slant_range / 6378.145            #6378.145 km / 1 DU
rho_dot = slant_rate / 7.90536828       #7.90536828 km/s / 1 DU/TU
el = m.radians(elevation_angle)
el_dot = m.radians(elevation_rate) / (1.239446309*(10**(-3)))
az = m.radians(azimuth_angle)
az_dot = m.radians(azimuth_rate) / (1.239446309*(10**(-3)))

#functions    
def dt_to_day(date_list, UT) ->float:
    time_to_day = (UT[0] / 24) + (UT[1] / 1440) + (UT[2] / 86400)
    if (date_list[2] % 4) == 0:
        return month_day[date_list[1]+11] + (date_list[0]-1) + time_to_day
    else:
        return month_day[date_list[1]-1] + (date_list[0]-1) + time_to_day

def long(theta_e, day ,GST_1970) ->float:
    return (m.radians(GST_1970 + theta_e) + omega*day) % (2*m.pi)

def dist_to_DU(dist) ->float:
    return dist / 6378.145

def x(lat, H) ->float:
    return abs((ae/m.sqrt(1 - (e**2)*(m.sin(lat)**2)) + dist_to_DU(H))*m.cos(lat))

def z(L, H) ->float:
    return abs((ae/m.sqrt(1 - (e**2)*(m.sin(lat)**2)) + dist_to_DU(H))*m.sin(lat))


if __name__ == "__main__":
    day = dt_to_day(date_list,UT)
    long = long(theta_e, day, GST_1970)
    x = x(lat,H)
    z = z(lat,H)
    RS = [x*m.cos(long), x*m.sin(long), z]
    VS = np.cross(omega_vector,RS)
    
    #Generate SEZ track vectors and rotation matrix
    rho_vect = ([-rho*m.cos(el)*m.cos(az)],[rho*m.cos(el)*m.sin(az)],[rho*m.sin(el)])
    rho_dot_vect = ([-rho_dot*m.cos(el)*m.cos(az)+rho*m.sin(el)*el_dot*m.cos(az)+rho*m.cos(el)*m.sin(az)*az_dot],
                    [rho_dot*m.cos(el)*m.sin(az)-rho*m.sin(el)*el_dot*m.sin(az)+rho*m.cos(el)*m.cos(az)*az_dot],
                    [rho_dot*m.sin(el)+rho*m.cos(el)*el_dot])
    rotation_matrix = ([m.sin(lat)*m.cos(long), -m.sin(long), m.cos(lat)*m.cos(long)],
                       [m.sin(lat)*m.sin(long), m.cos(long), m.cos(lat)*m.sin(long)],
                       [-m.cos(lat), 0, m.sin(lat)])

    #Generate R,V vectors for tracked satellite
    r_sat_ijk = np.dot(rotation_matrix, rho_vect) + ([RS[0]],[RS[1]],[RS[2]])
    v_sat_ijk = np.dot(rotation_matrix, rho_dot_vect) + ([VS[0]],[VS[1]],[VS[2]])

    print("Radar Site Location Vector (IJK): ", RS)
    print("Radar Site Velocity Vector (IJK): ", VS)
    print("Radar Site Sidereal Time: ", m.degrees(long))
    print("Radar Site Latitude: ", lat)
    print("Satellite Position Vector: ", r_sat_ijk)
    print("Satellite Velocity Vector: ", v_sat_ijk)

    #Generate IJK orbit track
    
    #Generate data for wirefram Earth
    u,v =  np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    
    px = ae*np.cos(u)*np.sin(v)
    py = ae*np.sin(u)*np.sin(v)
    pz = ae*np.cos(v)

    #Plot
    fig = plt.figure(figsize=(15,15))

    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    ax.set_zlim(-1.5,1.5)
    ax.plot_wireframe(px, py, pz, rstride=1, cstride=1, color='green', linewidth=0.5)
    ax.quiver(0,0,0,RS[0],RS[1],RS[2])
    ax.quiver(RS[0],RS[1],RS[2],VS[0],VS[1],VS[2], color='red')
    ax.quiver(0, 0, 0, r_sat_ijk[0], r_sat_ijk[1], r_sat_ijk[2])
    ax.quiver(r_sat_ijk[0], r_sat_ijk[1], r_sat_ijk[2], v_sat_ijk[0], v_sat_ijk[1], v_sat_ijk[2])
    plt.title('Position and Velocity Vector of Radar Station (DU)')
    ax.view_init(azim=0, elev=30)
    plt.show()