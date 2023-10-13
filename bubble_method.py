#####################################################
#
# Goal: Construct a geodesic net of a set of unbalanced point
# inspired from the bubbles corruption
#
# Geodesic net reference: https://doi.org/10.1080/10586458.2020.1743216 
# 
####################################################


import numpy as np
import matplotlib.pyplot as plt
from numpy import random
from FertmatPoint import *

class BubblePoint:
    def __init__(self,order,n):
        self.order = order
        self.boundary = False   #Is boundary (unbalanced)
        self.x = order // n
        self.y = order % n
        self.position = np.array([self.x,self.y])
        self.neighborlist = []

        #Initialize the coordinate of a point based on order
        if order % n != 0:
            self.neighborlist.append(order-1)
        else:
            self.boundary = True
        if order % n !=(n-1):
            self.neighborlist.append(order+1)
        else:
            self.boundary = True
        if order > n-1:
            self.neighborlist.append(order-n)
        else:
            self.boundary = True
        if order < n*n-n:
            self.neighborlist.append(order+n)
        else:
            self.boundary = True

        #Is fix? 
        self.isFix = False

    def changeFix(self,isfix):
        self.isFix = isfix
    
    def modify(self,changeVector, rate=1):
        if not self.isFix:
            self.position = self.position + rate*changeVector

    def getPosition(self):
        return self.position
    
    def getNeighborlist(self):
        return self.neighborlist
    
    def setPosition(self, newposition):
        self.position = newposition

def distance(A,B):
    diff = B-A
    return np.sqrt(diff[0]*diff[0]+diff[1]*diff[1])

def normalizeVector(vec):
    length = distance(vec,np.array([0,0]))
    return 1/length*vec

#Plotting functions

#Plot Bubble Points
def plotList(list,st,size):
    listX=[]
    listY=[]
    for I in list:
        listX = np.append(listX,I.getPosition()[0])
        listY = np.append(listY,I.getPosition()[1])
    plt.plot(listX,listY,st,markersize=size)
    for i in range(len(list)):
        itext = str(i)
        plt.text(listX[i],listY[i], itext)

#Plot Unbalanced Point
def plotUnbalancedPoint(list,str,size):
    listX=[]
    listY=[]
    for I in list:
        listX = np.append(listX,I[0])
        listY = np.append(listY,I[1])
    plt.plot(listX,listY,str,markersize=size)

#Plot segment (edge) connecting points
def plotSegment(A,B):
    x_values = [A[0], B[0]]
    y_values = [A[1], B[1]]
    plt.plot(x_values, y_values, 'b', linestyle="-", linewidth=1.0)


########################################
##########        MAIN      ############
########################################

if __name__ == '__main__':
    
    # Hyperparameters:
    changeMargin = 0
    learningrate_0 = 0.1   
    Number_of_Iteration = 100
    unbalanceRate = 0.2
    n=10  #Size of the square grid (nxn)
    
    listBubblePoint = []
   
    for i in range(n*n):
        point = BubblePoint(i,n)
        # print("Point with order ",i)
        # print(point.position)
        # print("Neighborlist: ")
        # print(point.neighborlist)
        listBubblePoint.append(point)

    ## INPUT unbalanced (boundary) points:
    A = np.array((0.00001,0.00001))
    B = np.array((0.00001,n-2+0.00001))
    C = np.array((n-2+0.000001,n-3+0.000001))
    D = np.array((n-2+0.0000001,3+0.0000001))
    # G = np.array((n/2+0.5+0.0000001,n/2-0.5+0.0000001))
    # E = np.array((n-1+0.000001,n-2+0.0001))
    # F = np.array((n-2+0.00001,n-1.5+0.0001))
    listUnbalancePoint = [A,B,C]

    #Take Fermat point of A,B,C
    FermatPoint = Fermat(A,B,C)
    print(FermatPoint)
    

    for u in listUnbalancePoint:
        distList = np.array([])
        #print('disList = ',distList)
        for p in listBubblePoint:
            d = 1000000
            if not p.isFix:
                d = distance(u,p.position)
            distList = np.append(distList,d)
            #print('distList = ',distList)
        
        index = np.argmin(distList)
        #print('Bubble point: ',listBubblePoint[index].position)
        #print('Close to unbalance point ',u)
        listBubblePoint[index].changeFix(True)
        listBubblePoint[index].setPosition(u)

    for p in listBubblePoint:
        if not p.isFix:
            a = random.rand()*2-1
            b = random.rand()*2-1
            p.modify(np.array((a,b)),changeMargin)


    for i in range(Number_of_Iteration):
        
        listchangeVector = []

        #For each bubble point p, calculate the changing vector
        for p in listBubblePoint:
            changeVector = np.array([0,0])
            for q in p.neighborlist:
                if listBubblePoint[q].isFix:
                    changeVector = changeVector + unbalanceRate*(-p.position + listBubblePoint[q].position)
                else:
                    changeVector = changeVector + (-p.position + listBubblePoint[q].position)
            listchangeVector.append(changeVector)

        # Modifying learning rate:
        if i<100:
            learningrate = 0.2
        else:
            if i<115:
                learningrate = 1.5
            else:
                learningrate = 0.2

        # Modifying positions of all balanced points
        j = 0
        while j<len(listBubblePoint):
            p = listBubblePoint[j]
            p.modify(listchangeVector[j],learningrate)
            j = j+1
    
        #Plotting
        plt.clf()

        for p in listBubblePoint:
            for q in p.neighborlist:
                plotSegment(p.position,listBubblePoint[q].position)

        plotList(listBubblePoint,'go',4)
        plotUnbalancedPoint(listUnbalancePoint,'rx',10)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        title = "Iteration "+str(i+1)
        plt.plot(FermatPoint[0],FermatPoint[1],'C1o',10)
        plt.title(title)
        plt.pause(0.1)
        
    plt.show()