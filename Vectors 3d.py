import os
import math

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

class Vector:
    #This class defines 3d vectors
    #Can only do one opperation at a time
    def __init__(self,starting_vector):
        self.position = starting_vector

    def __add__(self,OtherVector):
        try:
            [X,Y,Z] = self.position
            [X2,Y2,Z2] = OtherVector
            position = [X+X2,Y+Y2,Z+Z2]
        except TypeError: #Subtraction of two vector objects
            [X,Y,Z] = self.position
            [X2,Y2,Z2] = OtherVector.position
            position = [X+X2,Y+Y2,Z+Z2]
        return Vector(position)

    def __sub__(self,OtherVector):
        try:
            [X,Y,Z] = self.position
            [X2,Y2,Z2] = OtherVector
            position = [X-X2,Y-Y2,Z-Z2]
        except TypeError: #Subtraction of two vector objects
            [X,Y,Z] = self.position
            [X2,Y2,Z2] = OtherVector.position
            position = [X-X2,Y-Y2,Z-Z2]
        return Vector(position)

    def __mul__(self,scalor):
        [X,Y,Z] = self.position
        position = [float(X)*scalor,float(Y)*scalor,float(Z)*scalor]
        return Vector(position)

    def magnitude(self):
        [X,Y,Z] = self.position
        return (X**2+Y**2+Z**2)**0.5

    def unit_vector(self):
        magnitude = self.magnitude()
        [X,Y,Z] = self.position
        return Vector([float(X)/magnitude,float(Y)/magnitude,float(Z)/magnitude])

    def dotP_angle(self,OtherVector):
        [X,Y,Z] = self.position
        [X2,Y2,Z2] = OtherVector.position
        dotP = X*X2 + Y*Y2 + Z*Z2
        cos_angle = dotP / (self.magnitude() * OtherVector.magnitude())
        angle = math.acos(cos_angle)
        return math.degrees(angle)

class Object:
    def __init__(self,position,velocity, mass, radius):
        self.position = Vector(position) #The objects position is a vector (metres/second)
        self.velocity = Vector(velocity) #The objects velocity is a vector (metres/second
        self.mass = mass                 #Given in kilograms
        self.radius = radius             #Given in metres

    def gravitational_acceleration(self,heavenly_body):
        G = 6.673e-11 #Gravitational constant
        m1 = heavenly_body.mass
        vector_distance = heavenly_body.position - self.position #Calculated the vector Object -> Heavenly body (ie moon to Earth)
        r = vector_distance.magnitude()
        magnitude = G*m1/(r**2)
        return vector_distance.unit_vector() * magnitude

    def calculate_1_step(self,acceleration):
        #assumed that acceleration already calculated
        step = 60*60*6#seconds -> A lower number is a lot better to use
        final_velocity = self.velocity + acceleration * step # v = u + at
        self.position = self.position + final_velocity * step #x(n+1) = x + vt
        self.velocity = final_velocity

        return self.position
           

Earth = Object([0,0,0],[0,-5,5],5.972e24,6.367e6)

Moon = Object([3.844e8,0,0],[0,1018.320462,0],7.346e22,1.173e8) #moon true velocity ->around earth 1018.320462

moon_on_earth = Moon.gravitational_acceleration(Earth)


Xm = []
Ym = []
Zm = []

Xe = []
Ye = []
Ze = []

for i in range(1,50*6):
    moon_on_earth = Moon.gravitational_acceleration(Earth)
    earth_on_moon = Earth.gravitational_acceleration(Moon)
    #print "after %s step the moon has moved to this position with that velocity" % i
    #print Moon.velocity.position
    #print "Distance from moon to earth ",Moon.position.magnitude()
    [xm,ym,zm] = Moon.calculate_1_step(moon_on_earth).position
    [xe,ye,ze] = Earth.calculate_1_step(earth_on_moon).position

    Xm.append(xm), Ym.append(ym), Zm.append(zm)
    Xe.append(xe), Ye.append(ye), Ze.append(ze)

ax.scatter(Xm,Ym,Zm, c = 'r', marker='o')
ax.scatter(Xe,Ye,Ze, c = 'g', marker='o')
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')

plt.show()

os.system('pause')
