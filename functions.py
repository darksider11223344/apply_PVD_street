import traci


def TTS_Total():
    numberOfVeh = traci.vehicle.getIDCount()
    return numberOfVeh

def getVehIds():
    listVehIDs = traci.vehicle.getIDList()
    return listVehIDs


def edgeVehParameters(edgeStart, edgeStartPlusOne, oldVehIDs):
    intersection = set(oldVehIDs).intersection(traci.edge.getLastStepVehicleIDs(edgeStartPlusOne))

    if len(list(intersection)) != 0:
        for idVeh in list(intersection):
            indexVeh = oldVehIDs.index(idVeh)
            del oldVehIDs[indexVeh]

    currentVehIDs = traci.edge.getLastStepVehicleIDs(edgeStart)
    newVehIDs = []
    for vehID in currentVehIDs:
        if vehID not in oldVehIDs:
            newVehIDs.append(vehID)
    n = 0
    speed = 0
    for vehID in newVehIDs:
        speed += traci.vehicle.getSpeed(vehID)
        oldVehIDs.append(vehID)
        n = n + 1
    flow = n

    return flow, speed, oldVehIDs, newVehIDs