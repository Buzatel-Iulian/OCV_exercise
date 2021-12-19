import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from model_load import read_off, shade

#import math

pygame.init()
display = (400, 300)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

sphere = gluNewQuadric() 

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# init mouse movement and center mouse on screen
displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
run = True
clock = pygame.time.Clock()
j=0
scale = 0.5
model = read_off( "Appendix_C/LowPolyMask.off" )

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
				run = False
			if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
				paused = not paused
				pygame.mouse.set_pos(displayCenter)
		if not paused: 
			if event.type == pygame.MOUSEMOTION:
				mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
			pygame.mouse.set_pos(displayCenter)
	if not paused:
		# get keys
		keypress = pygame.key.get_pressed()
		#mouseMove = pygame.mouse.get_rel()
		
		# init model view matrix
		glLoadIdentity()

		# apply the look up and down
		up_down_angle += mouseMove[1]*0.1
		glRotatef(up_down_angle, 1.0, 0.0, 0.0)

		# init the view matrix
		glPushMatrix()
		glLoadIdentity()

		# apply the movment 
		if keypress[pygame.K_w]:
			glTranslatef(0,0,0.1)
		if keypress[pygame.K_s]:
			glTranslatef(0,0,-0.1)
		if keypress[pygame.K_d]:
			glTranslatef(-0.1,0,0)
		if keypress[pygame.K_a]:
			glTranslatef(0.1,0,0)

		# apply the left and right rotation
		glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

		#degrees_per_second = 360./5.
		#degrees_per_millisecond = degrees_per_second / 1000.
		#milliseconds = clock.tick()
		#degrees = degrees_per_millisecond * milliseconds
		#glRotatef(degrees, 1,1,1)


		# multiply the current matrix by the get the new view matrix and store the final vie matrix 
		glMultMatrixf(viewMatrix)
		viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

		# apply view matrix
		glPopMatrix()
		glMultMatrixf(viewMatrix)

		glLightfv(GL_LIGHT0, GL_POSITION, [100, -100, 100, 0])

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glPushMatrix()

		glColor4f(0.2, 0.2, 0.2, 1)
		glBegin(GL_QUADS)
		glVertex3f(-10, -10, -2)
		glVertex3f(10, -10, -2)
		glVertex3f(10, 10, -2)
		glVertex3f(-10, 10, -2)
		glEnd()

		glRotate(j,0,0,1)
		j = (j + 1) % 360

		glTranslatef(-1.5, 0, 0)
		color = (0.5, 0.5, 0.2, 1)
		lum = 0.2
		#glColor4f(0.5, 0.5, 0.2, 1)
		#glColor4f(color[0]*lum, color[1]*lum, color[2]*lum, color[3]*lum)
		glBegin(GL_TRIANGLES)
		for i in range(model["face_count"]):
			#glBegin(GL_TRIANGLES)
			face = [
				(model["vertexes"][model["faces"][i]["v1"]]["x"]*scale, model["vertexes"][model["faces"][i]["v1"]]["y"]*scale, model["vertexes"][model["faces"][i]["v1"]]["z"]*scale),
				(model["vertexes"][model["faces"][i]["v2"]]["x"]*scale, model["vertexes"][model["faces"][i]["v2"]]["y"]*scale, model["vertexes"][model["faces"][i]["v2"]]["z"]*scale),
				(model["vertexes"][model["faces"][i]["v3"]]["x"]*scale, model["vertexes"][model["faces"][i]["v3"]]["y"]*scale, model["vertexes"][model["faces"][i]["v3"]]["z"]*scale)]
			lum = shade(face)
			glColor4f(color[0]*lum, color[1]*lum, color[2]*lum, color[3]*lum)
			for v in face:
				glVertex3fv(v)
			#glVertex3f(model["vertexes"][model["faces"][i]["v1"]]["x"]*scale, model["vertexes"][model["faces"][i]["v1"]]["y"]*scale, model["vertexes"][model["faces"][i]["v1"]]["z"]*scale)
			#glVertex3f(model["vertexes"][model["faces"][i]["v2"]]["x"]*scale, model["vertexes"][model["faces"][i]["v2"]]["y"]*scale, model["vertexes"][model["faces"][i]["v2"]]["z"]*scale)
			#glVertex3f(model["vertexes"][model["faces"][i]["v3"]]["x"]*scale, model["vertexes"][model["faces"][i]["v3"]]["y"]*scale, model["vertexes"][model["faces"][i]["v3"]]["z"]*scale)
		glEnd()
		print(face)

		glTranslatef(-10.5, 0, 0)
		glColor4f(0.5, 0.2, 0.2, 1)
		gluSphere(sphere, 1.0, 32, 16)

		glTranslatef(13, 0, 0)
		glColor4f(0.2, 0.2, 0.5, 1)
		gluSphere(sphere, 1.0, 32, 16)

		glPopMatrix()

		pygame.display.flip()
		pygame.time.wait(10)
pygame.quit()
