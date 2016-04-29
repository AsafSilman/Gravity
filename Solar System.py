import pygame
import math

#This is a basic program that simulates the first 3 planets and the earth moon system.
#In addition to a large asteroid
#The calculations used in this program are physically accurate
#Asaf Silman 2016

#Initial Values
background_colour = (0,0,0)
(width,height) = (1000,1000)
clock = pygame.time.Clock()
simulation_time = 60*30 #second
G = 6.67e-11

au = 400 #pixels

#Start window
screen = pygame.display.set_mode((width,height))
screen.fill(background_colour)

#Name
pygame.display.set_caption("Gravity simulation")

#Vector addition
def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def collision(particle1,particle2):
	dx = particle1.x - particle2.x
	dy = particle1.y - particle2.y

	dist = math.hypot(dx, dy) * 1.496e8 

	return dist < (particle1.size + particle2.size)*1e5

def distance(particle1,particle2):
	dx = (particle1.x - particle2.x) * 1.496e11 / au
	dy = (-particle1.y + particle2.x) * 1.496e11 / au
	return math.hypot(dx, dy)

#Start code (class structure)
class particle(object):
	def __init__(self,(x,y),(angle,r),size,mass,colour = (0,0,225),thickness = 0,parent = screen):
		self.x = x
		self.y = y
		self.size = size
		self.mass = mass
		self.colour = colour
		self.parent = parent
		self.thickness = thickness
		self.speed = r
		self.angle = math.radians(angle)

	def draw(self):
		pygame.draw.circle(self.parent,self.colour,(int(self.x),int(self.y)),self.size,self.thickness)

	def move(self):
		self.x += (math.sin(self.angle) * self.speed) / (1.496e11 ) * au * simulation_time
		self.y -= (math.cos(self.angle) * self.speed) / (1.496e11 ) * au * simulation_time
	
	def gravity_attraction(self,OtherParticle):
		dx = (OtherParticle.x - self.x) * 1.496e11 / au
		dy = (-OtherParticle.y + self.y) * 1.496e11 / au

		angle = 0.5 * math.pi - math.atan2(dy, dx)
		distance = math.hypot(dx, dy)

		acceleration = (G * OtherParticle.mass) / distance**2 
		return (angle,acceleration)


#Running code
centre = (width/2,height/2)

list_of_particles = []


Sun = particle(centre,(0, 0),5,1.99e30,(255,255,0)) #particvle
Earth = particle((width/2-400,height/2),(0, 29805),0, 5.972e24, (0,100,255)) #e24
#Earth = particle((width/2,height/2),(0, 0),5, 5.972e24, (255,255,255)) #e24

Venus = particle((width/2-280.8,height/2),(0, 3.5e4),1,4.867e24, (145,135,145))
Mercury = particle((width/2-155,height/2),(0, 4.7e4),0,3.28e23, (255,102,0))
Mars = particle((width/2,height/2+480),(270, 2.41e4),2,6.39e22, (255,102,0))
Moon = particle((width/2-401.24,height/2),(0,29805+1018.320462),0,7.3476e22,(255,255,255))
Comet = particle((width/2-100,height/2+20),(20,29805*2.5),2,7.3476e5,(255,255,255))
#Moon = particle((width/2-401,height/2),(0,1018.320462),1,7.3476e22,(255,0,0))

list_of_particles.append(Sun)
list_of_particles.append(Earth)
list_of_particles.append(Venus)
list_of_particles.append(Mercury)
#list_of_particles.append(Mars)
list_of_particles.append(Moon)
list_of_particles.append(Comet)

for particle in list_of_particles:
	x = (0,0)
	for p in list_of_particles:
		if particle == p:
			continue
		x = addVectors(x,particle.gravity_attraction(p))


#Running loop
running = True
clear = True
count =0
while running:
	clock.tick(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			clear = False #Trace/no trace
		if event.type == pygame.KEYUP:
			clear = True #Trace/no trace

	if clear == False:
		screen.fill(background_colour)

	for particle in list_of_particles:
		particle.draw()

		x = (0,0)

		for p in list_of_particles:
			#if it's itself
			if particle == p:
				continue
			#if it collides with another particle
			if collision(particle,p):
				print 'collision'
				if particle.mass > p.mass:
					particle.mass += p.mass
					particle.size += p.size
					list_of_particles.remove(p)
				else:
					p.mass += particle.mass
					p.size += particle.size
					list_of_particles.remove(particle)

			x = addVectors(x,particle.gravity_attraction(p))
		(a1,r1) = x
		rf = r1 * simulation_time

		(particle.angle,particle.speed) = addVectors((a1,rf),(particle.angle,particle.speed))
		particle.move()

	pygame.display.flip()
