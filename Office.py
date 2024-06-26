import networkx as nx
import geopy.distance
import time
#----------------------------------------------------------------------------------------------
#
#
# A* for secure paths to an emergency exit
#
#The program is designed to run on HMI screens mounted nearby some interested points of a  fictional building.
#All these points are saved in a database. The aim of the problem is to show on output the best direction to go to
#reach safety the nearest exit
#
#
#----------------------------------------------------------------------------------------------


def main():
    # open the db file
    file = open("Data1.txt", "r")
    #ask the status of the smoke detectors
    # smoke detector outputs: (true: smoke is not detected false: smoke is detected)
    print("Smoke sensors status [0 Alarm | 1 Normal] :")
    print("Sensor 1 [Ground floor Ovest]")
    smokeDetector1 = input()
    print("Sensor 2 [Ground floor East]")
    smokeDetector2 = input()
    print("Sensor 3 [First floor East]")
    smokeDetector3 = input()
    print("Sensor 4 [First floor Ovest]")
    smokeDetector4 = input()
    print("Sensor 5 [Second floor East]")
    smokeDetector5 = input()
    print("Sensor 6 [Second floor Ovest]")
    smokeDetector6 = input()

    # ask the position of the hmi screen
    print("Start position [Position of the HMI screen] :")
    start_node = input()

    print("Output to the HMI screen :")
    # verifies the state of the sensors
    if (int(smokeDetector1) == 1 and int(smokeDetector2) == 1 and int(smokeDetector3) == 1 and int(
            smokeDetector4) == 1 and int(smokeDetector5) == 1 and int(smokeDetector6) == 1):
        print("All secure")
    else:
        print("FIRE ALARM")

        # Extract all the points from the database and draw a graph
        G = nx.Graph()
        lines = file.read().splitlines()
        for line in range(len(lines)):
            n = list(lines[line].split(' '))
            m = []
            for word in n:
                m.append(word)
            G.add_node(str(m[0]), x=m[1], y=m[2], s=m[3])
        for line in range(len(lines)):
            n = list(lines[line].split(' '))
            m = []
            for word in n:
                m.append(word)
            for i in range(4, len(m)):
                coords1 = [float(m[1]), float(m[2])]
                coords2 = [float(G.nodes[str(m[i])]['x']), float(G.nodes[str(m[i])]['y'])]
                if G.has_edge(m[0], m[i]):
                    continue
                else:
                    G.add_edge(m[0], m[i], weight=geopy.distance.geodesic(coords1, coords2).m)

        # The end node is always safe a node connected to all the four possible emergency exits
        end_node = "Safe"

        # Physical distance between the two nodes
        def dist(a, b):
            (x1, y1) = [float(G.nodes[a]['x']), float(G.nodes[a]['y'])]
            (x2, y2) = [float(G.nodes[b]['x']), float(G.nodes[b]['y'])]
            d = (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
            return d

        # Shows if there are any active alarms near the node
        def Alarmpresence(a):
            if int(G.nodes[a]['s']) == 1 and (not int(smokeDetector1) == 1):
                return True
            if int(G.nodes[a]['s']) == 2 and (not int(smokeDetector2) == 1):
                return True
            if int(G.nodes[a]['s']) == 3 and (not int(smokeDetector3) == 1):
                return True
            if int(G.nodes[a]['s']) == 4 and (not int(smokeDetector4) == 1):
                return True
            if int(G.nodes[a]['s']) == 5 and (not int(smokeDetector5) == 1):
                return True
            if int(G.nodes[a]['s']) == 6 and (not int(smokeDetector6) == 1):
                return True
            return False

        # Shows if the node is an elevator node
        def isElevator(a):
            if int(G.nodes[a]['s']) == 7:
                return True
            return False

        def total(a, b, c):
            # The node we are looking to move to is to be considered not secure if there is an active alarm
            # on that node or if it is an elevator
            safety = 0
            if Alarmpresence(b) or isElevator(b):
                safety = 10000
            # The physical distance between the two nodes
            ab = [float(G.nodes[a]['x']), float(G.nodes[a]['y'])]
            cd = [float(G.nodes[b]['x']), float(G.nodes[b]['y'])]
            partial_distance = geopy.distance.geodesic(ab, cd).km
            # In the end to draw the best path we take in account both the distance and the security of the path
            totals = partial_distance + safety
            return totals

        # use A* algorithm to find the best path
        alfa = nx.astar_path(G, start_node, end_node, heuristic=dist, weight=total)
        print(alfa)
        print("Go to ", alfa[1], "and follow the next instructions to get to the nearest emergency exit")
        time.sleep(10)

if __name__ == "__main__":
    main()

