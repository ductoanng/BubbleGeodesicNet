import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import random
from FertmatPoint import *
import itertools
from IPython.display import HTML

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


A1 = Point(np.array([0.0, 0.0]))
A2 = Point(np.array([1.0, 0.0]))
A3 = Point(np.array([0.0, 0.1]))
A4 = Point(np.array([1.0, 1.0]))
listUnbalancedPoint = [A1, A2, A3, A4]

listBalancedPoint = []

# fig, ax = plt.subplots(figsize=(10, 8))
# ax.set_aspect('equal')

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect('equal', adjustable='box')

count = 0
G = nx.complete_graph(listUnbalancedPoint)
mst = nx.minimum_spanning_tree(G)

def update(frame):
    ax.clear()  # Clear the previous plot
    global count
    global G
    global mst
    print(count)

    if count == 0:
        # Draw the Fully Connected Graph
        # Create a fully connected graph with listpoint

        # Draw the Fully Connected Graph
        pos = {node: node.position for node in G.nodes()}
        nx.draw(G, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=10)
        plt.title("Fully Connected Graph "+str(count))
        #plt.show()
        plt.pause(3)
        count = count+1
        return

    elif count == 1:
        # Draw the MST
        # Add weighted edges based on Euclidean distance
        G = nx.complete_graph(listUnbalancedPoint)
        for edge in G.edges():
            node1, node2 = edge
            dist = distance(node1.position, node2.position)
            G[edge[0]][edge[1]]['weight'] = dist

        # Find the minimum spanning tree (MST)
        mst = nx.minimum_spanning_tree(G)

        # Draw the MST
        pos = {node: node.position for node in mst.nodes()}
        nx.draw(mst, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=10)
        plt.title("Minimum-Spanning-Tree "+str(count))
        plt.pause(3)
        count = count+1
        return
        
        #plt.show()
    elif count == 2:
        # Draw the Final Result
        pos = {node: node.position for node in mst.nodes()}
        # posBal = {node : node.position for node in listBalancedPoint}
        node_colors = ['skyblue' if node not in listBalancedPoint else 'red' for node in mst.nodes()]
        nx.draw(mst, pos, with_labels=False, node_size=50, node_color=node_colors, font_size=10)
        plt.title("Final Result "+str(count))
        plt.pause(3)
        count=0
        return
        #plt.show()
    
    # Title for each frame
    #plt.title(f"Frame {frame}")
   

# Set the number of frames (iterations)
num_frames = 3 # Change this to the desired number of frames (3 for your three figures)

# Create the FuncAnimation object
animation = FuncAnimation(fig, update, frames=num_frames, interval=2000, repeat=True)

# Display the animation
# plt.show()
plt.show()
