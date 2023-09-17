import traci
import time
import pyodbc
import datetime as dt

import functions as fn

sumoCmd = ["sumo-gui", "-c", "demo.sumocfg"]

# Change the name of your SERVER in SERVER=KKUSIC-L\SQLEXPRESS (see your database), and UID=FPZ\kkusic (used by SQL authentication)
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-Q9818VV\SQLEXPRESS;DATABASE=PVD_traffic_data;UID=DESKTOP-Q9818VV\quang;TRUSTED_CONNECTION=yes')
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
    if step % 50 == 0:
        # Get a list of all currently existing vehicle IDs
        existing_vehicle_ids = traci.vehicle.getIDList()

        current_utc = dt.datetime.utcnow()
        current_time = (current_utc - dt.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
        select_vehicle_E = """SELECT TOP 1 ID, VerhicleID, RouteId, DepartLane, TypeID FROM tblVehicles WHERE Active = 0 ORDER BY ID ASC"""
        cursor = conn.cursor()
        cursor.execute(select_vehicle_E)
        for row in cursor:
            # X_0224_01[0] = row[0]
            # vehicle_id = row[1] + str(step) # perform test
            vehicle_id = row[1]
            route_id = row[2]
            depart_lane = row[3]
            vehicle_type = row[4]

        time.sleep(0.1)

        if vehicle_id in existing_vehicle_ids:
            continue

        print(vehicle_id, route_id, depart_lane, vehicle_type)
        traci.vehicle.add(vehicle_id, route_id, departLane=depart_lane, typeID=vehicle_type)

        update_vehicle_E = """UPDATE tblVehicles SET Active = 1 WHERE VerhicleID = '""" + vehicle_id + """' """
        print('--- Update >>> ', update_vehicle_E)
        cursor.execute(update_vehicle_E)
        conn.commit()

    traci.simulationStep()
    print(step)

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
