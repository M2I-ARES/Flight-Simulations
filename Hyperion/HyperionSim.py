# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 19:20:22 2024

@author: brody
"""

"""
This Code is Property of ARES M2I and may only be used for ARES purposes unless
prior aproval has been given by Matt Nelson
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
date = datetime(2026, 3, 27, 12) #year, month, day, hour(UTC)
env=Environment(latitude=43.7615, longitude=-93.1643, date=date)
#^Defining Location of Launch
#Concord Nebraska (42.3397,-96.9424)
#North Branch Minesota (43.7615,-93.1643)


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
elif difDAY<=2 and difHOURS>30:
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

env.set_atmospheric_model(type="Windy", file="ECMWF")

#Defining Rocket Information
##Defining Motor 
#https://docs.rocketpy.org/en/latest/reference/classes/motors/SolidMotor.html#rocketpy.SolidMotor
#Information on Rocket Motors Located in Docuemnt
AT_O3400= SolidMotor(
    thrust_source="../Data/Cesaroni_21062O3400-P.eng", #File MUST be in Data Folder

    # Dry motor properties (casing, nozzle, closures, etc.)
    dry_mass=6.5,  # kg
    dry_inertia=(0.055, 0.055, 0.0035),  # kg*m^2
    center_of_dry_mass_position=0.48,  # m
    # Propellant center of mass
    grains_center_of_mass_position=0.48,  # m
    burn_time=6.3,  # s
    # Grain geometry
    grain_number=6,
    grain_separation=0.005,  # m
    grain_density=1815,  # kg/m^3
    grain_outer_radius=0.049,  # m
    grain_initial_inner_radius=0.016,  # m
    grain_initial_height=0.145,  # m
    # Nozzle geometry
    nozzle_radius=0.022,  # m
    throat_radius=0.0105,  # m
    interpolation_method="linear",
    # Positioning
    nozzle_position=0.0,  # reference origin at nozzle
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

#Display Motor Info
#AT_O3400.all_info()
AT_O3400.draw()

#Defining the Rocket
Hyperion = Rocket(
    radius=0.1143, #m (9in Section)
    mass=51.2, #kg
    inertia=( 32.825,  32.825, .2062),
    #Both of these cvs files can be obtained for RASAERO 2 or CFD
    #FILES MUST BE IN THE Data Folder
   power_off_drag="../Data/Hyperion_CD_OFF.CSV",
   power_on_drag="../Data/Hyperion_CD_OFF.CSV",
    center_of_mass_without_motor=-2.03, #m
    coordinate_system_orientation="tail_to_nose",
)
#Adding the Motor
Hyperion.add_motor(AT_O3400, position=-4.63)

#Adding the Nose Cone
nose_cone = Hyperion.add_nose(length=0.909, kind="von karman", position=0)


#Adding the Transiton
Hyperion.add_tail(
    top_radius=0.1143,      # 6 in / 2
    bottom_radius=0.0762,   # 9 in / 2 
    length=0.889,          #m
    position=-1.823    # where the transition starts
)
#Adding the Fins (Trapezodial)
fin_set = Hyperion.add_trapezoidal_fins(
    n=3,
    root_chord=0.254,
    tip_chord=0.051,
    span=0.171,
    position=-4.351, #m
    cant_angle=0,
)

main = Hyperion.add_parachute(
    name="Main",
    cd_s=2.2,
    trigger=250,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
    radius=.914/2,
    height=.876,
    porosity=0.0432,
)

drogue = Hyperion.add_parachute(
    name="Drogue",
    cd_s=2.2,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
    radius=.914/2,
    height=.876,
    porosity=0.0432,
)

rail_buttons = Hyperion.set_rail_buttons(
    upper_button_position=-2.618,
    lower_button_position=-3.618,
    angular_position=45,
)

test_flight = Flight(
    rocket=Hyperion, environment=env, rail_length=15.2, inclination=80, heading=0
    )

test_flight.plots.all()
Hyperion.draw()
test_flight.prints.events_registered()

'''
#Generates a Google Earth File to Model the Flight
from rocketpy.simulation import FlightDataExporter

FlightDataExporter(test_flight).export_kml(
    file_name="trajectory.kml",
    extrude=True,
    altitude_mode="relativetoground",
)
'''