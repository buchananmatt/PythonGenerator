#
#	Matthew Buchanan
#	27 Aug 17
#	G-Code Generator
#
#	The goal of this program is to generate g-code using basic python commands
#	I am hoping to use only console inputs instead of using the python interactive interpreter
#
#	Step 1: Get console arguments passed correctly...DONE!
#	Step 2: Make a function that generates G-Code for a circle...DONE!
#			args: circle 50(radius) 25(x-position center) 27(y-position center) 100(number of line segments)
#			circle start and end point should be the top 
#	Step 3: Access the circle function from the command-line...DONE!
#			NOTE: units are in radians
#	Step 4: Option to write to a file...
#
import sys		# this is the sys library which has sys.argv, which stores the command-line args
from math import sin, cos, pow, sqrt, pi, atan2
#from pathlib import Path
import os.path

#print "This is the name of the script: ", sys.argv[0]
#print "This is the number of arguments:", len(sys.argv)
#print "These are the arguments:", str(sys.argv)

def print_point(x_next, y_next):
	if write:
		with open(filestr, "a+") as file:
			file.write("G1 X{} Y{}\n".format(x_next, y_next))
	else:
		print "G1 X{} Y{}".format(x_next, y_next)

def circle(rad, x_pos, y_pos, num_seg):

	degrees_circle = 2 * pi

	x_start = float(x_pos)
	y_start = float(y_pos) + float(rad)

	x_next = x_start
	y_next = y_start

	deg_segment = degrees_circle/float(num_seg) #degrees per segment

	deg_ind = 0.0

	print_point(x_next, y_next)

	for i in range(0, int(num_seg)):

		deg_ind = deg_ind + deg_segment

		x_ind = float(rad) * sin(deg_ind)
		y_ind = float(rad) * cos(deg_ind)

		x_next = float(x_pos) + x_ind
		y_next = float(x_pos) + y_ind

		print_point(x_next, y_next)

def line(x_start, y_start, x_end, y_end, num_seg):

	print_point(x_start, y_start)

	length = sqrt(pow( float(x_end)-float(x_start) ,2)+pow( float(y_end)-float(y_start) ,2))

	len_segment = length / float(num_seg)
	len_ind = 0

#	if x_start > x_end: 
#		x_dist = x_start - x_end
#	else:
#		x_dist = x_end - x_start
#	if y_start > y_end: 
#		y_dist = y_start - y_end
#	else:
#		y_dist = y_end - y_start
	x_dist = float(x_end) - float(x_start)
	y_dist = float(y_end) - float(y_start)

	alpha = atan2(y_dist, x_dist)

	for i in range(0, int(num_seg)):
		len_ind = len_ind + len_segment

		x_ind = float(len_ind) * cos(alpha)
		y_ind = float(len_ind) * sin(alpha)

		x_next = float(x_start) + x_ind
		y_next = float(y_start) + y_ind

		print_point(x_next, y_next)

#MAIN PROGRAM STARTS HERE
index = 1;
write = False;

#FILE PRINTING MODULE
if str(sys.argv[1]) == "-f":
	write = True;
	index = 2
	if str(sys.argv[2]) == "-d":
		index = 4
		filestr = "./" + str(sys.argv[3])
	else:
		for i in range(0,100):
			filestr = './generated{}.gcode'.format(i)
			if os.path.isfile(filestr):
				print "file exists"
				continue
			else:
				file = open(filestr, "w+")
				break

#COMMAND-LINE ARGUMENT PARSER
if str(sys.argv[index]) == "circle":
	circle(sys.argv[index+1], sys.argv[index+2], sys.argv[index+3], sys.argv[index+4])
elif str(sys.argv[index]) == "line":
	line(sys.argv[index+1], sys.argv[index+2], sys.argv[index+3], sys.argv[index+4], sys.argv[index+5])
else:
	print "Command not found. Type circle followed by the radius, x center, y center, and # of line segements"
	sys.exit()
