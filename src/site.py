#SITE procedure

#module imports
import math as m
import numpy as np
import matplotlib.pyplot as plt

#Inputs
Lat = 39.007                        #geodetic latitude (degrees)
theta_e = -104.883                  #longitude in east direction(degrees) (Long w is negative)
H = 2.188464                        #altitude above mean sea level (km)
date_list = [2, 9, 1970]            #Date [day, month, year]
UT = [3, 17, 2]                     #Time [hour, minutes, seconds]

#Constants/Lookups
month_day = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
ae = 1                              #equatorial radius, Units: DU
e = 0.08182                         #eccentricity
omega = 6.300388099                 #angular rotation, Units: rad/day
GST_1970 = 100.229420782            #Greenwich Sidereal Time - Jan 1 1970
omega_vector = [0, 0, 0.0588336565] #angular rotation vector, Units: rad/TU

#functions    
def dt_to_day(date_list, UT) ->float:
    time_to_day = (UT[0] / 24) + (UT[1] / 1440) + (UT[2] / 86400)
    if (date_list[2] % 4) == 0:
        return month_day[date_list[1]+11] + (date_list[0]-1) + time_to_day
    else:
        return month_day[date_list[1]-1] + (date_list[0]-1) + time_to_day

def long(theta_e, day ,GST_1970) ->float:
    return m.radians(GST_1970 + theta_e) + omega*day

def dist_to_DU(dist) ->float:
    return dist / 6378.145

def x(Lat, H) ->float:
    return abs((ae/m.sqrt(1 - (e**2)*(m.sin(m.radians(Lat))**2)) + dist_to_DU(H))*m.cos(m.radians(Lat)))

def z(L, H) ->float:
    return abs((ae/m.sqrt(1 - (e**2)*(m.sin(m.radians(Lat))**2)) + dist_to_DU(H))*m.sin(m.radians(Lat)))


if __name__ == "__main__":
    day = dt_to_day(date_list,UT)
    long = long(theta_e, day, GST_1970)
    x = x(Lat,H)
    z = z(Lat,H)
    RS = [x*m.cos(long), x*m.sin(long), z]
    VS = np.cross(omega_vector,RS)

    print("Radar Site Location Vector (IJK): ", RS)
    print("Radar Site Velocity Vector (IJK): ", VS)
    
    u,v =  np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    
    px = ae*np.cos(u)*np.sin(v)
    py = ae*np.sin(u)*np.sin(v)
    pz = ae*np.cos(v)

    fig = plt.figure(figsize=(15,15))

    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    ax.set_zlim(-1.5,1.5)
    ax.plot_wireframe(px, py, pz, rstride=1, cstride=1, color='green', linewidth=0.5)
    ax.quiver(0,0,0,RS[0],RS[1],RS[2])
    ax.quiver(RS[0],RS[1],RS[2],VS[0],VS[1],VS[2], color='red')
    plt.title('Position and Velocity Vector of Radar Station (DU)')
    ax.view_init(azim=0, elev=30)
    plt.show()


