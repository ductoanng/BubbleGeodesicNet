#####################################################
#
# Algorithm Calculate the Fermat point of three points on plane
# 
####################################################
# About Fermat Point:
#
# Note that: Given a triangle ABC, the Fermat point F of triangle ABC is 
# the point that minimize the distance sum FA+FB+FC
#
# +) If there is no angle of triangle ABC > 120^o, then F is different from A,B,C
# +) If angle BAC>=120^o, then F=A 
#
#####################################################

import numpy as np

def cosAngle(A,B,C):
    vecAB =np.array([B[0]-A[0],B[1]-A[1]])
    vecAC =np.array([C[0]-A[0],C[1]-A[1]])

    normAB = np.linalg.norm(vecAB)
    normAC = np.linalg.norm(vecAC)
    cosA = np.dot(vecAB,vecAC)/(normAB*normAC)

    if cosA>1:
        cosA = 1.0
    if cosA<-1:
        cosA = -1.0

    return cosA

#Calculate distance between two points
def distance(A,B):
    vecAB =np.array([B[0]-A[0],B[1]-A[1]])
    return np.linalg.norm(vecAB)

#Return unit vector of the vector(AB) with points A and B 
def unitVector(A,B):
    vec = np.array([B[0]-A[0],B[1]-A[1]])
    norm = np.linalg.norm(vec)
    if norm<1e-15:
        return np.array([0,0])
    else:
        return vec/norm
    
#Check whether it is linear or not
def isLinear(A,B,C):
    totalVec = unitVector(A,B)+unitVector(A,C)
    diffVec = unitVector(A,B)-unitVector(A,C)

    #Case 1: Vectors AB and AC are opposite
    if np.linalg.norm(totalVec)<1e-15:
        return -1
    
    #Case 2: Vectors AB and AC are in same direction
    if np.linalg.norm(diffVec)<1e-15:
        return 1
    
    #Case 3: A,B,C are not linear
    return 0

#Calculate the coordinate of the Fermat point of three point A,B,C
def Fermat(A,B,C):
    #Check whether they are on the same line
    if isLinear(A,B,C) == -1:
        return A
    if isLinear(B,A,C) == -1:
        return B
    if isLinear(C,A,B) == -1:
        return C

    cosA = cosAngle(A,C,B)
    cosB = cosAngle(B,C,A)
    cosC = cosAngle(C,A,B)

    #First case: There is an angle >2/3pi
    if np.arccos(cosA) >= (2/3)*np.pi:
        return A
    if np.arccos(cosB) >= (2/3)*np.pi:
        return B
    if np.arccos(cosC) >= (2/3)*np.pi:
        return C

    #Second case
    a = distance(B,C)
    b = distance(A,C)
    c = distance(B,A)
    s = (a+b+c)/2

    pointA = np.array([A[0],A[1]])
    pointB = np.array([B[0],B[1]])
    pointC = np.array([C[0],C[1]])
    
    #(x0:y0:z0) is the barycentric coordinate of F
    S_A = b*c*cosA
    S_B = a*c*cosB
    S_C = a*b*cosC

    S = 2*np.sqrt(s*(s-a)*(s-b)*(s-c)) #S = 2*area(ABC)

    x0 = 1/(np.sqrt(3)*S_A+S)
    y0 = 1/(np.sqrt(3)*S_B+S)
    z0 = 1/(np.sqrt(3)*S_C+S)

    #formular of Fermat point (Introduction to the Geometry of the Triangle - Paul Yiu)
    pointF = (x0*pointA+y0*pointB+z0*pointC)/(x0+y0+z0)
    # F = point(pointF[0],pointF[1])

    return pointF



