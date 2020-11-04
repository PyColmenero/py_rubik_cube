import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import random as rd
import math


vertices = 	[
	[ 0.5, 	-0.5,	-0.5],
	[ 0.5, 	 0.5,	-0.5],
	[-0.5, 	 0.5,	-0.5],
	[-0.5,	-0.5,	-0.5],
	[ 0.5,	-0.5,	0.5],
	[ 0.5, 	 0.5,	0.5],
	[-0.5,	-0.5,	0.5],
	[-0.5,	 0.5,	0.5]
			]

vert_axis = (
	(-10,   0,   0),
	( 10,   0,   0),
	(  0, -10,   0),
	(  0,  10,   0),
	(  0,   0, -10),
	(  0,   0,  10)
			)

#LINES DOTS
edges = (
	(0,1),
	(0,3),
	(0,4),
	(2,1),
	(2,3),
	(2,7),
	(6,3),
	(6,4),
	(6,7),
	(5,1),
	(5,4),
	(5,7)
	)

#SURFACES DOTS
surfaces = (
	(0, 1, 2, 3),
	(3, 2, 7, 6),
	(6, 7, 5, 4),
	(4, 5, 1, 0),
	(1, 5, 7, 2),
	(4, 0, 3, 6),
	)

#AXIS DOTS
edges_axis = (
	(2,3),
	(3,2)
			)

cube_size = 6
matrix_cubes_len = (cube_size*cube_size*cube_size)-((cube_size-2)*(cube_size-2)*(cube_size-2))
boxes = 			np.zeros((matrix_cubes_len), dtype='object')	#5 = 97 4 = 55 #3 = 26

resto = (cube_size-1)/2

boolSelection = True
boolReor = False


def runCube():

	def draw_cube(x,y,z, cr, cl, cu, cd, cb, cf, selected, lift_list_asign):
		#SURFACES DRAWING ==============================================================================
		glTranslatef(x,y,z)
		glBegin(GL_QUADS)
		
		colorS = 0.2
		color_list = [0,0,0,0,0,0]

		if selected: 	color_list = 	[(0,0,1-colorS), 	(1-colorS,0.65-colorS,0),	(0,0.7-colorS,0),	(1-colorS,0,0), 	(1-colorS,1-colorS,1-colorS),	(1-colorS,1-colorS,0),]
		else: 			color_list = 	[(0,0,1), 			(1, 	0.65, 0), 			(0,0.7,0),			(1,0,0), 			(1,1,1), 						(1,1,0)]
										#BLUE 				#ORANGE						#GREEN				#RED				#WHITE							#YELLOW
		myColors = [cr, cl, cu, cd, cb, cf]

		index_current_surface = 0
		#if selected:
		for edge in surfaces:	
			#COLOR OF EACH SURFACE
			glColor3fv(color_list[myColors[index_current_surface]])
			is_drawn = False

			if (index_current_surface == 0 and z == lift_list_asign[0]):
				is_drawn = True
			if (index_current_surface == 1 and x == lift_list_asign[0]):
				is_drawn = True
			if (index_current_surface == 2 and z == lift_list_asign[cube_size-1]):
				is_drawn = True
			if (index_current_surface == 3 and x == lift_list_asign[cube_size-1]):
				is_drawn = True
			if (index_current_surface == 4 and y == lift_list_asign[cube_size-1]):
				is_drawn = True
			if (index_current_surface == 5 and y == lift_list_asign[0]):
				is_drawn = True

			if selected: is_drawn = True

			if is_drawn:
				glVertex3fv(vertices[edge[0]])
				glVertex3fv(vertices[edge[1]])
				glVertex3fv(vertices[edge[2]])
				glVertex3fv(vertices[edge[3]])


			index_current_surface+=1

		glEnd()

		#EDGES DRAWING =========================================================================
		glLineWidth(2);
		glBegin(GL_LINES)
		colorSelOut = 0.9
		if not selected:	glColor3fv((0,0,0))
		else: 				glColor3fv((colorSelOut,colorSelOut,colorSelOut))

		for edge in edges:
			for vertex in edge:
				glVertex3fv(vertices[vertex])

		glEnd()

		glTranslatef(-x,-y,-z)


	def draw_Axis():
		glLineWidth(3);
		glBegin(GL_LINES)
		glColor3fv((1,1,1))

		for edge in edges_axis:
			for vertex in edge:
				glVertex3fv(vert_axis[vertex])
		glEnd()

	def draw_Core(lift_list_asign):
		glBegin(GL_QUADS)
		glColor3fv((0,0,0))
		index_core = 0

		mult_by = (cube_size) -2

		for edge in surfaces:	
			for vertex in edge:
				
				x,y,z = vertices[vertex][0], vertices[vertex][1], vertices[vertex][2] 
				x,y,z = x*mult_by,y*mult_by,z*mult_by
				glVertex3fv((x,y,z))

				index_core+= 1
		glEnd()


	def change_position(selectedAxis, selectedDir):
		#selectedAxis indica el "x,y,x" que no toca

		indexS = 0
		selected_list_coord = 	[]

		for cBox in boxes:
			x,y = 0,0

			if selectedAxis == 0: x, y, z = cBox.y, cBox.z, cBox.x
			if selectedAxis == 1: x, y, z = cBox.x, cBox.z, cBox.y
			if selectedAxis == 2: x, y, z = cBox.x, cBox.y, cBox.z

			if not (x == 0 and y == 0 and z == 0):
				if cBox.isSelected:
					if selectedAxis == 0: 		
						x, y = cBox.y, cBox.z
						if selectedDir == 0:  	cBox.cr, cBox.cu, cBox.cb, cBox.cf = cBox.cf, cBox.cb, cBox.cr, cBox.cu; #print(0)
						else:					cBox.cr, cBox.cu, cBox.cb, cBox.cf = cBox.cb, cBox.cf, cBox.cu, cBox.cr; #print(1)
					if selectedAxis == 1: 		
						x, y = cBox.x, cBox.z
						if selectedDir == 0:	cBox.cr, cBox.cl, cBox.cu, cBox.cd = cBox.cd, cBox.cr, cBox.cl, cBox.cu; #print(2)
						else:					cBox.cr, cBox.cl, cBox.cu, cBox.cd = cBox.cl, cBox.cu, cBox.cd, cBox.cr; #print(3)
					if selectedAxis == 2: 		
						x, y = cBox.x, cBox.y
						if selectedDir == 0:	cBox.cl, cBox.cd, cBox.cb, cBox.cf = cBox.cb, cBox.cf, cBox.cd, cBox.cl; #print(4)
						else:					cBox.cl, cBox.cd, cBox.cb, cBox.cf = cBox.cf, cBox.cb, cBox.cl, cBox.cd; #print(5)

					indexS+=1
					selected_list_coord.append((x+resto,y+resto,cBox.idB))
					cBox.isSelected = False

		matrix_sel = np.zeros((cube_size, cube_size), dtype='object')
		matrix_coor_cs = np.zeros((cube_size, cube_size), dtype='object')

		index_coor = 0
		for index in selected_list_coord:
			xM, yM, idcB = index[0], index[1], index[2]
			matrix_sel[int(xM), int(yM)] = idcB
			index_coor += 1

		if selectedAxis == 0:	axes_c = (1,0) if selectedDir == 0 else (0,1)
		if selectedAxis == 1: 	axes_c = (1,0) if selectedDir != 0 else (0,1)
		if selectedAxis == 2:	axes_c = (1,0) if selectedDir == 0 else (0,1)

		matrix_rot = np.rot90(matrix_sel, k=1, axes=axes_c)

		for x in range(cube_size):
			for y in range(cube_size):
				cID = boxes[matrix_rot[x,y]].idB
				cID = int(cID)	
				if selectedAxis == 0:	matrix_coor_cs[x,y] = (boxes[cID].y, boxes[cID].z)
				if selectedAxis == 1: 	matrix_coor_cs[x,y] = (boxes[cID].x, boxes[cID].z)
				if selectedAxis == 2: 	matrix_coor_cs[x,y] = (boxes[cID].x, boxes[cID].y)

		for x in range(cube_size):
			for y in range(cube_size):
				index = matrix_sel[x,y]
				if selectedAxis == 0:	boxes[index].y, boxes[index].z = matrix_coor_cs[x,y][0], matrix_coor_cs[x,y][1]
				if selectedAxis == 1: 	boxes[index].x, boxes[index].z = matrix_coor_cs[x,y][0], matrix_coor_cs[x,y][1]
				if selectedAxis == 2: 	boxes[index].x, boxes[index].y = matrix_coor_cs[x,y][0], matrix_coor_cs[x,y][1]
				



	def change_selected(boxes, selectedAxis, selectedLift):
		isSelected = False
		for cBox in boxes:
			x, y, z = cBox.x, cBox.y, cBox.z
			if 		selectedAxis 	== 0: 	isSelected = True if x == selectedLift else False
			elif 	selectedAxis	== 1: 	isSelected = True if y == selectedLift else False
			elif 	selectedAxis	== 2:	isSelected = True if z == selectedLift else False
			if isSelected: cBox.isSelected = True;
			else: cBox.isSelected = False

		boolSelection = False
		return boxes


	def update(boxes, selectedAxis, selectedLift, selectedDir, rotation_Sel, rotation_Cube, lift_list_asign):
		glPushMatrix()

		draw_Axis()

		draw_Core(lift_list_asign)

		#SELECTED BOXES ======================================================================
		glPushMatrix()
		#direction = 1 if selectedDir == 0 else -1
		if selectedDir == 0 or selectedDir == 1:
			if selectedAxis == 0: glRotatef(rotation_Sel, 1, 0, 0)
			if selectedAxis == 1: glRotatef(rotation_Sel, 0, 1, 0)
			if selectedAxis == 2: glRotatef(rotation_Sel, 0, 0, 1)
		
		for currentBox in boxes:
			x,y,z = 	currentBox.x, 	currentBox.y, 	currentBox.z
			cr, cl, cu, cd, cb, cf = 	currentBox.cr, currentBox.cl, currentBox.cu, currentBox.cd, currentBox.cb, currentBox.cf
			isSelected = currentBox.isSelected
			if isSelected:
				draw_cube(x,y,z, cr, cl, cu, cd, cb, cf, True, lift_list_asign)
		glPopMatrix()

		#NOT SELECTED BOXES ======================================================================
		glPushMatrix()
		for currentBox in boxes:
			x,y,z = currentBox.x, currentBox.y, currentBox.z
			cr, cl, cu, cd, cb, cf = 	currentBox.cr, currentBox.cl, currentBox.cu, currentBox.cd, currentBox.cb, currentBox.cf
			isSelected = currentBox.isSelected
			if not isSelected:
				draw_cube(x,y,z, cr, cl, cu, cd, cb, cf, False, lift_list_asign)
		glPopMatrix()

		glPopMatrix()


	class Box:
		def __init__(self, idB, x,y,z, cr, cl, cu, cd, cb, cf, isSelected):
			self.idB = idB

			self.x = x
			self.y = y
			self.z = z

			self.cr = cr
			self.cl = cl
			self.cu = cu
			self.cd = cd
			self.cb = cb
			self.cf = cf

			self.isSelected = isSelected


	def main(boxes, boolSelection, boolReor):

		#PYGAME INIT
		pygame.init()
		display = (800, 600)
		pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

		#OPENGL INIT
		gluPerspective(45, (display[0]/display[1]), 1, 1000.0)
		glTranslatef(0, 0, -50)
		glRotatef(0, 0, 0, 0)
		glEnable(GL_DEPTH_TEST)
		
		clock = pygame.time.Clock()


		#CREATE BOXES CLASSES ==================================================================================
		blen = 0
		
		for x in range(cube_size):
			for y in range(cube_size):
				for z in range(cube_size):
					if x == 0 or x == cube_size-1 or y == 0 or y == cube_size-1 or z == 0 or z == cube_size-1:
						print(blen)
						boxes[blen] = Box(blen, x-resto, y-resto, z-resto, 0, 1, 2, 3, 4, 5, False)
						blen+=1


		#CONTROL VARS
		key_W_pressed = False
		key_A_pressed = False
		key_S_pressed = False
		key_D_pressed = False
		key_R_pressed = False
		key_F_pressed = False

		key_Q_pressed = False
		key_E_pressed = False

		#PLAYER VARS
		mov_speed = 1

		#SELECTION VARS
		selectedAxis = 0
		selectedLift = 0
		selectedDir  = -1

		lift_list_asign = []
		first_lift_asign = 0 - ((cube_size-1)/2)
		for e in range(cube_size):
			lift_list_asign.append(first_lift_asign)
			first_lift_asign+=1

		#BOX ROTATION VARS
		isAnySelected = 0
		rotation_Sel 		= 360000
		rotation_Sel_Last 	= rotation_Sel
		rotation_Cube_X, rotation_Cube_Y, rotation_Cube_Z = 1, 1, 1

		speed_rot_sel = 9

		#CONTROLS INPUTS
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.MOUSEMOTION:
					mouse_pos = pygame.mouse.get_pos()
					
					bool_mouse = True
					

				#MOVEMENT CONTROLS ========================================================================
				if event.type == KEYDOWN:
					if event.key == pygame.K_w: key_W_pressed = True
					if event.key == pygame.K_a: key_A_pressed = True
					if event.key == pygame.K_s: key_S_pressed = True
					if event.key == pygame.K_d: key_D_pressed = True
					if event.key == pygame.K_r: key_R_pressed = True
					if event.key == pygame.K_f: key_F_pressed = True

					if event.key == pygame.K_q: key_Q_pressed = True
					if event.key == pygame.K_e: key_E_pressed = True

					if event.key == pygame.K_p: 
						if boolReor:
							boolReor = False
							speed_rot_sel = 5
						else:
							boolReor = True
							speed_rot_sel = 30

					#AXIS SELECTION ========================================================================
					if event.key == pygame.K_x: selectedAxis = 0; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_y: selectedAxis = 1; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_z: selectedAxis = 2; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False

					if event.key == pygame.K_1: selectedLift = lift_list_asign[0]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_2: selectedLift = lift_list_asign[1]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_3: selectedLift = lift_list_asign[2]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_4: selectedLift = lift_list_asign[3]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_5: selectedLift = lift_list_asign[4]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_6: selectedLift = lift_list_asign[5]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_7: selectedLift = lift_list_asign[6]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_8: selectedLift = lift_list_asign[7]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False
					if event.key == pygame.K_9: selectedLift = lift_list_asign[8]; boxes = change_selected(boxes, selectedAxis, selectedLift); 	isAnySelected+=1; boolSelection = False

					

					if event.key == pygame.K_t:
						if isAnySelected >= 1: 
							selectedDir = 0;
							rotation_Sel_Last = rotation_Sel +90
							isAnySelected = 0
					if event.key == pygame.K_g: 
						if isAnySelected >= 1: 
							selectedDir = 1;
							rotation_Sel_Last = rotation_Sel -90
							isAnySelected = 0

				if event.type == KEYUP:
					if event.key == pygame.K_w: key_W_pressed = False
					if event.key == pygame.K_a: key_A_pressed = False
					if event.key == pygame.K_s: key_S_pressed = False
					if event.key == pygame.K_d: key_D_pressed = False
					if event.key == pygame.K_r: key_R_pressed = False
					if event.key == pygame.K_f: key_F_pressed = False

					if event.key == pygame.K_q: key_Q_pressed = False
					if event.key == pygame.K_e: key_E_pressed = False



			#DRAW WORLD
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			glClearColor(0.2, 0.2, 0.2, 1)

			#print(rotation, ", ", rotation_Sel_Last, ", ", selectedDir)
			if rotation_Sel < rotation_Sel_Last: 
				if selectedDir == 0: rotation_Sel += speed_rot_sel
			else: 
				if selectedDir == 0: 
					change_position(selectedAxis, selectedDir)
					selectedDir = -1
					rotation_Sel = 360000

					boolSelection = True

			if rotation_Sel > rotation_Sel_Last: 
				if selectedDir == 1: rotation_Sel -= speed_rot_sel
			else: 
				if selectedDir == 1: 
					change_position(selectedAxis, selectedDir)
					selectedDir = -1
					rotation_Sel = 360000

					boolSelection = True

			#rotation_Cube+=0.15
			
			#MOVEMENT
			if key_Q_pressed: glTranslatef(0, 0, mov_speed)
			if key_E_pressed: glTranslatef(0, 0, -mov_speed)

			sen_rot = 3
			if key_W_pressed: rotation_Cube_Y = rotation_Cube_Y+sen_rot if rotation_Cube_Y <  90 else 90
			if key_S_pressed: rotation_Cube_Y = rotation_Cube_Y-sen_rot if rotation_Cube_Y > -90 else -90
			if key_A_pressed: rotation_Cube_X = rotation_Cube_X+sen_rot	if rotation_Cube_X < 360 else 1
			if key_D_pressed: rotation_Cube_X = rotation_Cube_X-sen_rot	if rotation_Cube_X > 1 else 360
			if key_F_pressed: rotation_Cube_Z = rotation_Cube_Z+sen_rot if rotation_Cube_Z <  90 else 90
			if key_R_pressed: rotation_Cube_Z = rotation_Cube_Z-sen_rot if rotation_Cube_Z > -90 else -90
			

			glPushMatrix()
			glRotatef(rotation_Cube_X-1, 0, 1, 0)
			glPushMatrix()
			glRotatef(rotation_Cube_Y-1, 1, 0, 0)
			glRotatef(rotation_Cube_Z-1, 0, 0, 1)

			update(boxes, selectedAxis, selectedLift, selectedDir, rotation_Sel, 0, lift_list_asign)
			glPopMatrix()
			glPopMatrix()


			if boolSelection and boolReor:

				selectedAxis = rd.randint(0,2)
				selectedLift = rd.randint(0,cube_size-1)
				selectedDir  = rd.randint(0,1)

				if selectedDir == 0: 	rotation_Sel_Last = rotation_Sel +90
				else: 					rotation_Sel_Last = rotation_Sel -90
				
				boxes = change_selected(boxes, selectedAxis, lift_list_asign[selectedLift]);
				boolSelection = False


				
			pygame.display.flip()
			clock.tick(60)

	if __name__ == "__main__":
		main(boxes, boolSelection, boolReor)


runCube()