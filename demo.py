import traci
import time
import pyodbc

import functions as fn

sumoCmd = ["sumo-gui", "-c", "demo.sumocfg"]


# Change the name of your SERVER in SERVER=KKUSIC-L\SQLEXPRESS (see your database), and UID=FPZ\kkusic (used by SQL authentication)
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-Q9818VV\SQLEXPRESS;DATABASE=PVD_traffic_data;UID=DESKTOP-Q9818VV\quang;TRUSTED_CONNECTION=yes')
time.sleep(0.1)

hours = 24
run = 0
res_time = 1
step_length = 0.25

traci.start(sumoCmd)
step = 0

# Define vehicle parameters
vehicle_id = "vehicle_1"  # Unique ID for the vehicle
vehicle_type = "vtype_car1"  # Type of vehicle (you need to define this type in your SUMO configuration)
route_id = "route_0"  # ID of the route the vehicle will follow


# Add a vehicle to the simulation
# traci.vehicle.add(vehicle_id, route_id, departLane="free", typeID=vehicle_type)

# while (traci.simulation.getMinExpectedNumber() > 0):
while True:
    if step % 100 == 0:
        traci.vehicle.add(vehicle_id + str(step), route_id, departLane="free", typeID=vehicle_type)
    traci.simulationStep()
    # print(step)

    oldVehIDs_E_in = []


    if step % (res_time * (1 / step_length)) == 0:
        flow_E_in, speed_E_in, oldVehIDs_E_in, newVehIDs_E_in = \
            fn.edgeVehParameters('404516659#1', '404516659#2', oldVehIDs_E_in)
        # print(flow_E_in, speed_E_in, oldVehIDs_E_in, newVehIDs_E_in)


    # setFlow(self, calibratorID, begin, end, vehsPerHour, speed, typeID, routeID, departLane='first', departSpeed='max')
    traci.calibrator.setFlow("caliCar1_E_W_0", 0, 60, 180, 1, \
                             'vtype_car1', 'route_cali_E_W', \
                             departLane="free", departSpeed='max')

    step += 1
    time.sleep(0.1)

traci.close()
