# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 19:20:22 2024

@author: brody
"""

"""
This Code is Property of ARES M2I and may only be used for ARES purposes unless
prior aproval has been given by someone idk
This Python Code Uses the RocketPy library which is needed inorder for the code to
be succefly ran, all information about rocketpy can be found here
https://docs.rocketpy.org/en/latest/index.html
This Code can we used for any rocket and launch location if the variables are
changed
"""
#Imports of all Libraries
from rocketpy import Environment,SolidMotor, Rocket, Flight
from datetime import datetime, date
current = datetime.now()

#Defining Enviormental Data
date = datetime(2025, 4, 26, 8) #year, month, day, hour(UTC)
env=Environment(latitude=43.7615, longitude=-93.1643, date=date)
#^Defining Location of Launch
#Concord Nebraska (42.3397,-96.9424)


#Set Up for Autosorting which weather prediction to use
#If the date is too far out the code will use standard atmopshere
dif=date-current
difDAY=dif.days
difHOURS=dif.seconds/60/60+difDAY*24

#Defining Weather at Launch
if difDAY<11 and difDAY>2:
    #Global Forecast System (GFS) Can Predict weather 10 days out
    #Use for Launch date 3-10 Days Out
    env.set_atmospheric_model(type="Forecast",file="GFS")
    env.info()
elif difDAY<2 and difHOURS>30:
    #North American Mesoscale Forecast System (NAM) Can Predict Weather 3 Days out
    #Use for Launch 3Days-51Hours Out
    env.set_atmospheric_model(type="Forecast", file="NAM")
    env.info()
elif difHOURS<30 and difHOURS>0:
    #Rapid Refresh (RAP) Can Predict Weather 51 Hours out
    #Use for Launch 51 Hours out or Less
    env.set_atmospheric_model(type="Forecast", file="RAP")
    env.info()
    env.plots.atmospheric_model()

#Defining Rocket Information

##Defining Motor 
#https://docs.rocketpy.org/en/latest/reference/classes/motors/SolidMotor.html#rocketpy.SolidMotor
#Information on Rocket Motors Located in Docuemnt
AT_I284W= SolidMotor(
    thrust_source="AeroTech_I284W.eng", #File MUST be in same Folder
    dry_mass=0.3, #kg
    dry_inertia=(0.125, 0.125, 0.002),
    center_of_dry_mass_position=0.1,
    grains_center_of_mass_position=0.1,
    burn_time=2.16, #s
    #Grain Info
    grain_number=3,
    grain_separation=0.005,
    grain_density=1815, #kg/m^3
    grain_outer_radius=0.019, #m
    grain_initial_inner_radius=0.006,
    grain_initial_height=0.07,
    #Nozzle Info
    nozzle_radius=0.007,
    throat_radius=0.003,
    interpolation_method="linear",
    nozzle_position=0,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)
AT_I284W.all_info()

#Defining the Rocket
#NOTE: x=0 is the CG without the motor
Scylla = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    #Both of these cvs files can be obtained for RASAERO 2 or CFD
    #FILES MUST BE IN THE SAME FOLDER AS THE CODE
    power_off_drag="../data/rockets/calisto/powerOffDragCurve.csv",
    power_on_drag="../data/rockets/calisto/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)
#Adding the Motor
Scylla.add_motor(AT_I284W, position=-1.255)
#Adding the Nose Cone
nose_cone = Scylla.add_nose(length=0.55829, kind="von karman", position=1.278)

#Adding the Fins (Trapezodial)
fin_set = Scylla.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=("../data/airfoils/NACA0012-radians.txt","radians"),
)

tail = Scylla.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

main = Scylla.add_parachute(
    name="Main",
    cd_s=10.0,
    trigger=800,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = Scylla.add_parachute(
    name="Drogue",
    cd_s=1.0,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)
