import math
import networkx as nx
import matplotlib.pyplot as plt
import geopy.distance
import pandas as pd
def main():

    '''Asks the user for his profile modifying the parameters to suite his needs'''
    file = open("nodes.txt", "r")
    print('Welcome to Save Your Buddy around - lago di Carezza - !')
    print ('What kind of profile do you have? Runner, Careful or Traveler? Or maybe Balanced?')
    a = input()
    if a == 'Runner':
        parameter = 1
    elif a == 'Careful':
        parameter = 2
    elif a == 'Traveler':
        parameter = 3
    elif a == 'Balanced':
        parameter = 4
    else:
        print ("Incorrect input")
        exit(1)

    '''Reads the databases and builds the Graph based on nodes distance'''
    G = nx.Graph()
    lines = file.read().splitlines()
    for line in range(len(lines)):
        n = list(lines[line].split(' '))
        m = []
        for word in n:
            m.append(word)
        G.add_node(str(m[0]),x= m[1],y= m[2],z= m[3],s =m[4])
    for line in range(len(lines)):
        n = list(lines[line].split(' '))
        m = []
        for word in n:
            m.append(word)
        for i in range(5, len(m)):
            coordinates1 = [float(m[1]), float(m[2])]
            coordinates2 = [float(G.nodes[str(m[i])]['x']),float(G.nodes[str(m[i])]['y'])]
            if G.has_edge(m[0], m[i]):
                continue
            else:
                G.add_edge(m[0], m[i], weight=geopy.distance.geodesic(coordinates1, coordinates2).km)

    '''Asks the user for starting and end point'''
    print('Where do you want to start?')
    start_node = input()
    if start_node not in G.nodes:
        print("Incorrect state")
        exit(1)
    print('Where do you want to go?')
    end_node = input()
    if end_node not in G.nodes:
        print("Incorrect input")
        exit(1)

    '''Dist function: distance between starting and end point, the results is modified according to
        user's need, used as heuristic h(n)'''
    def dist(a, b):
        (x1, y1) = [float(G.nodes[a]['x']), float(G.nodes[a]['y'])]
        (x2, y2) = [float(G.nodes[b]['x']), float(G.nodes[b]['y'])]
        d = (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
        if parameter == 1:
            d = d/1000
        elif parameter ==2:
            d = d/100
        elif parameter == 3:
            d = d/100
        elif parameter == 4:
            d = d
        return d

    '''Total function: sum of safety, height difference and distance between starting and neighbour points
       the results is modified according to user's need, used as weight g(n)'''
    def total (a,b,c):
        safety = int(G.nodes[a]['s']) + int(G.nodes[b]['s'])
        safety = safety /2
        height_diff = float(G.nodes[a]['z']) - float(G.nodes[b]['z'])
        height_diff = abs(height_diff)/20
        ab = [float(G.nodes[a]['x']), float(G.nodes[a]['y'])]
        cd = [float(G.nodes[b]['x']), float(G.nodes[b]['y'])]
        partial_distance = geopy.distance.geodesic(ab, cd).km
        if parameter == 1:
            totals = partial_distance + safety + 1000 * (1/height_diff)
        elif parameter ==2:
            totals = partial_distance*4 + safety*1000 + height_diff
        elif parameter == 3:
            totals = partial_distance*1000 + safety + height_diff
        elif parameter == 4:
            totals = partial_distance*4 + safety/2 + height_diff/2
        return totals

    '''Timecalc function: calculates the average time to walk or run a certain path depending
       on user's preference'''
    def timecalc(a,b):
        ab = [float(G.nodes[a]['x']), float(G.nodes[a]['y'])]
        cd = [float(G.nodes[b]['x']), float(G.nodes[b]['y'])]
        partial_distance = geopy.distance.geodesic(ab, cd).km
        speed = 0
        if parameter == 1:
            speed = 10
        elif parameter == 2:
            speed = 6
        elif parameter == 3:
            speed = 4
        elif parameter == 4:
            speed = 8
        return math.floor((partial_distance/speed)*60)

    '''Outputs the a star ideal path, the coordinates and the time to traverse paths'''
    print("Your ideal path is:")
    alfa = nx.astar_path(G, start_node, end_node, heuristic= dist, weight=total)
    print(alfa)
    print ("You found yourself at:",G.nodes[alfa[0]]['x'], G.nodes[alfa[0]]['y'])
    for i in range(1, len(alfa)):
        print ("Go to: ",G.nodes[alfa[i]]['x'], G.nodes[alfa[i]]['y'])
        print("It will take:", timecalc(alfa[i], alfa[i - 1]), "minutes")
    print ("Job Done!")

    '''Building the 2D picture to show graph and path'''
    color_map = []
    edge_colors = []
    for edge in G.edges:
        if edge [0] in alfa and edge [1] in alfa:
            edge_colors.append('red')
        else:
            edge_colors.append('black')
    for node in G:
        if node in alfa:
            color_map.append('red')
        else:
            color_map.append('yellow')
    dicta = {}
    for node in G.nodes:
        dicta.update({node: [float(G.nodes[node]['y']),float( G.nodes[node]['x'])]})
    my_pos = nx.spring_layout(G,pos = dicta,seed=0)
    nx.draw(G, with_labels=True,node_size = 400,font_size=7,node_color=color_map,edge_color=edge_colors, pos = my_pos)
    plt.savefig("Graph.png", format="PNG")
    plt.show()
    file.close()

    '''Building 3D Graph to show graph and path'''
    dataframe = pd.read_csv('nodes.txt', sep='\s+', header=None, usecols=[0,1, 2, 3])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(dataframe[1], dataframe[2], dataframe[3], cmap='viridis', edgecolor='none')
    x=[]
    y=[]
    z=[]
    for i in alfa:
        for index, line in dataframe.iterrows():
            if i==line[0]:
                x.append(line[1])
                y.append(line[2])
                z.append(line[3])
    for i in range(len(alfa) - 1):
        ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]], color='red',zorder=10)
    for i, city in enumerate(alfa):
        ax.text(x[i], y[i], z[i], alfa[i] , color='black')
    ax.set_box_aspect([5, 5, 2])
    plt.show()
if __name__ == "__main__":
    main()

