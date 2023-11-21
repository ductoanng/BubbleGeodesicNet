import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from numpy import random
from FertmatPoint import *
import itertools

class Point:
    def __init__(self,position):
        self.id = None
        self.isBalanced = False   #the point is balanced or not
        self.x = None
        self.y = None
        self.position = position
        self.neighborlist = []

    def __str__(self):
        st = "["+str(np.round(self.position[0],2))+","+str(np.round(self.position[1],2))+"]"
        st=""
        if self.isBalanced:
            return st+"(B)"
        else:
            return st+"(U)"
    
    def modify(self,changeVector, rate=1):
        if not self.isFix:
            self.position = self.position + rate*changeVector

    def getPosition(self):
        return self.position
    
    def getNeighborlist(self):
        return self.neighborlist
    
    def setPosition(self, newposition):
        self.position = newposition

def distance(posA,posB):
    diffVec = posB-posA
    return np.sqrt(diffVec[0]*diffVec[0]+diffVec[1]*diffVec[1])

def normalizeVector(vec):
    return 1/lenVec(vec)*vec

def lenVec(vec):
    return np.sqrt(vec[0]*vec[0]+vec[1]*vec[1])

def angle(nodeA,nodeB,nodeC):
    vecAB = nodeB.position-nodeA.position
    vecAC = nodeC.position-nodeA.position

    dot_product = vecAB[0]*vecAC[0]+vecAB[1]*vecAC[1]
    cosine_angle = dot_product / (lenVec(vecAB) * lenVec(vecAC))
    if cosine_angle>1:
        cosine_angle = 1.0
    if cosine_angle<-1:
        cosine_angle = -1.0

    angle_radians = np.arccos(cosine_angle)
    return angle_radians


def islessthan120(nodeA,nodeB,nodeC):
    return 2/3*np.pi-angle(nodeA,nodeB,nodeC)>10**(-8)

if __name__ == '__main__':

    # Initialize node positions
    A = Point(np.array([1.0,0.0]))
    B = Point(np.array([2.0,0.0]))
    C = Point(np.array([0.6925275235382, 0.9504814392206]))
    D = Point(np.array([1.4985395878209, 1.5386524050485]))
    E = Point(np.array([2.311813022052, 0.9504814392206]))

    
    A1 = Point(np.array([0.0,0.0]))
    A2 = Point(np.array([1.0,0.0]))
    A3 = Point(np.array([0.0,0.1])) 
    A4 = Point(np.array([1.0,1.0])) 
    listUnbalancedPoint = [A1,A2,A3,A4]

    # Initialize by input
    # listUnbalancedPoint = []
    # while (True):
    #     node = input("Enter node (or 'done' to finish): ")
    #     if node.lower() == 'done':
    #         break
    #     else:
    #         try:
    #             x = float(input("Enter x-coordinate for node {}: ".format(node)))
    #             y = float(input("Enter y-coordinate for node {}: ".format(node)))
    #             point = Point(np.array([x, y]))
    #             listUnbalancedPoint.append(point)
    #         except ValueError:
    #             print("Invalid input. Please enter valid coordinates.")

    # posUnbalanced = {node:node.position for node in listUnbalancedPoint}

    # Intialize randomly
    # listUnbalancedPoint=[]
    # numberofpoint = 50
    # for i in range(numberofpoint):
    #     x = random.uniform(0, 20)  # Adjust the range as needed
    #     y = random.uniform(0, 20)  # Adjust the range as needed
    #     point = Point(np.array([x, y]))
    #     listUnbalancedPoint.append(point)

    listBalancedPoint = []

    # Create a fully connected graph with listpoint
    G = nx.complete_graph(listUnbalancedPoint)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal', adjustable='box')
    pos = {node:node.position for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=10)
    plt.title("Fully Connected Graph")
    plt.pause(3)
    plt.close()

    # Add weighted edges based on Euclidean distance
    for edge in G.edges():
        node1, node2 = edge
        dist = distance(node1.position,node2.position)
        G[edge[0]][edge[1]]['weight'] = dist

    # Find the minimum spanning tree (MST)
    mst = nx.minimum_spanning_tree(G)    
    # mst.add_edge(A3,A4, weight=distance(A3.position,A4.position))
    # mst.add_edge(A1,A4, weight=distance(A1.position,A4.position))
    # Draw the MST
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal', adjustable='box')
    pos = {node:node.position for node in mst.nodes()}
    nx.draw(mst, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=10)
    plt.title("Minimum-Spanning-Tree")
    plt.pause(3)

    # Check all triples of connected nodes for acute angles
    triples_less_120 = dict()
    for node in mst.nodes():
        if not node.isBalanced:
            triples_less_120 ={**triples_less_120, **{(node, n2, n3) : angle(node, n2, n3) for n2, n3 in itertools.combinations(mst.neighbors(node),2)
                            if islessthan120(node, n2, n3)}}
        
    # Create a dictionary of (n1,n2,n3) with its angle 
    # Sort items by value
    sorted_items = sorted(triples_less_120.items(), key=lambda x: x[1])
    
    numberOfIter = 10
    movingRate = 0.1
    numberOfIterBal = 200
    epsilon = 1e-3

    for i in range(numberOfIter):

        # Find the angle root at unbalanced points that <120
        triples_less_120 = dict()
        for node in mst.nodes():
            if not node.isBalanced:
                triples_less_120 ={**triples_less_120, **{(node, n2, n3) : angle(node, n2, n3) for n2, n3 in itertools.combinations(mst.neighbors(node),2)
                                if islessthan120(node, n2, n3)}}
        
        if not triples_less_120:
            # End the algorithm, the graph is stable
            print("All the angles at unbalanced points are >=120")
            break
        
        sorted_items = sorted(triples_less_120.items(), key=lambda x: x[1])
        node1,node2,node3 = sorted_items[0][0]
        #print("the sorted angle: node1 = ",node1.position,", node2 = ",node2.position," node3 = ",node3.position)
        #print("The angle = ",sorted_items[0][1])

        # Find the Fermat point of node1, node2, node3
        Fermatpos = Fermat(node1.position,node2.position,node3.position)  
        FermatPoint = Point(Fermatpos)
        FermatPoint.isBalanced=True

        # Add the Fermat Point to the graph
        mst.add_node(FermatPoint)

        # Connect node1, node2, node3 to Fermat Point
        mst.add_edge(FermatPoint,node1, weight=distance(FermatPoint.position,node1.position))
        mst.add_edge(FermatPoint,node2, weight=distance(FermatPoint.position,node2.position))
        mst.add_edge(FermatPoint,node3, weight=distance(FermatPoint.position,node3.position))

        # Remove edge (node1,node2) and (node1,node3)
        mst.remove_edge(*(node1,node2))
        mst.remove_edge(*(node1,node3))

        #print("Fermat point pos = ", FermatPoint.position)

        # Add Fermat point to balancedPoint list
        listBalancedPoint.append(FermatPoint)
        #print("list balanced = ",listBalancedPoint)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_aspect('equal', adjustable='box')
        pos = {node:node.position for node in mst.nodes()}
        nx.draw(mst, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=10)
        plt.title("Add a new Fertmat Point")
        plt.pause(3)
        plt.close()

        j=1
        balanceMeasure = 99999999
        while (j<numberOfIterBal and balanceMeasure>epsilon):
            #print('inner iter = ',j)
            # Balance the new balancedPoint list
            balanceMeasure=0
            for node in listBalancedPoint:
                #print("balance node = ",node.position)
                vecChange = np.array([0.0,0.0])

                # smallest distance
                minDist = 99999999

                # Calculate the sum of all unit tangent vectors to all neighbors
                for u in mst.neighbors(node):
                    vecChange += normalizeVector(u.position-node.position)
                    dist = distance(u.position,node.position)
                    if dist < minDist:
                        minDist = dist
                    
                balanceMeasure += lenVec(vecChange)
                print("vecChange = ",vecChange)
                print("balanceMeasure = ",balanceMeasure)
                node.position = node.position+movingRate*minDist*vecChange

            balanceMeasure = balanceMeasure/len(listBalancedPoint)
            

            fig, ax = plt.subplots(figsize=(10, 8))
            ax.set_aspect('equal', adjustable='box')
            pos = {node:node.position for node in mst.nodes()}
            nx.draw(mst, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=10)
            plt.title("Balancing iter "+str(j))
            plt.pause(0.1)
            plt.close()

            j=j+1
            

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    pos = {node:node.position for node in mst.nodes()}
    #posBal = {node : node.position for node in listBalancedPoint}
    nx.draw(mst, pos, with_labels=False, node_size=50, node_color='skyblue', font_size=10)
    plt.title("Final Result")
    plt.show()
    

    


    
