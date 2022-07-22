import math as m
import matplotlib as plt
import numpy as np

RSSI_1M = -50 #dBm

PATH_LOSS = 4 #dBm

STD_DEV = 5.1 #dB

def  rssiCalc(distance, useRV):
    if distance >= 1:
        if useRV:
            return (-10*PATH_LOSS*m.log10(distance) + RSSI_1M + np.random.normal(0,pow(STD_DEV, 2),1))
        else:
            return (-10*PATH_LOSS*m.log10(distance) + RSSI_1M)
    else:
        return 0

def distanceCalc(loc1, loc2):
    return m.sqrt(m.pow(loc1[0]-loc2[0],2) + m.pow(loc1[1]-loc2[1],2) + m.pow(loc1[2]-loc2[2],2))

def diffSquare(p1, p2):
    return pow(p1-p2, 2)

def meanSquare(f1, f2):
    sum = 0
    for i in range(len(f1)):
        sum += diffSquare(f1[i], f2[i])
    return sum/len(f1)

class Sensor:

    def __init__(self, loc):
        self.loc = loc

    def getLoc(self):
        return self.loc

class Target:

    def __init__(self, loc) -> None:
        self.loc = loc

    def getLoc(self):
        return self.loc

    def rssi(self, sensor):
        return rssiCalc(distanceCalc(self.loc, sensor.getLoc()), True)

class Tile:

    def __init__(self, loc):
        self.loc = loc
        self.fingerprints = []

    def addFingerprint(self, sensor):
        self.fingerprints.append(rssiCalc(distanceCalc(self.loc, sensor.getLoc()), False))

    def getFingerprint(self):
        return self.fingerprints

    def getLoc(self):
        return self.loc


class Building:

    def __init__(self, size, sensors) -> None:
        self.size = size
        self.sensors = sensors
        self.tiles = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    self.tiles.append(Tile((i,j,k)))

        for tile in self.tiles:
            for sensor in self.sensors:
                tile.addFingerprint(sensor)

    def estimateLoc(self, target):
        targetFingerprint = []
        for sensor in self.sensors:
            targetFingerprint.append(target.rssi(sensor))

        closestTile = self.tiles[0]
        leastMeanSquare = meanSquare(closestTile.getFingerprint(), targetFingerprint)

        for tile in self.tiles:
            ms = meanSquare(tile.getFingerprint(), targetFingerprint)
            if ms < leastMeanSquare:
                leastMeanSquare = ms
                closestTile = tile

        return closestTile.getLoc()

if __name__ == "__main__":

    s1 = Sensor((0,30,3))
    s2 = Sensor((50,60,4))
    s3 = Sensor((100,30,3))
    target = Target((30,45,0))
    building = Building((100,60,5),[s1,s2,s3])

    x = y = z = 0

    """print(rssiCalc(10, False))

    sum = 0

    for i in range(10):
        r = rssiCalc(10, True)
        print(r)
        sum += r

    print("avg rssi: ",sum/10)"""

    for i in range(10):
        loc = building.estimateLoc(target)
        print(loc)
        x += loc[0]
        y += loc[1]
        z += loc[2]

    approxLoc = [x/10, y/10, z/10]

    print(approxLoc)